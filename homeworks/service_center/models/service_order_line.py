from odoo import models, fields

class ServiceOrderLine(models.Model):

    _name = "service.order.line"
    _description = "Service order line"

    order_id = fields.Many2one("service.order")
    part_id = fields.Many2one("service.part")
    description = fields.Char()
    note = fields.Char()