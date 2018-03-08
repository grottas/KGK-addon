# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionScheme(models.Model):
    _name = 'commission.scheme'
    _description = 'Define commission scheme'

    name = fields.Char(string = 'Name of scheme', required = True, size = 30)
    active = fields.Boolean(string = 'Active?', required = True, default=True)
    product = fields.Many2one('product.product', required = True, string = 'Product')
    tier_ids = fields.One2many('commission.tier', 'scheme', string = 'Commission tiers')


    @api.multi
    def calculate(self):
        print('calculate')
        self.env['commission'].calculate()
        