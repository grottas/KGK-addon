# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MobileProduct(models.Model):
     _name = 'product.template'
     _inherit = 'product.template'
     _description = 'add additional product information'

     information = fields.Html(string='Product information')