from odoo import models, fields, api
from datetime import date

class ServiceCountry(models.Model):
    _name = "service.country"
    _description = "Servis davlati"

    name = fields.Char(required=True)
    code = fields.Integer()
    phone_code = fields.Char()
    is_active = fields.Boolean(default=True)

    state_ids = fields.One2many("service.state", "country_id")
    district_ids = fields.One2many("service.district", "country_id")
    center_ids = fields.One2many("service.center", "country_id")
    technician_ids = fields.One2many("service.technician", "country_id")

    technician_count = fields.Integer(compute="_compute_technician_count")
    state_count = fields.Integer(compute="_compute_state_count")
    center_count = fields.Integer(compute="_compute_center_count")
    active_order_ids = fields.Many2many("service.order", compute="_compute_active_order_ids")
    active_order_count = fields.Integer(compute="_compute_active_order_count")
    done_order_ids = fields.Many2many("service.order", compute="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")
    today_order_ids = fields.Many2many("service.order", compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")
    total_revenue = fields.Float(compute="_compute_total_revenue")
    avg_rating = fields.Float(compute="_compute_avg_rating")
    last_order_date = fields.Date(compute="_compute_last_order_date")

    def _compute_technician_count(self):
        for rec in self:
            rec.technician_count = len(rec.technician_ids)

    def _compute_state_count(self):
        for rec in self:
            rec.state_count = len(rec.state_ids)

    def _compute_center_count(self):
        for rec in self:
            rec.center_count = len(rec.center_ids)

    def _compute_active_order_ids(self):
        for rec in self:
            orders = self.env["service.order"].search([
                ("center_id.country_id", "=", rec.id),
                ("state", "in", ["received","diagnosed","in_progress"])
            ])
            rec.active_order_ids = orders

    def _compute_active_order_count(self):
        for rec in self:
            rec.active_order_count = len(rec.active_order_ids)

    def _compute_done_order_ids(self):
        for rec in self:
            orders = self.env["service.order"].search([
                ("center_id.country_id", "=", rec.id),
                ("state", "=", "done")
            ])
            rec.done_order_ids = orders

    def _compute_done_order_count(self):
        for rec in self:
            rec.done_order_count = len(rec.done_order_ids)

    def _compute_today_order_ids(self):
        today = date.today()
        for rec in self:
            orders = self.env["service.order"].search([
                ("center_id.country_id", "=", rec.id),
                ("order_date", "=", today)
            ])
            rec.today_order_ids = orders

    def _compute_today_order_count(self):
        for rec in self:
            rec.today_order_count = len(rec.today_order_ids)

    def _compute_total_revenue(self):
        for rec in self:
            payments = self.env["service.payment"].search([
                ("order_id.center_id.country_id", "=", rec.id),
                ("state", "=", "confirmed")
            ])
            rec.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for rec in self:
            ratings = self.env["service.order.rating"].search([
                ("center_id.country_id", "=", rec.id)
            ])
            scores = ratings.mapped("score")
            rec.avg_rating = sum(scores)/len(scores) if scores else 0

    def _compute_last_order_date(self):
        for rec in self:
            orders = self.env["service.order"].search([
                ("center_id.country_id", "=", rec.id)
            ])
            dates = orders.mapped("order_date")
            rec.last_order_date = max(dates) if dates else False

    def action_activate(self):
        self.is_active = True

    def action_deactivate(self):
        self.is_active = False

    def action_deactivate_empty_centers(self):
        for record in self:
            centers = self.env["service.center"].search([
                ("country_id", "=", record.id),
                ("id", "not in", record.active_order_ids.mapped("center_id").ids)
            ])
            centers.write({"is_active": False})

    def action_cleanup_zero_payments(self):
        for record in self:
            zero_payments = self.env["service.payment"].search([
                ("center_id.country_id", "=", record.id),
                ("amount", "=", 0)
            ])
            zero_payments.unlink()

    def action_finish_in_progress_orders(self):
        for record in self:
            in_progress_orders = self.env["service.order"].search([
                ("center_id.country_id", "=", record.id),
                ("state", "=", "in_progress")
            ])
            in_progress_orders.write({"state": "done"})

    _sql_constraints = [
        ("country_name_uniq", "unique(name)", "Davlat nomi takrorlanmasligi kerak"),
        ("country_code_uniq", "unique(code)", "Davlat kodi takrorlanmas bo‘lishi kerak")
    ]
