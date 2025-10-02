# -*- coding: utf-8 -*-
# from odoo import http


# class RentalManagement(http.Controller):
#     @http.route('/rental_management/rental_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rental_management/rental_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rental_management.listing', {
#             'root': '/rental_management/rental_management',
#             'objects': http.request.env['rental_management.rental_management'].search([]),
#         })

#     @http.route('/rental_management/rental_management/objects/<model("rental_management.rental_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rental_management.object', {
#             'object': obj
#         })

