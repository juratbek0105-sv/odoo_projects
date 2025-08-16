# -*- coding: utf-8 -*-
# from odoo import http


# class Clinics1(http.Controller):
#     @http.route('/clinics1/clinics1', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/clinics1/clinics1/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('clinics1.listing', {
#             'root': '/clinics1/clinics1',
#             'objects': http.request.env['clinics1.clinics1'].search([]),
#         })

#     @http.route('/clinics1/clinics1/objects/<model("clinics1.clinics1"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('clinics1.object', {
#             'object': obj
#         })

