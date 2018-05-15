# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime
import sys
import logging
_logger = logging.getLogger(__name__)


class CommissionCalc(models.Model):
    _name="commission"
    _description='calculate commission'

    @api.multi
    def calculate(self):
        start_time = datetime.datetime.now()
        self.env.cr.execute('select "end_date" from "commission_summary" order by "end_date" desc limit 1')
        temp_time = self.env.cr.fetchone()
        
        # if there is no previous record start year 2000
        if(temp_time == None):
            start_time = datetime.datetime(2000, 1, 1)
        else:
            #start_time ==  datetime.datetime.strptime(temp_time[0], '%Y-%m-%d %H:%M:%S.%f')
            start_time = fields.Datetime.from_string(temp_time[0])

        print('start time %s'  % (start_time))

        self.__calc_agents(start_time)
        self.__calc_manager(start_time)


    @api.model
    def __calc_agents(self, start_time):
        # create list of all applicaple users
        dict_agents = dict()

        groups = self.env['commission.group'].search([('active', '=', True)])
        for group in groups:
            teams = group.team_ids
            for team in teams:
                members = team.member_ids
                for member in members:
                    dict_agents.update({member.id : member.name})

        for agent_id in dict_agents.keys():
            print('=================================')
            print('calc for %d %s' %(agent_id, dict_agents.get(agent_id)))
            self.__calc_for_agent(start_time, agent_id)


    @api.model
    def __calc_for_agent(self, start_time, agent_id, is_manager=False):
        #find all groups the belongs to and then related schemes
        dict_schemes = dict()
        calc_time = datetime.datetime.now()
        total_amount = 0.0
        total_points = 0

        team = []
       
        #get the users team id
        temp = self.env['res.users'].search([('id', '=', agent_id)])[0].sale_team_id.id
        team = [temp]

        print('teams %s' % team)
        
        groups = self.env['commission.group'].search([('team_ids', 'in', team)])
        for group in groups:
            schemes = group.scheme_ids
            for scheme in schemes:
                if scheme.active:
                    dict_schemes.update({scheme.id : scheme.name})

        print('number of schemes %d' % len(dict_schemes.keys()))

        #manager get all reports
        agents = []
        if is_manager:
            agents = self.__get_reports(agent_id)
        else:
            agents = [agent_id]
        
        arr_details = []
        for scheme_id in dict_schemes.keys():
            print('commission for %s' % ( dict_schemes.get(scheme_id)))
            
            commission_detail = self.__calc_agent_scheme(start_time, agents, scheme_id)

            print(commission_detail)
            
            for temp in commission_detail:
                arr_details.append((0, 0, temp))
                total_amount += temp.get('amount', 0)
                total_points += temp.get('points', 0)
                temp.update({'sales_agent' : agent_id})

        commission_summary = dict()
        commission_summary.update({'start_date' : start_time})
        commission_summary.update({'end_date': calc_time})
        commission_summary.update({'sales_agent' : agent_id})
        commission_summary.update({'amount' : total_amount})
        commission_summary.update({'points' : total_points})
        commission_summary.update({'detail' : arr_details})

        print('commission amount %d ========' % total_amount)
        self.__log_commission(commission_summary)

        
    @api.model
    def __calc_agent_scheme(self, start_time, agent_id, scheme_id):
        commission_detail = dict()
        arr_details = []
        calc_time = datetime.datetime.now()
        today = datetime.date.today()
        
        scheme = self.env['commission.scheme'].browse([scheme_id])
        dict_triggers = self.__calc_triggers(start_time, agent_id, scheme.aggregation, scheme.product.id)
        dict_comm_triggers = self.__calc_comm_triggers(start_time, agent_id, scheme.aggregation, scheme.product.id)

        # find matching tier/rate
        for tier in scheme.tier_ids:
            rate = 0
            amount = 0.0
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

            trigger_qty = dict_triggers.get('trigger_qty')
            print('trigger qty %d tier_start %d tier_end %d' %(trigger_qty, tier.tier_start, tier_end))
            trigger_amount = dict_triggers.get('trigger_amount')
            if tier.trigger == 's': # triggered by sales
                if tier.type == 'q': #sales quantity
                    if (trigger_qty >= tier.tier_start) and (trigger_qty <= tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                        rate = tier.amount
                        eligible_qty = dict_triggers.get('eligible_qty', 0)
                        print('quantity rate %d - eligible %d ' % (rate, eligible_qty))
                        amount += eligible_qty * tier.amount
                elif tier.type == 'v': #sales volume     
                    if (trigger_amount >= tier.tier_start) and (trigger_amount <= tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                        rate = tier.percent
                        eligible_amount = dict_triggers.get('eligible_amount', 0)
                        print('percent rate %d - eligible %d ' % (rate, eligible_amount))
                        amount += eligible_amount * tier.percent / 100

            elif tier.trigger == 'c': # triggered by commission
                trigger_amount = dict_comm_triggers.get('trigger_amount', 0)
                print('commission based trigger %d - eligible %d' % (trigger_amount, dict_comm_triggers.get('eligible_amount', 0)))
                if (trigger_amount >= tier.tier_start) and (trigger_amount <= tier_end) and (start_date >= start_time.date()) and (end_date <= today):
                    rate = tier.percent
                    eligible_amount = dict_comm_triggers.get('eligible_amount', 0)
                    amount += eligible_amount * rate / 100

            if amount == 0: # tier did not apply
                continue

            points = scheme.points * dict_triggers.get('eligible_qty', 0)
            
            commission_detail.update({'calc_datetime' : calc_time })
            commission_detail.update({ 'sales_agent' : 0})
            commission_detail.update({'product' : scheme.product.id})
            commission_detail.update({'commission_group' : 0})
            commission_detail.update({'commission_scheme' : scheme.id})
            commission_detail.update({'commission_tier' : tier.id})
            commission_detail.update({'type' : tier.type})
            commission_detail.update({'rate' : rate })
            commission_detail.update({'amount' : amount})
            commission_detail.update({'points' : points })
            arr_details.append(commission_detail)

        return arr_details


    @api.model
    def __calc_triggers(self, start_time, agent_id, aggregation, product_id):
        # the trigger amounts determined by the aggregation method (c, m, p)
        product_ids = self.__get_products(product_id, aggregation)        

        if not isinstance(agent_id, list):
            agent_id = [agent_id]

        salelines = self.env['sale.order.line'].search([('salesman_id', 'in', agent_id), ('product_id', 'in', product_ids), \
                ('write_date', '>=', fields.Datetime.to_string(start_time))])

        print(' calc trigger - number of sales lines %d' % len(salelines))

        trigger_amount = 0.0
        trigger_qty = 0
        eligible_amount = 0.0
        eligible_qty = 0

        for saleline in salelines:
            trigger_amount += saleline.price_total
            trigger_qty += saleline.product_uom_qty
            if saleline.product_id.id == product_id:
                eligible_amount += saleline.price_total;
                eligible_qty += saleline.product_uom_qty

        dict_result = dict()
        dict_result.update({'trigger_amount' : trigger_amount})
        dict_result.update({'trigger_qty' : trigger_qty})
        dict_result.update({'eligible_amount' : eligible_amount})
        dict_result.update({'eligible_qty' : eligible_qty})

        return dict_result
    


    @api.model
    def __calc_manager(self, start_time):
        # travers commission hierarchy
        root_nodes = self.env['commission.hierarchy'].search([('parent_id', '=', False)])
        for root_node in root_nodes:
            child_nodes = root_node.child_nodes_deep(root_node.id)
            for child_node in child_nodes:
                manager = child_node.manager
                if not manager:
                    _logger.warning('No manager assigned to node: %s' % child_node.name)
                    continue
                agent_id = manager.id
                print('=============================================================')
                print('calc_manager %s' % manager.name)
                self.__calc_for_agent(start_time, agent_id, is_manager=True)
            #calc root note
            manager = root_node.manager
            if not manager:
                _logger.warning('No manager assigned to node: %s' % root_node.name)
                continue
            agent_id = manager.id
            
            print('=============================================================')
            print('calc_manager %s' % manager.name)
            self.__calc_for_agent(start_time, agent_id, is_manager=True)

    
    @api.model
    def __log_commission(self, commission_summary):
        o_summary = self.env['commission.summary']

        try:
            o_summary.create(commission_summary)
        except Exception as exc:
            _logger.error('Error saving commission: %s' % exc)
            raise UserError('Failed saving commision summary')


    @api.model
    def __get_reports(self, agent_id):
        arr_reports = []

        #find the node she manages
        nodes = self.env['commission.hierarchy'].search([('manager', '=', agent_id)])
        for node in nodes:
            child_nodes = node.child_nodes_deep(node.id)
            for _node in child_nodes:
                print('number of teams %d' % len(_node.team_ids))
                for team in _node.team_ids:
                    arr_reports.extend([user.id for user in team.member_ids])
            #also include current node
            for team in node.team_ids:
                arr_reports.extend([user.id for user in team.member_ids])
            

        print('reports %d' % len(arr_reports))
        return arr_reports


    @api.model
    def __calc_comm_triggers(self, start_time, agents, aggregation, product_id):
        product_ids = self.__get_products(product_id, aggregation)
        details = self.env['commission.detail']. search([('product', 'in', product_ids), ('sales_agent', 'in', agents), \
            ('calc_datetime', '>', fields.Datetime.to_string(start_time))])

        print('product ids %s  sales agents %s #details %d' %(product_ids, agents, len(details)))

        eligible_amount = 0.0
        trigger_amount = 0.0

        for detail in details:
            trigger_amount += detail.amount
            if detail.product.id == product_id:
                eligible_amount += detail.amount

        result = dict()
        result.update({'trigger_amount' : trigger_amount})
        result.update({'eligible_amount' : eligible_amount})
        return result


    @api.model
    def __get_products(self, product_id, aggregation):
        # get products based on aggegation method
        product_ids = []
        temp = self.env['product.product'].browse([product_id])

        if aggregation == 'c': #category
            # find all other product in category
            category_id = 0            
            if(len(temp) > 0):
                category_id = temp[0].categ_id.id
            products = self.env['product.product'].search([('categ_id', '=', category_id)])
            for product in products:
                product_ids.append(product.id)
               
        elif aggregation == 'm': # product master
            #find product for product master
            prod_template = 0
            if(len(temp) > 0):
                prod_template = temp[0].product_tmpl_id.id
            products = self.env['product.product'].search([('product_tmpl_id', '=', prod_template.id)])
            for product in products:
                product_ids.append(product.id)

        else: # by product
            product_ids.append(product_id)

        return product_ids


