from odoo import models, fields

class KitchenDisplayLine(models.TransientModel):
    _name = "fast.food.kitchen.display.line"
    _description = "Kitchen Display Line"

    display_id = fields.Many2one("fast.food.kitchen.display", string="Display")
    product_id = fields.Many2one("fast.food.product", string="Product", required=True)
    quantity = fields.Integer(string="Quantity", default=0)