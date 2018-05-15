# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class lead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"

    source = fields.Many2one('res.partner', string='Lead source')
    product = fields.Many2one('product.product', help='Customer is interested in this product')
    external_status = fields.Char(compute='_get_status', string='Status', store=False, help='Status provided by external partner')


    @api.model
    def pipeline_count(self, user_id):
        if user_id == None:
            _logger.warning('pipeline_count: no user id provided')

        # return the count of leads per stage
        result = dict()
        stages = self.env['crm.stage'].search([])
        for stage in stages:
            id = stage.id
            domain = [('stage_id', '=', id), ('active', '=', 't'), ('user_id', '=', user_id)]
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


    @api.multi
    def _get_status(self):
        for lead in self:
            temp = self.env['commission.status'].search([('lead_id', '=', lead.id)])
            for status in temp:
                lead.external_status = status.issue


    @api.model
    def search_mobile(self, args, user= None):
        offset=0
        limit=200 
        order='id desc'
        fields = ['id', 'name', 'partner_name', 'city', 'contact_name', 'phone', 'email_from']
        #if no user specified default to current user
        print(user)
        if user is None:
            user = self.env.user.id

        #if it's a manager find all the rports for she can view data
        users = [user]
        users += self.env['commission.hierarchy'].get_reports(651)

        print(users)

        domain = []
        domain += [ '&', '&', ('active', '=', True), ('user_id', 'in', users), '|', ('name', 'ilike', args), \
            '|', ('partner_name', 'ilike', args), ('city', 'ilike', args)]

        result = self.search_read(domain, fields, offset, limit, order)
        print(result)
        return result