# -*- coding: utf-8 -*-
# from odoo import http


# class Src/homeworks/odooLog(http.Controller):
#     @http.route('/src/homeworks/odoo_log/src/homeworks/odoo_log', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/src/homeworks/odoo_log/src/homeworks/odoo_log/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('src/homeworks/odoo_log.listing', {
#             'root': '/src/homeworks/odoo_log/src/homeworks/odoo_log',
#             'objects': http.request.env['src/homeworks/odoo_log.src/homeworks/odoo_log'].search([]),
#         })

#     @http.route('/src/homeworks/odoo_log/src/homeworks/odoo_log/objects/<model("src/homeworks/odoo_log.src/homeworks/odoo_log"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('src/homeworks/odoo_log.object', {
#             'object': obj
#         })

