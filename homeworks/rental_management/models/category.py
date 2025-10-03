from odoo import models, fields

class Category(models.Model):
    _name = "rental.category"
    _description = "Category"
    _order = "name asc"

    name = fields.Char(required=True)
    description = fields.Text()
    product_ids = fields.One2many("rental.product", "category_id", string="Products")
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Category name must be unique!')
    ]

