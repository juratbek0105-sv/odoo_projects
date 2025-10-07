# -*- coding: utf-8 -*-
# from odoo import http


# class Ecommercy2(http.Controller):
#     @http.route('/ecommercy2/ecommercy2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecommercy2/ecommercy2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecommercy2.listing', {
#             'root': '/ecommercy2/ecommercy2',
#             'objects': http.request.env['ecommercy2.ecommercy2'].search([]),
#         })

#     @http.route('/ecommercy2/ecommercy2/objects/<model("ecommercy2.ecommercy2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecommercy2.object', {
#             'object': obj
#         })

