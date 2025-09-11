from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class ServiceCenter(models.Model):
    _name = "service.center"
    _description = "Servis markazi"

    name = fields.Char(required=True)
    code = fields.Char()
    is_active = fields.Boolean(default=True)

    country_id = fields.Many2one("service.country", string="Country")
    state_id = fields.Many2one("service.state", string="State")
    district_id = fields.Many2one("service.district", string="District")
    payment_ids = fields.One2many("service.payment", "center_id")
    service_order_rating_ids = fields.One2many("service.order.rating", "center_id")

    technician_ids = fields.One2many("service.technician", "center_id")
    technician_count = fields.Integer(compute="_compute_technician_count")

    order_ids = fields.One2many("service.order", "center_id")
    order_count = fields.Integer(compute="_compute_order_count")
    active_order_ids = fields.Many2many("service.order", compute="_compute_active_order_ids")
    active_order_count = fields.Integer(compute="_compute_active_order_count")
    done_order_ids = fields.Many2many("service.order", compute="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")
    today_order_ids = fields.Many2many("service.order", compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")

    total_revenue = fields.Float(compute="_compute_total_revenue")
    avg_rating = fields.Float(compute="_compute_avg_rating")
    last_order_date = fields.Date(compute="_compute_last_order_date")

    latitude = fields.Float()
    longitude = fields.Float()
    address = fields.Char()
    phone = fields.Char()
    email = fields.Char()

    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def _compute_active_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id", "=", record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id", "=", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id", "=", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("center_id", "=", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env["service.order.rating"].search([
                ("center_id", "=", record.id)
            ])
            scores = ratings.mapped("score")
            record.avg_rating = sum(scores)/len(scores) if scores else 0.0

    def _compute_last_order_date(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id", "=", record.id)
            ])
            dates = orders.mapped("order_date")
            record.last_order_date = max(dates) if dates else False

    # ================= Actions =================
    def action_activate(self):
        self.write({"is_active": True})

    def action_deactivate(self):
        self.write({"is_active": False})

    def action_cleanup_zero_payments(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("center_id", "=", record.id),
                ("amount", "=", 0)
            ])
            payments.unlink()

    def action_finish_all_in_progress(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id", "=", record.id),
                ("state", "=", "in_progress")
            ])
            orders.write({"state": "done"})

    # ================= Constraints =================
    @api.constrains("latitude", "longitude")
    def _check_coordinates(self):
        for record in self:
            if record.latitude and (record.latitude < -90 or record.latitude > 90):
                raise ValidationError("Latitude must be between -90 and 90")
            if record.longitude and (record.longitude < -180 or record.longitude > 180):
                raise ValidationError("Longitude must be between -180 and 180")
