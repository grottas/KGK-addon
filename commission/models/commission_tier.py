# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionTier(models.Model):
    _name = 'commission.tier'
    _description = 'Define commission tiers'

    type = fields.Selection((('v','Value'), ('q','Quantity')), string='Calculation base', required = True)
    tier_start = fields.Integer(string='Start value', default=0)
    tier_end = fields.Integer(string = 'End value')
    amount = fields.Float(string = 'Commission amount')
    percent = fields.Float(string = 'Commission percent')
    trigger = fields.Selection((('s', 'Sales'), ('c', 'Commission')), string = 'Triggered by' )
    active_from = fields.Date(string = 'Start date')
    active_end = fields.Date(string = 'End date')
    scheme = fields.Many2one('commission.scheme', required=True, ondelete='cascade')


    @api.onchange('tier_start')
    def check_overlap(self):
        scheme_id = self.scheme
        start = self.tier_start

        print(start)
        print(scheme_id)
