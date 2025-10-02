from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RentalPrice(models.Model):
    _name = "rental.price"
    _description = "Rental Price"

    _interval_map = {
        'hour': 1,
        'day': 24,
        'week': 24 * 7,
        'month': 24 * 30,
        'year': 24 * 365,
    }

    product_id = fields.Many2one("rental.product", string="Product", required=True)
    interval_number = fields.Integer(default=1, required=True)
    interval_type = fields.Selection([
        ('hour','Hour'),
        ('day','Day'),
        ('week','Week'),
        ('month','Month'),
        ('year','Year'),
    ], default="hour", required=True)
    price = fields.Float(required=True)
    hour = fields.Integer(compute="_compute_hour", store=True)

    @api.depends('interval_number', 'interval_type')
    def _compute_hour(self):
        for record in self:
            if record.interval_type == "hour":
                hours = 1
            elif record.interval_type == "day":
                hours = 24
            elif record.interval_type == "week":
                hours = 24 * 7
            elif record.interval_type == "month":
                hours = 24 * 30
            else:
                hours = 24 * 365
            record.hour = record.interval_number * hours

    @api.model
    def get_min_rent_price(self, product_id, hours):
        prices = self.env["rental.price"].search([
            ("product_id", "=", product_id), ("hour", "<=", hours)
        ], order="hour asc")
        return prices[-1] if prices else None

    @api.model
    def get_max_rent_price(self, product_id, hours):
        prices = self.env["rental.price"].search([
            ("product_id", "=", product_id), ("hour", ">=", hours)
        ], order="hour asc")
        return prices[0] if prices else None

    @api.model
    def get_result_price(self, product_id, hours):
        min_rent_price = self.get_min_rent_price(product_id, hours)
        max_rent_price = self.get_max_rent_price(product_id, hours)

        if not min_rent_price and not max_rent_price:
            raise ValidationError("Ushbu mahsulot uchun narx jadvali topilmadi.")

        if not min_rent_price:
            return max_rent_price.price

        if not max_rent_price:
            return min_rent_price.price * (hours / min_rent_price.hour)

        price_by_min = min_rent_price.price * (hours / min_rent_price.hour)
        price_by_max = max_rent_price.price
        return min(price_by_min, price_by_max)

    _sql_constraints = [
        ('unique_price_per_interval', 'unique(product_id, interval_number, interval_type)',
         'A product can have only one price per interval type and number!')
    ]

    @api.constrains('interval_number')
    def check_interval_number(self):
        for record in self:
            if record.interval_number <= 0:
                raise ValidationError("Interval number must be greater than 0")

    @api.constrains('price')
    def check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Price must be greater than 0")
