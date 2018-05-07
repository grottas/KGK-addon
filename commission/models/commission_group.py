# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CommissionGroup(models.Model):
    _name = 'commission.group'
    _description = 'Define commission tiers'

    name = fields.Char(string = 'Name', required = True, size = 30)
    active = fields.Boolean(string = 'Active?', default = True)
    scheme_ids = fields.Many2many('commission.scheme', 'comm_group_scheme', 'group_id', 'scheme_id', string ='Included schemes')
    team_ids = fields.Many2many('crm.team', 'comm_group_team', 'group_id', 'team_id', string = 'Sales teams')
    