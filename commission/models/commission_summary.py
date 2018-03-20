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