from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = "rental.product"
    _description = "Product"

    name = fields.Char(required=True)
    availability = fields.Selection([
        ('rented', 'Rented'),
        ('available', 'Available')
    ], default="available")
    broken = fields.Boolean(default=False)
    future_availability_date = fields.Datetime()
    category_id = fields.Many2one("rental.category")

    rental_price_ids = fields.One2many("rental.price", "product_id", string="Rental Prices")
    rental_order_ids = fields.One2many("rental.order", "product_id", string="Rental Orders")


    @api.constrains('broken')
    def check_broken(self):
        for record in self:
            if record.broken and record.availability == "rented":
                raise ValidationError("Broken products cannot be rented.")

    @api.constrains('future_availability_date')
    def check_future_availability_date(self):
        for record in self:
            if record.future_availability_date and record.future_availability_date < fields.Datetime.now():
                raise ValidationError("Future availability date cannot be in the past")
