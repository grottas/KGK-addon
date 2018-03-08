# -*- coding: utf-8 -*-

from odoo import models, fields, api

class mobile(models.Model):
     _name = 'res.partner'
     _inherit = 'res.partner'

     num_employees = fields.Integer(string="Number of employes")
     year_founded = fields.Integer( string = "Year founded")
     capital = fields.Integer( string = "Founding captial")
