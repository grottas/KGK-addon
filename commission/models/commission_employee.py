# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    sales_target = fields.Many2one('commission.target', string = 'Sales target')