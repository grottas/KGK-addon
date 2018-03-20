# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionTarget(models.Model):
    _name = 'commission.target'
    _description = 'Sales targets for an employee based on points'

    name = fields.Char(string = 'Name', required = True, size = 50)
    code = fields.Char(string = 'Code', required = True, size = 6)
    active = fields.Boolean(string = 'Active?', default = True)
    target_start = fields.Integer(string = 'Start')
    target_end = fields.Integer(string = 'End')
    salary = fields.Integer(string = 'Salary')
