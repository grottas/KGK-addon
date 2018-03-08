# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionGroup(models.Model):
    _name = 'commission.group'
    _description = 'Define commission tiers'

    name = fields.Char(string = 'Name', required = True, size = 30)
    active = fields.Boolean(string = 'Active?', default = True)
    scheme_ids = fields.Many2many('commission.scheme', 'comm_group_scheme', 'group_id', 'scheme_id', string ='Included schemes')
    salesperson_ids = fields.Many2many('res.users', 'comm_group_user', 'group_id' 'user_id', string = 'Sales person')
