# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class Commission(models.Model):
    _name="commission_old"

    @api.multi
    def calculate(self):
        arrProducts = []
        arrSchemes = []
        arrSaleLine = []
        dicAgents = dict()

        self.env.cr.execute('select "end_date" from "commission_summary" order by "end_date" desc limit 1')
        start_time = self.env.cr.fetchone()
        # if there is no previous record start year 2000
        if(start_time == None):
            start_time = datetime.datetime(2000, 1, 1)
        print('start time %s'  % (start_time))
     
        m_group = self.env['commission.group']
        groups = m_group.search([('active', '=', True)])
    
        # find all sales people with commission configured
        for group in groups:
            for id in group.salesperson_ids:
                dicAgents.update({id.id : id.id})
                print('agent %s' % id.login)
                self.calc_for_user(id.id, start_time)
        
        # calculate commission based tiers
        self.__calc_commission_based(dicAgents.keys(), start_time)
       
        """
        for agent in arrAgents:
            print(agent)
            lines = self.env['sale.order.line'].search([('salesman_id', '=', agent), ('product_id', 'in', arrProducts)])
            for line in lines:
                print(line.product_uom_qty)

        tiers = self.env['commission.tier'].search([('activeFrom', '<=', today), ('activeEnd', '>=', today)])
        for tier in tiers:
            print(tier.type)
        """
        # m_orderline = self.pool['sale.order.line']
        

    @api.model
    def calc_for_user(self, user_id, start_time):
        today = datetime.date.today()
        arr_scheme_ids = []
        arr_product_ids = []
        arr_tiers = []
        arr_triggers = [0, 0] # contains sales qty, total price pair for product
        dict_lines = dict()
        dict_schemes = dict()
        prod_id = 0

        # find schemes for the user
        groups = self.env['commission.group'].search([('active', '=', True), ('salesperson_ids', '=', user_id)])
        for group in groups:
            for id in group.scheme_ids:
                arr_scheme_ids.append(id.id)
                dict_schemes.update({id.id : group.id})

        # find all product with commission configured
        schemes = self.env['commission.scheme'].search([('active', '=', True), ('id', 'in', arr_scheme_ids)])
        for scheme in schemes:
            arr_product_ids.append(scheme.product.id)
            for id in scheme.tier_ids:
                arr_tiers.append(id.id)

        # find order lines with product applicable for commission
        calc_time = datetime.datetime.now()
        lines = self.env['sale.order.line'].search([('salesman_id', '=', user_id), ('product_id', 'in', arr_product_ids), \
            ('write_date', '>', fields.Datetime.to_string(start_time))])
        for line in lines:
            prod_id = line.product_id.id
            if prod_id in dict_lines.keys():
                arr_triggers = dict_lines.get(prod_id)
                qty = arr_triggers[0]
                value = arr_triggers[1]
                qty += line.product_uom_qty
                value += line.price_total
                arr_triggers[0] = qty
                arr_triggers[1] = value
                dict_lines.update({prod_id : arr_triggers})
            else:
                arr_triggers[0] = line.product_uom_qty
                arr_triggers[1] = line.price_total
                dict_lines.update({prod_id : arr_triggers})

        # all commission schemes/tiers for sold product
        for key in dict_lines.keys():
            arr_triggers = dict_lines.get(key)
            arr_tiers = []
            arr_details = []
            product_amount = 0.0

            #retrieve schemes for this product and have been filtered for user
            schemes = self.env['commission.scheme'].search([('active', '=', True), ('product', '=', key), ('id', 'in', arr_scheme_ids)])
            for scheme in schemes:     
                arr_schemes = [] 
                rate = 0.0
                tiers = scheme.tier_ids

                # find eligable tiers based on type and sales qty/price
                for tier in tiers:
                    amount = 0.0
                    # if commission based skip
                    if(tier.trigger == 'c'):
                        continue

                    start_date = fields.Date.from_string(tier.active_from)
                    end_date = fields.Date.from_string(tier.active_end) 
                    # replace empty date fields (false)
                    if (start_date == None):
                        start_date = start_time.date()
                    if (end_date == None):
                        end_date = today

                    if tier.type == 'q':
                        qty = arr_triggers[0]
                        print('qunatity %d start %s tierstart %s' % (qty, start_date, end_date))
                        if (qty >= tier.tier_start) and (qty <= tier.tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                            arr_tiers.append(tier)
                            rate = tier.amount
                            amount += qty * tier.amount
                    elif tier.type == 'v':
                        value = arr_triggers[1]
                        if (value >= tier.tier_start) and (value <= tier.tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                            arr_tiers.append(tier)
                            rate = tier.percent
                            amount += value * tier.percent / 100

                    # if tier doesn't apply skip
                    if amount == 0.0:
                        continue
                    
                    product_amount += amount

                    dict_detail = dict()
                    dict_detail.update({'calc_datetime' : calc_time})
                    dict_detail.update({'sales_agent' : user_id})
                    dict_detail.update({'product' : key})
                    dict_detail.update({'commission_group' : dict_schemes.get(scheme.id)})
                    dict_detail.update({'commission_scheme' : scheme.id})
                    dict_detail.update({'commission_tier' : tier.id})
                    dict_detail.update({'type' : tier.type})
                    dict_detail.update({'rate' : rate})
                    dict_detail.update({'amount' : amount})
                    arr_details.append((0, 0, dict_detail))

            dict_summary = dict()
            dict_summary.update({'start_date' : start_time})
            dict_summary.update({'end_date' : calc_time})
            dict_summary.update({'sales_agent' : user_id})
            dict_summary.update({'amount' : product_amount})
            dict_summary.update({'detail' : arr_details})

            self.env['commission.summary'].create(dict_summary)
            
            print('amount: %d for product %d ' % (product_amount, key))
            print('==============================')

    
    def __calc_commission_based(self, arrAgents, start_time):
        # caculate commissions for agents who receive commssion based on their team 
        print('calculate commission based =======================')

        # id there no commission based tiers exit
        tiers = self.env['commission.tier'].search([('trigger', '=', 'c')])
        if len(tiers) == 0:
            return        

        # travers commission hierarchy
        root_nodes = self.env['commission.hierarchy'].search([('parent_id', '=', False)])
        for root_node in root_nodes:
            child_nodes = root_node.child_nodes_deep(root_node.id)
            for child_node in child_nodes:
                self.__calc_manager(child_node, start_time)
            


        """
        # check if user is team lead and what hierchary level
        for agent in arrAgents:
            print('agent %d' % agent)
            arrReports = []
            teams = self.env['crm.team'].search([('user_id', '=', agent)])
            for team in teams:
                arrReports.extend(team.member_ids)
                nodes = self.env['commission.hierarchy'].search([('team', '=', team.id)])
                for node in nodes:
                    print('node - ' + node.name)
                    arrReports.extend(node.team.member_ids)
                    # get all agents in graph
                    child_nodes = node.child_nodes_deep(node.id)
                    for child_node in child_nodes:
                        print('child - ' + child_node.name)
                        arrReports.extend(child_node.team.member_ids)

            print(arrReports)
        """

    def __calc_manager(self, node, start_time):
        arrReports = []
        arrSchemes = []
        dicProducts = dict()
        total_commission = 0.0
        dict_schemes = dict()

        # if no team, i.e. no manager assigned skip
        if not node.team:
            return

        manager = node.team.user_id
        calc_time = datetime.datetime.now()
        print('===calc manager=== ' + str(node.team.user_id.name))

        # find all commisson schemes for manager
        groups = self.env['commission.group'].search([('salesperson_ids', '=', manager.id)])
        for group in groups:
            for scheme in group.scheme_ids:
                if scheme.active:
                    arrSchemes.append(scheme)
                    dict_schemes.update({scheme.id : group.id})

        # get applicable products
        for scheme in arrSchemes:
            if scheme.active:
                dicProducts.update({scheme.product.id : scheme.product.id})


        child_nodes = node.child_nodes_deep(node.id)
        arrReports.extend(node.team.member_ids)

        # get teammembers of all child nodes
        for child_node in child_nodes:
            arrReports.extend(child_node.team.member_ids)

        # get all commissions for the sales agents and calculate total
        arr_tmp = []
        for report in arrReports:
            arr_tmp.append(report.id)

        print('number of members: %d'  % len(arr_tmp))
                
        for product in dicProducts.keys():
            total = 0.0
            commission = 0.0
            dic_summary = dict()
            arr_details = []

            lines = self.env['commission.detail'].search([('sales_agent', 'in', arr_tmp), ('product', '=', product), \
                ('write_date', '>', fields.Datetime.to_string(start_time))])
            for line in lines:
                total += line.amount

            for scheme in arrSchemes:
                # skip if scheme does apply to product
                if(scheme.product.id != product):
                    continue

                tiers = scheme.tier_ids
                for tier in tiers:
                    # skip tiers that are not commission based
                    if tier.trigger != 'c':
                        continue

                    temp = total * tier.percent / 100
                    commission += temp

                    dict_detail = dict()
                    dict_detail.update({'calc_datetime' : calc_time})
                    dict_detail.update({'sales_agent' : manager.id})
                    dict_detail.update({'product' : product})
                    dict_detail.update({'commission_group' : dict_schemes.get(scheme.id)})
                    dict_detail.update({'commission_scheme' : scheme.id})
                    dict_detail.update({'commission_tier' : tier.id})
                    dict_detail.update({'type' : tier.type})
                    dict_detail.update({'rate' : tier.percent})
                    dict_detail.update({'amount' : temp})
                    arr_details.append((0, 0, dict_detail))

            print('manager commission %d for product %d ' % (commission, product))
            total_commission += commission
        if total_commission == 0:
            return
        dict_summary = dict()
        dict_summary.update({'start_date' : start_time})
        dict_summary.update({'end_date' : calc_time})
        dict_summary.update({'sales_agent' : manager.id})
        dict_summary.update({'amount' : total_commission})
        dict_summary.update({'detail' : arr_details})
            
        self.env['commission.summary'].create(dict_summary)

        print('total commission %d ' % total_commission)

