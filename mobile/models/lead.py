# -*- coding: utf-8 -*-

from odoo import models, fields, api

class lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    source = fields.Many2one('res.partner', string='Lead source')


    @api.model
    def pipeline_count(self):
        # return the count of leads per stage
        result = dict()
        stages = self.env['crm.stage'].search([])
        for stage in stages:
            id = stage.id
            domain = [('stage_id', '=', id), ('active', '=', 't')]
            count = self.env['crm.lead'].search_count(domain)
            result[id] = count

        return result


    @api.model
    def create(self, vals):
        
        if 'partner_id' in vals:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            vals['partner_name'] = partner.name
            if 'contact_name' not in vals:
                vals['contact_name'] = partner.name if not partner.is_company else False
            if 'title' not in vals:
                vals['title'] = partner.title.id
            if 'street' not in vals:
                vals['street'] = partner.street
            if 'street2' not in vals:
                vals['street2'] =  partner.street2
            if 'city' not in vals:
                vals['city'] = partner.city
            if 'state_id' not in vals:
                vals['state_id'] = partner.state_id.id
            if 'country_id' not in vals:
                vals['country_id'] = partner.country_id.id
            if 'email_from' not in vals:
                vals['email_from'] = partner.email
            if 'phone' not in vals:
                vals['phone'] = partner.phone
            if 'mobile' not in vals:
                vals['mobile'] = partner.mobile
            if 'zip' not in vals:
                vals['zip'] = partner.zip
            if 'function' not in vals:
                vals['function'] = partner.function
            if 'website' not in vals:
                vals['website'] = partner.website

        return super(lead, self).create(vals)




    @api.multi
    def write(self, vals):

        if 'partner_id' in vals:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            vals['partner_name'] = partner.name
            if 'contact_name' not in vals:
                vals['contact_name'] = partner.name if not partner.is_company else False
            if 'title' not in vals:
                vals['title'] = partner.title.id
            if 'street' not in vals:
                vals['street'] = partner.street
            if 'street2' not in vals:
                vals['street2'] =  partner.street2
            if 'city' not in vals:
                vals['city'] = partner.city
            if 'state_id' not in vals:
                vals['state_id'] = partner.state_id.id
            if 'country_id' not in vals:
                vals['country_id'] = partner.country_id.id
            if 'email_from' not in vals:
                vals['email_from'] = partner.email
            if 'phone' not in vals:
                vals['phone'] = partner.phone
            if 'mobile' not in vals:
                vals['mobile'] = partner.mobile
            if 'zip' not in vals:
                vals['zip'] = partner.zip
            if 'function' not in vals:
                vals['function'] = partner.function
            if 'website' not in vals:
                vals['website'] = partner.website

        return super(lead, self).write(vals)
