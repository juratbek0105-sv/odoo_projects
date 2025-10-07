from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Product(models.Model):
    _name = "rental.product"
    _inherit = "image.mixin"
    _description = "Product"

    name = fields.Char(required=True)
    availability = fields.Selection([
        ('rented', 'Rented'),
        ('available', 'Available'),
        ('broken', 'Broken')
    ], compute="_compute_availability", store=True)
    broken = fields.Boolean(default=False)
    future_availability_date = fields.Datetime(compute="_compute_future_availability_date", store=True)
    category_id = fields.Many2one("rental.category")
    active= fields.Boolean(default=True)
    avg_rental_hours = fields.Float(compute="_compute_avg_rental_hours", store=True)

    rental_price_ids = fields.One2many("rental.price", "product_id", string="Rental Prices")
    rental_order_ids = fields.One2many("rental.order", "product_id", string="Rental Orders")

    def action_toggle_broken(self):
        for record in self:
            record.broken = not record.broken

    @api.depends('rental_order_ids')
    def _compute_avg_rental_hours(self):
        for record in self:
            orders = self.env["rental.order"].search([
                ("product_id" , "=", record.id),
                ("returned_date", "!=", False)
            ])
            order_hours = []
            for order in orders:
                duration = (order.returned_date - order.start_date).total_seconds() //3600
                order_hours.append(duration)
            if order_hours:
                record.avg_rental_hours = sum(order_hours) / len(order_hours)
            else:
                record.avg_rental_hours = 0


    @api.depends("rental_order_ids.end_date", "rental_order_ids.returned_date", "rental_order_ids.status")
    def _compute_future_availability_date(self):
        for record in self:
            active_orders = record.rental_order_ids.filtered(
                lambda o: o.status == "confirmed" and o.end_date
            )
            if active_orders:
                order = active_orders.sorted(key=lambda o: o.end_date, reverse=True)[0]
                record.future_availability_date = order.returned_date or order.end_date
            else:
                record.future_availability_date = False

    @api.depends('broken', 'rental_order_ids.status')
    def _compute_availability(self):
        for record in self:
            if record.broken:
                record.availability = "broken"
            elif any(order.status == "confirmed" for order in record.rental_order_ids):
                record.availability = 'rented'
            else:
                record.availability = 'available'

    @api.constrains('broken', 'availability')
    def check_broken(self):
        for record in self:
            if record.broken and record.availability != "broken":
                raise ValidationError("Broken product must always have 'Broken' availability.")

    @api.constrains('future_availability_date')
    def check_future_availability_date(self):
        for record in self:
            if record.future_availability_date and record.future_availability_date < fields.Datetime.now():
                raise ValidationError("Future availability date cannot be in the past")
