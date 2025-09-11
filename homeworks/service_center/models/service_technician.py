from odoo import models, fields, api
from datetime import date

class ServiceTechnician(models.Model):
    _name = "service.technician"
    _description = "Servis Ustasi"

    name = fields.Char(required=True)
    code = fields.Char()
    is_active = fields.Boolean(default=True)

    center_id = fields.Many2one("service.center", string="Service Center")
    country_id = fields.Many2one("service.country")
    phone = fields.Char()
    email = fields.Char()
    specialty = fields.Char()
    hire_date = fields.Date()
    capacity_per_day = fields.Integer(default=5)

    # ================= Orders =================
    order_ids = fields.One2many("service.order", "technician_id")
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
    utilization_rate = fields.Float(compute="_compute_utilization_rate")
    is_busy = fields.Boolean(compute="_compute_is_busy")

    # ================= Compute Methods =================
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def _compute_active_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("technician_id", "=", record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("technician_id", "=", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("technician_id", "=", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("order_id.technician_id", "=", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env["service.order.rating"].search([
                ("technician_id", "=", record.id)
            ])
            scores = ratings.mapped("score")
            record.avg_rating = sum(scores)/len(scores) if scores else 0.0

    def _compute_last_order_date(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("technician_id", "=", record.id)
            ])
            dates = orders.mapped("order_date")
            record.last_order_date = max(dates) if dates else False

    def _compute_utilization_rate(self):
        for record in self:
            if record.capacity_per_day:
                record.utilization_rate = (record.active_order_count / record.capacity_per_day) * 100
            else:
                record.utilization_rate = 0.0

    def _compute_is_busy(self):
        for record in self:
            record.is_busy = record.active_order_count >= record.capacity_per_day

    # ================= Actions =================
    def action_activate(self):
        self.write({"is_active": True})

    def action_deactivate(self):
        self.write({"is_active": False})
