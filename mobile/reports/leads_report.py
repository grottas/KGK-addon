# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api

class LeadReport(models.Model):
    """ adds fields to CRM Opportunity Analysis """

    _name = "crm.opportunity.report"
    _inherit = "crm.opportunity.report"
    _auto = False
    _description = "CRM Opportunity Analysis"
    _rec_name = 'date_deadline'

    product = fields.Many2one('product.product', string='Product', readonly=True)


    def _select(self):
        select_str = """
        SELECT
            c.id,
            c.date_deadline,

            c.date_open as opening_date,
            c.date_closed as date_closed,
            c.date_last_stage_update as date_last_stage_update,

            c.user_id,
            c.product,
            c.probability,
            c.stage_id,
            stage.name as stage_name,
            c.type,
            c.company_id,
            c.priority,
            c.team_id,
            (SELECT COUNT(*)
             FROM mail_message m
             WHERE m.model = 'crm.lead' and m.res_id = c.id) as nbr_activities,
            c.active,
            c.campaign_id,
            c.source_id,
            c.medium_id,
            c.partner_id,
            c.city,
            c.country_id,
            c.planned_revenue as total_revenue,
            c.planned_revenue*(c.probability/100) as expected_revenue,
            c.create_date as create_date,
            extract('epoch' from (c.date_closed-c.create_date))/(3600*24) as  delay_close,
            abs(extract('epoch' from (c.date_deadline - c.date_closed))/(3600*24)) as  delay_expected,
            extract('epoch' from (c.date_open-c.create_date))/(3600*24) as  delay_open,
            c.lost_reason,
            c.date_conversion as date_conversion
        """
        return select_str