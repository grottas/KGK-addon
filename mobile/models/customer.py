# -*- coding: utf-8 -*-

from odoo import models, fields, api

class customer(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    identification_id = fields.Char(string= 'Identification Id')