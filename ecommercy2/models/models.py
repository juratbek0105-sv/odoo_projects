# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ecommercy2(models.Model):
#     _name = 'ecommercy2.ecommercy2'
#     _description = 'ecommercy2.ecommercy2'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

