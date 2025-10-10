from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = "fast.food.product"
    _description = "Product"

    name = fields.Char(string="Product Name", required=True)
    image = fields.Image(max_width=1920, max_height=1920)
    description = fields.Char()
    currency_id = fields.Many2one('res.currency', string='Currency')
    price = fields.Monetary(string="Price", currency_field='currency_id', required=True)
    category_id = fields.Many2one("fast.food.category", string="Category")
    order_line_ids = fields.One2many("fast.food.order.line", "product_id", string="Order Lines")

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Price should be positive")
