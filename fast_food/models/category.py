from odoo import models, fields

class ProductCategory(models.Model):
    _name = "fast.food.category"
    _description = "Product Category"

    name = fields.Char(string="Category Name", required=True)
    sequence = fields.Integer()
    product_ids = fields.One2many("fast.food.product", "category_id", string="Products")
