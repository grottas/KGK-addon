# -*- coding: utf-8 -*-

from odoo import fields, models, tools, api

class CommissionReport(models.Model):
    _name = 'commission.report'
    _description = 'Generate data for commission reports'
    _auto = False
    _rec_name = 'id'

    start_date = fields.Datetime(string ='Start period', readonly=True)
    end_date = fields.Datetime(string ='End period', readonly=True)
    sales_agent = fields.Many2one('res.users', readonly=True)
    amount = fields.Float(string ='Amount', readonly=True)
    points = fields.Integer(string = 'Points', readonly=True)

    @api.model
    def get_report_values(self, userid):
        #find the users node in the hierarchy - first find the team she is leading and then the node
        #making assumption only lead of one team
        print('get_report_data for %d' % userid)
        teams = self.env['crm.team'].search([('user_id', '=', userid)])
        if len(teams)  == 0:
            return []

        team = teams[0]
        nodes = self.env['commission.hierarchy'].search([('team', '=', team.id)])
        if len(nodes) == 0:
            return []

        node = nodes[0]
        agent_ids = []
        agent_ids.extend(node.team.member_ids)

        nodes = self.env['commission.hierarchy'].child_nodes_deep(node.id)
        for node in nodes:
            for team in node.team:
                agent_ids.extend(team.member_ids)
        
        temp = []
        for id in agent_ids:
            temp.append(id.id)

        #add current user
        temp.append(userid)
        
        doc_ids = self.env['commission.summary'].search([('sales_agent', 'in', temp)])
        result = self.env['commission.summary'].browse(doc_ids)

        print(result)
        print('type of result %s' % type(result))
        
        docs = {
            'doc_ids' : doc_ids,
            'doc_model' : self.env['commission.summary'],
            'docs' : result,
            'data' : result,
        }

        return result
        

    """
    payslips = self.env['hr.payslip'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'data': data,
            'get_details_by_rule_category': self.get_details_by_rule_category(payslips.mapped('details_by_salary_rule_category').filtered(lambda r: r.appears_on_payslip)),
            'get_lines_by_contribution_register': self.get_lines_by_contribution_register(payslips.mapped('line_ids').filtered(lambda r: r.appears_on_payslip)),
        }
    """

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'commission_report')
        self._cr.execute("""
            create or replace view asset_asset_report as (
                select
                    start_date as start_date,
                    end_date as end_date,
                    sales_agent as sales_agent,
                    amount as amount,
                    points as points
                from commission_summary
                order by
                    sales_agent
        )""")