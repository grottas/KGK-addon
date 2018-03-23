# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleStatus(models.Model):
    _name = 'sale.status'
    _description = 'Status informaton on sales received from partner'


    identifier = fields.Char(string='external identifier', required=True, index=True)
    partner = fields.Many2one('res.partner', required=True, string='Partner')
    customer = fields.Char(string='Customer', required=True)
    product = fields.Many2one('product.product', required=True, string='Product sold')
    product_category = fields.Many2one('product.category', string='Product category')
    issue = fields.Text(string='Open issues')
    create_date = fields.Date(string='Date created')
    phone = fields.Char(string='Phone number')
    mobile = fields.Char(string='Mobile number')
    notes = fields.Text(string='Notes')
    agent = fields.Many2many('res.users', string='Sales agent')
    amount = fields.Float(string='Amount')
    update_date = fields.Datetime('Last update on')
    detail = fields.One2many('sale.status.detail', 'sale_status', string='Status detail')


class SaleStatusDetail(models.Model):
    _name = 'sale.status.detail'
    _description = 'History of the status changes of the sale'

    sale_status = fields.Many2one('sale.status', required=True, ondelete='cascade')
    status_date = fields.Datetime(string='Date status changed')
    status = fields.Char(string='status')
