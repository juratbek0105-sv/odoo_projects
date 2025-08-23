from odoo import models, fields


class Book(models.Model):
    _name = "ecommercy.book"
    _description = "Book"

    name = fields.Char()