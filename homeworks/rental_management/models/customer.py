from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Customer(models.Model):
    _name = "rental.customer"
    _description = "Customer"
    _order = "name asc"

    name = fields.Char(required=True)
    phone = fields.Char()
    email = fields.Char()
    rental_orders = fields.One2many("rental.order", "customer_id", string="Rental Orders")
    rental_order_count = fields.Integer(compute="_compute_order_count", store=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'Email must be unique!'),
    ]

    @api.depends('rental_orders')
    def _compute_order_count(self):
        for rec in self:
            rec.rental_order_count = len(rec.rental_orders)

    @api.constrains('email')
    def check_email(self):
        for record in self:
            if record.email:
                if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', record.email):
                    raise ValidationError("Invalid email format.")

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            if record.phone and not re.match(r'^\+?\d{7,15}$', record.phone):
                raise ValidationError("Phone must be digits (7–15) and may start with +.")


