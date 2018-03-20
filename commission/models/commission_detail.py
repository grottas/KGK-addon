# -*- coding: utf-8 -*-

from odoo import models, fields, api

class commission_detail(models.Model):
    _name = 'commission.detail'
    _description = 'Detailed commission history'
    #track commssion calculation for each sold product with link to the tier used

    calc_datetime = fields.Datetime(string = 'Calculation date', required=True)
    sales_agent = fields.Many2one('res.users', required=True, string = 'Sales agent')
    product = fields.Many2one('product.product', required=True, string='Product sold')
    commission_group = fields.Many2one('commission.group', string='Commission group')
    commission_scheme = fields.Many2one('commission.scheme', required=True, string='Commission scheme')
    commission_tier = fields.Many2one('commission.tier', required=True, string='Commission tier')
    type = fields.Char(string ='Type')
    rate = fields.Float(string = 'Rate')
    amount = fields.Float(string = 'Amount')
    points = fields.Integer(string = 'Points')
    summary = fields.Many2one('commission.summary', required=True, ondelete='cascade')