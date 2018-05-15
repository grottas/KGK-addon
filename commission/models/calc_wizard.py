# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CalcWizard(models.TransientModel):
    _name = 'commission.calc.wizard'

    partner = fields.Many2one('res.partner', required=True, string='Partner')
    customer = fields.Char(string='Customer', required=True)
    identification_id = fields.Char(string='Identification number', help='Number of the identificaton document provided by the customer')
    product = fields.Many2one('product.product', required=True, string='Product sold')
    issue = fields.Text(string='Open issues')
    create_date = fields.Date(string='Date created')
    sales_agent = fields.Many2one('res.users', string='Sales agent')
    amount = fields.Float(string='Amount')
    update_date = fields.Datetime('Last update on')
    start_date = fields.Datetime('Calculation start date')

    def _get_default_commission_status(self):
        status_ids = self.env['commission.status'].search([('issue', '=', 'DISBURSED')])
        return self.env['commission.status'].browse(status_ids)