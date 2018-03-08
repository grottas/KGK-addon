# -*- coding: utf-8 -*-
from odoo import http

class Mobile(http.Controller):
#     @http.route('/mobile/mobile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mobile/mobile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mobile.listing', {
#             'root': '/mobile/mobile',
#             'objects': http.request.env['mobile.mobile'].search([]),
#         })

#     @http.route('/mobile/mobile/objects/<model("mobile.mobile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mobile.object', {
#             'object': obj
#         })

     @http.route('/mobile/pipeline_count', type='http', auth='user', methods=['GET'])
     def mobile_pipeline_count(self, res_id, token):
            try:
                record.pipeline_count()
            except Exception:
                return MailController._redirect_to_messaging()
            return redirect