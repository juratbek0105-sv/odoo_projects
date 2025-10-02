from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Customer(models.Model):
    _name = "rental.customer"
    _description = "Customer"

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    rental_orders = fields.One2many("rental.order", "customer_id", string="Rental Orders")

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!'),
        ("unique_customer_name", "unique(name)", "Customer name must be unique!"),
    ]

    @api.constrains('email')
    def check_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.email):
                    raise ValidationError("Invalid email format.")


    @api.constrains('phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone and not rec.phone.isdigit():
                raise ValidationError("Phone must contain only digits")


