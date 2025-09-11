from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class ServiceState(models.Model):
    _name = "service.state"
    _description = "Servis viloyati"

    name = fields.Char(required=True)
    code = fields.Char()
    is_active = fields.Boolean(default=True)

    country_id = fields.Many2one("service.country", string="Country")
    district_ids = fields.One2many("service.district", "state_id")
    center_ids = fields.One2many("service.center", "state_id")

    population = fields.Integer()
    area_km2 = fields.Float()
    latitude = fields.Float()
    longitude = fields.Float()

    district_count = fields.Integer(compute="_compute_district_count")
    center_count = fields.Integer(compute="_compute_center_count")
    technician_ids = fields.Many2many("service.technician", compute="_compute_technician_ids")
    technician_count = fields.Integer(compute="_compute_technician_count")

    active_order_ids = fields.Many2many("service.order", compute="_compute_active_order_ids")
    active_order_count = fields.Integer(compute="_compute_active_order_count")
    done_order_ids = fields.Many2many("service.order", compute="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")
    today_order_ids = fields.Many2many("service.order", compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")
    total_revenue = fields.Float(compute="_compute_total_revenue")
    avg_rating = fields.Float(compute="_compute_avg_rating")
    last_order_date = fields.Date(compute="_compute_last_order_date")

    # ================= Compute Methods =================
    def _compute_district_count(self):
        for record in self:
            record.district_count = len(record.district_ids)

    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    def _compute_technician_ids(self):
        for record in self:
            record.technician_ids = self.env["service.technician"].search([("state_id", "=", record.id)])

    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    def _compute_active_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.state_id", "=", record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.state_id", "=", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env["service.order"].search([
                ("center_id.state_id", "=", record.id),
                ("order_date", "=", date.today())
            ])

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("order_id.center_id.state_id", "=", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env["service.order.rating"].search([
                ("center_id.state_id", "=", record.id)
            ])
            scores = ratings.mapped("score")
            record.avg_rating = sum(scores)/len(scores) if scores else 0.0

    def _compute_last_order_date(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.state_id", "=", record.id)
            ])
            dates = orders.mapped("order_date")
            record.last_order_date = max(dates) if dates else False

    # ================= Actions =================
    def action_activate(self):
        self.write({"is_active": True})

    def action_deactivate(self):
        self.write({"is_active": False})

    def action_deactivate_idle_centers(self):
        for record in self:
            idle_centers = self.env["service.center"].search([
                ("state_id", "=", record.id),
                ("id", "not in", record.active_order_ids.mapped("center_id").ids)
            ])
            idle_centers.write({"is_active": False})

    def action_cleanup_zero_payments(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("order_id.center_id.state_id", "=", record.id),
                ("amount", "=", 0)
            ])
            payments.unlink()

    def action_finish_all_in_progress(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.state_id", "=", record.id),
                ("state", "=", "in_progress")
            ])
            orders.write({"state": "done"})

    # ================= Constraints =================
    @api.constrains("population", "area_km2")
    def _check_positive_values(self):
        for record in self:
            if record.population < 0:
                raise ValidationError("Aholi soni musbat bo'lishi kerak")
            if record.area_km2 < 0:
                raise ValidationError("Maydon musbat bo'lishi kerak")
