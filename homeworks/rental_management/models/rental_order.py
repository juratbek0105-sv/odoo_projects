from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RentalOrder(models.Model):
    _name = "rental.order"
    _description = "Rental Order"

    name = fields.Char(string="Order Reference", required=True, copy=False, default="New")
    customer_id = fields.Many2one("rental.customer", string="Customer", required=True)
    product_id = fields.Many2one("rental.product", string="Product", required=True)

    start_date = fields.Datetime(default=fields.Datetime.now)
    end_date = fields.Datetime()
    returned_date = fields.Datetime(readonly=True)

    duration = fields.Integer(compute="_compute_duration", store=True)
    human_readable_duration = fields.Char(compute="_compute_human_readable_duration", store=True)

    total_price = fields.Float(compute="_compute_total_price", store=True)
    complete_price = fields.Float(compute="_compute_complete_price", store=True)

    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')], default="draft")

    def action_confirm(self):
        for record in self:
            record.status = 'confirmed'
            record.product_id.availability = 'rented'
            record.product_id.future_availability_date = record.end_date

    def action_return(self):
        for record in self:
            record.status = 'returned'
            record.product_id.availability = 'available'
            record.product_id.future_availability_date = False
            record.returned_date = fields.Datetime.now()


    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                record.duration = (record.end_date - record.start_date).total_seconds() / 3600
            else:
                record.duration = 0

    @api.depends("duration")
    def _compute_human_readable_duration(self):
        for record in self:
            total_hours = record.duration
            years = total_hours // (24*365)
            remaining_hours = total_hours % (24*365)

            months = remaining_hours // (24*30)
            remaining_hours %= 24*30

            weeks = remaining_hours // (24*7)
            remaining_hours %= 24*7

            days = remaining_hours // 24
            hours = remaining_hours % 24

            text = []
            if years:
                text.append(f"{years} year(s)")
            if months:
                text.append(f"{months} month(s)")
            if weeks:
                text.append(f"{weeks} week(s)")
            if days:
                text.append(f"{days} day(s)")
            if hours or not text:
                text.append(f"{hours} hour(s)")

            record.human_readable_duration = " ".join(text)

    @api.depends("start_date", "end_date", "product_id")
    def _compute_total_price(self):
        for record in self:
            hours = (record.end_date - record.start_date).days * 24
            total_price = self.env["rental.price"].get_result_price(product_id=record.product_id.id, hours=hours)
            record.total_price = total_price

    @api.depends("returned_date", "start_date", "product_id")
    def _compute_complete_price(self):
        for record in self:
            hours = (record.returned_date - record.start_date).days * 24
            complete_price = self.env["rental.price"].get_result_price(product_id=record.product_id.id, hours=hours)
            record.complete_price =  complete_price

    @api.constrains('start_date', 'end_date')
    def check_start_end_date(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date >= record.end_date:
                    raise ValidationError("End date can not be before start date")

    @api.constrains('product_id', 'status')
    def _check_product_availability(self):
        for order in self:
            if order.status == 'confirmed':
                if order.product_id.availability != 'available' or order.product_id.broken:
                    raise ValidationError("Product is not available for rental")

    @api.constrains('product_id', 'start_date', 'end_date')
    def _check_overlap(self):
        for order in self:
            overlapping = self.search([
                ('id', '!=', order.id),
                ('product_id', '=', order.product_id.id),
                ('status', '=', 'confirmed'),
                ('start_date', '<', order.end_date),
                ('end_date', '>', order.start_date)
            ])
            if overlapping:
                raise ValidationError("This product is already rented in the selected period")
