# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionStatus(models.Model):
    _name = 'commission.status'
    _description = 'Status informaton on commission related sales activity from partner'


    identifier = fields.Char(string='External identifier', required=True, index=True)
    partner = fields.Many2one('res.partner', required=True, string='Partner')
    customer = fields.Char(string='Customer', required=True)
    identification_id = fields.Char(string='Identification number', help='Number of the identificaton document provided by the customer')
    product = fields.Many2one('product.product', required=True, string='Product sold')
    product_category = fields.Many2one('product.category', string='Product category')
    issue = fields.Text(string='Open issues')
    create_date = fields.Date(string='Date created')
    phone = fields.Char(string='Phone number')
    mobile = fields.Char(string='Mobile number')
    notes = fields.Text(string='Notes')
    sales_agent = fields.Many2one('res.users', string='Sales agent')
    amount = fields.Float(string='Amount')
    update_date = fields.Datetime('Last update on')
    detail = fields.One2many('commission.status.detail', 'sale_status', string='Status detail')
    lead_id = fields.Many2one('crm.lead', string='Associated lead')


class SaleStatusDetail(models.Model):
    _name = 'commission.status.detail'
    _description = 'History of the status changes'

    sale_status = fields.Many2one('sale.status', required=True, ondelete='cascade')
    status_date = fields.Datetime(string='Date status changed')
    status = fields.Char(string='Status')
    changed_by = fields.Char(string='Updated by')
    notes = fields.Text(string='Status notes')
