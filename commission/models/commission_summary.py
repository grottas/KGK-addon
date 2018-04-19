# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_summary(models.Model):
    _name = 'commission.summary'
    _description = 'Periodic commission summary per sales agent, manager'
    #commission summary for each calculation run for a period for each sales agent, manager

    start_date = fields.Datetime(string ='Start period', required=True)
    end_date = fields.Datetime(string ='End period', required=True)
    sales_agent = fields.Many2one('res.users', required=True)
    amount = fields.Float(string ='Amount')
    points = fields.Integer(string = 'Points')
    detail = fields.One2many('commission.detail', 'summary', string='Commission detail')


    @api.multi
    def name_get(self):
        names = []
        for summary in self:
            name = 'Commission for: '
            name += summary.sales_agent.name
            names.append((summary.id, name))
        return names
    

    @api.model
    def get_report_values(self, userid):
        return self.env['commission.report'].get_report_values(userid)