# -*- coding: utf-8 -*-
# from odoo import http


# class Homework7(http.Controller):
#     @http.route('/homework_7/homework_7', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/homework_7/homework_7/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('homework_7.listing', {
#             'root': '/homework_7/homework_7',
#             'objects': http.request.env['homework_7.homework_7'].search([]),
#         })

#     @http.route('/homework_7/homework_7/objects/<model("homework_7.homework_7"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('homework_7.object', {
#             'object': obj
#         })

