from odoo import models, fields

class Category(models.Model):
    _name = "rental.category"
    _description = "Category"

    name = fields.Char(required=True)
    product_ids = fields.One2many("rental.product", "category_id", string="Products")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Category name must be unique!')
    ]

