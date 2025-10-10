from odoo import models, fields, api
from odoo.exceptions import ValidationError

class OrderLine(models.Model):
    _name = "fast.food.order.line"
    _description = "Order Line"

    order_id = fields.Many2one("fast.food.order", string="Order", required=True)
    product_id = fields.Many2one("fast.food.product", string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=1)
    currency_id = fields.Many2one('res.currency',string='Currency',)
    price_unit = fields.Monetary(string="Unit Price",default=0.0)
    subtotal = fields.Monetary(string="Subtotal",compute="_compute_subtotal",store=True)
    payment_id = fields.Many2one("fast.food.payment")

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for record in self:
            price = record.price_unit or 0
            qty = record.quantity or 0
            record.subtotal = price * qty

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.price
            self._compute_subtotal()

    @api.constrains("quantity", "price_unit")
    def _check_positive_values(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Product quantity should be positive.")
            if record.price_unit <= 0:
                raise ValidationError("Product price should be positive.")
