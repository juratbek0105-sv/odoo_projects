from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Product(models.Model):
    _name = "rental.product"
    _inherit = "image.mixin"
    _description = "Product"

    name = fields.Char(required=True)
    availability = fields.Selection([
        ('rented', 'Rented'),
        ('available', 'Available')
    ], compute="_compute_availability", store=True)
    broken = fields.Boolean(default=False)
    future_availability_date = fields.Datetime(compute="_compute_future_availability_date", store=True)
    category_id = fields.Many2one("rental.category")
    active= fields.Boolean(default=True)

    rental_price_ids = fields.One2many("rental.price", "product_id", string="Rental Prices")
    rental_order_ids = fields.One2many("rental.order", "product_id", string="Rental Orders")



    @api.depends("rental_order_ids.end_date", "rental_order_ids.returned_date", "rental_order_ids.status")
    def _compute_future_availability_date(self):
        for record in self:
            # active rental orders not yet returned/cancelled
            active_orders = record.rental_order_ids.filtered(
                lambda o: o.status == "confirmed" and o.end_date
            )
            if active_orders:
                # take the latest end_date
                order = active_orders.sorted(key=lambda o: o.end_date, reverse=True)[0]
                # if already returned, take returned_date; else use end_date
                record.future_availability_date = order.returned_date or order.end_date
            else:
                # not rented → no future date
                record.future_availability_date = False

    @api.depends("broken", "rental_order_ids.status")
    def _compute_availability(self):
        for rec in self:
            if rec.broken:
                rec.availability = 'available'  # could also make a new state like "unusable"
            elif any(order.status == "confirmed" for order in rec.rental_order_ids):
                rec.availability = 'rented'
            else:
                rec.availability = 'available'

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
