# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime
import sys


class CommissionCalc(models.Model):
    _name="commission"
    _description='calculate commission'

    @api.multi
    def calculate(self):
        dict_agents = dict()
        start_time = datetime.datetime.now()

        groups = self.env['commission.group'].search([('active', '=', True)])
        for group in groups:
            teams = group.team_ids
            for team in teams:
                members = team.member_ids
                for member in members:
                    dict_agents.update({member.id : member.name})
        
        
        self.env.cr.execute('select "end_date" from "commission_summary" order by "end_date" desc limit 1')
        temp_time = self.env.cr.fetchone()
        
        # if there is no previous record start year 2000
        if(temp_time == None):
            start_time = datetime.datetime(2000, 1, 1)
        else:
            #start_time ==  datetime.datetime.strptime(temp_time[0], '%Y-%m-%d %H:%M:%S.%f')
            start_time = fields.Datetime.from_string(temp_time[0])

        print('start time %s'  % (start_time))
        
        
        for agent in list(dict_agents.keys()):
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print('calc for agent: %d - %s' % (agent,  dict_agents[agent]))
            self.__calc_agent(agent, start_time)
        
        #self.__calc_agent(688, start_time)
        self.__calc_commission_based(start_time)
        


    @api.model
    def __calc_agent(self, agent_id, start_time):
        dict_schemes = dict()
        dict_products = dict()
        today = datetime.date.today()
        arr_details = []
        total_amount = 0.0
        total_points = 0

        #find all teams the agent is member of and then all related groups
        teams = self.env['crm.team'].search([('active', '=', True), ('member_ids', '=', agent_id)])
        arr_teams = []
        for team in teams:
            arr_teams.append(team.id)

        groups = self.env['commission.group'].search([('active', '=', True), ('team_ids', 'in', arr_teams)])
        for group in groups:
            schemes = group.scheme_ids
            for scheme in schemes:
                dict_schemes.update({scheme.id : scheme})
                dict_products.update({scheme.product.id : scheme.product.categ_id})

        product_ids = list(dict_products.keys())

        # find total sales for the scheme
        calc_time = datetime.datetime.now()
        for scheme in list(dict_schemes.values()):
            salelines = []
            trigger_amount = 0.0
            trigger_qty = 0
            eligable_amount = 0.0
            eligable_qty = 0
            rate = 0

            print('scheme %s =====' % scheme.name)
        
            if(scheme.aggregation == 'c'):
                category = dict_products[scheme.product.id]
                products = self.env['product.product'].search([('categ_id', '=', category.id), ('id' , 'in', product_ids)])
                prod_ids = []
                for product in products:
                    prod_ids.append(product.id)

                salelines = self.env['sale.order.line'].search([('salesman_id', '=', agent_id), ('product_id', 'in', prod_ids), \
                    ('write_date', '>', fields.Datetime.to_string(start_time))])
            else:
                salelines = self.env['sale.order.line'].search([('salesman_id', '=', agent_id), ('product_id', '=', scheme.product.id), \
                     ('write_date', '>', fields.Datetime.to_string(start_time))])
            
            print('number of lines %d' % len(salelines))
            for saleline in salelines:
                print('id %d name %s qty %d' % (saleline.id, saleline.name, saleline.product_uom_qty))
                trigger_amount += saleline.price_total
                trigger_qty += saleline.product_uom_qty
                if saleline.product_id.id == scheme.product.id:
                    eligable_amount += saleline.price_total;
                    eligable_qty += saleline.product_uom_qty

            #points are calculate on quantity
            points = eligable_qty*scheme.points
            total_points += points

            # find eligable tiers
            for tier in scheme.tier_ids:
                amount = 0.0
                # if commission based skip
                if(tier.trigger == 'c'):
                    continue

                start_date = fields.Date.from_string(tier.active_from)
                end_date = fields.Date.from_string(tier.active_end) 
                tier_end = tier.tier_end
                # replace empty date fields (false)
                if (start_date == None):
                    start_date = start_time.date()
                if (end_date == None):
                    end_date = today
                if tier_end == 0:
                    tier_end = sys.maxsize

                if tier.type == 'q':
                    if (trigger_qty >= tier.tier_start) and (trigger_qty <= tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                        rate = tier.amount
                        amount += eligable_qty * tier.amount
                elif tier.type == 'v':
                    if (trigger_amount >= tier.tier_start) and (trigger_amount <= tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                        rate = tier.percent
                        amount += eligable_amount * tier.percent / 100

                # if tier doesn't apply skip
                if amount == 0.0:
                    continue
                
                total_amount += amount
                print('@@@@@ qty %d amount %d points %d' %(eligable_qty, amount, points))

                dict_detail = dict()
                dict_detail.update({'calc_datetime' : calc_time})
                dict_detail.update({'sales_agent' : agent_id})
                dict_detail.update({'product' : scheme.product.id})
                #dict_detail.update({'commission_group' : dict_schemes.get(scheme.id)})
                dict_detail.update({'commission_scheme' : scheme.id})
                dict_detail.update({'commission_tier' : tier.id})
                dict_detail.update({'type' : tier.type})
                dict_detail.update({'rate' : rate})
                dict_detail.update({'amount' : amount})
                arr_details.append((0, 0, dict_detail))          
        
        if total_amount == 0.0:
            return

        dict_summary = dict()
        dict_summary.update({'start_date' : start_time})
        dict_summary.update({'end_date' : calc_time})
        dict_summary.update({'sales_agent' : agent_id})
        dict_summary.update({'amount' : total_amount})
        dict_summary.update({'detail' : arr_details})
        print(dict_summary)
        print('==============================================================')
        self.env['commission.summary'].create(dict_summary)



    @api.model
    def __calc_commission_based(self, start_time):
        # caculate commissions for agents who receive commssion based on their team 
        print('calculate commission based =======================')

        # if there no commission based tiers exit
        tiers = self.env['commission.tier'].search([('trigger', '=', 'c')])
        if len(tiers) == 0:
            return        

        # travers commission hierarchy
        root_nodes = self.env['commission.hierarchy'].search([('parent_id', '=', False)])
        for root_node in root_nodes:
            child_nodes = root_node.child_nodes_deep(root_node.id)
            for child_node in child_nodes:
                self.__calc_manager(child_node, start_time)
     


    @api.model
    def __calc_manager(self, node, start_time):
        arrReports = []
        arrSchemes = []
        dicProducts = dict()
        total_commission = 0.0
        dict_schemes = dict()
        total_points = 0

        # if no team, i.e. no manager assigned skip
        if not node.team:
            return

        manager = node.team.user_id
        calc_time = datetime.datetime.now()
        print('===calc manager=== ' + str(node.team.user_id.name))

        # find all commisson schemes for manager
        groups = self.env['commission.group'].search([('team_ids', '=', node.team.id), ('active', '=', True)])
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

        # calculate points based on the number of products sold by reports
        total_points = self.__calc_points(arr_tmp, dict_schemes, dicProducts, start_time)
        print('points %d' % total_points)
                
        for product in dicProducts.keys():
            total = 0.0
            qty = 0
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
        dict_summary.update({'points' : total_points})
            
        self.env['commission.summary'].create(dict_summary)

        print('++total commission %d points %d' % (total_commission, total_points))


    @api.model
    def __calc_points(self, arr_reports, dict_schemes, dict_product, start_time):
        # calculate the points on the quantity sold for each eligable product
        total_points = 0
        dict_points = dict()

        #arr_products = list(dict_products.keys())
        arr_schemes = list(dict_schemes.keys())
        schemes = self.env['commission.scheme'].search([('id', 'in', arr_schemes)])
        for scheme in schemes:
            dict_points.update({scheme.product.id : scheme.points})

        salelines = self.env['sale.order.line'].search([('salesman_id', 'in', arr_reports), \
            ('write_date', '>', fields.Datetime.to_string(start_time))])
        for saleline in salelines:
            product = saleline.product_id.id
            qty = saleline.product_uom_qty
            print('calc points for product %d' % product)
            points = dict_points.get(product)
            print(points)
            if points is not None:
                total_points += qty*points
            
        return total_points