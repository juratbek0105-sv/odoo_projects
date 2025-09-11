from odoo import models, fields, api

class ServiceOrderLine(models.Model):
    _name = "service.order.line"
    _description = "Service Order Line"

    order_id = fields.Many2one(
        "service.order",
        string="Order",
        required=True,
        ondelete="cascade"
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product/Service"
    )
    quantity = fields.Float(default=1.0)
    price_unit = fields.Float()
    subtotal = fields.Float(
        compute="_compute_subtotal",
        store=True
    )

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
