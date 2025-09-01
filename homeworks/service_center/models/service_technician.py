from odoo import models, fields
from datetime import date

from odoo.odoo.addons.test_convert.tests.test_env import record


class ServiceDistrict(models.Model):
    _name = "service.technician"
    _description = "Servis ustalari"

    name = fields.Char(required=True)
    code = fields.Char()
    is_active = fields.Boolean()
    center_id = fields.Many2one("service.center")
    phone = fields.Char()
    email = fields.Char()
    specialty = fields.Char()
    hire_date = fields.Date()
    capacity_per_day = fields.Integer()

    order_ids = fields.One2many("service.order")
    order_count = fields.Integer(computed="_compute_order_count")
    active_order_ids = fields.Many2many(computed="_compute_active_order_ids")
    active_order_count = fields.Integer(compute = "compute_active_order_count")
    done_order_ids = fields.Many2many(computed="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="compute_done_order_count")
    today_order_ids = fields.Many2many(computed="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")
    utilization_rate = fields.Char(compute="_compute_utilization_rate")
    avg_rating = fields.Float(computed="_compute_avg_rating")
    total_revenue = fields.Char(computed="_compute_total_revenue")
    last_order_date = fields.Date(computed="_compute_last_order_date")
    is_busy  = fields.Boolean(compute="_compute_is_busy" ,required=True)

    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def _compute_active_order_ids(self):
        for record in self:
            active_orders = self.env["service.order"].search([
                ("technician_id", "in" , record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = active_orders

    def compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            done_orders = self.env["service.order"].search([
                ("technician_id", "in", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = done_orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            today_orders = self.env["service.order"].search([
                ("technician_id", "in", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = today_orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_utilization_rate(self):
        for record in self:
            record.utilization_rate = record.active_order_count / record.capacity_per_day *100

    def _compute_avg_rating(self):
        for record in self:
            rating = self.env["service.order.rating"].search([
                ("technician_id", "in", record.id)
            ])
            scores = rating.mapped("score")
            record.avg_rating = sum(scores) / len(scores)

    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("technician_id", "in", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_last_order_date(self):
        for record in self:
            last_orders = self.env["service.order"].search([
                ("technician_id", "in", record.id)
            ])
            order_dates = last_orders.mapped("order_date")
            record.last_order_date = max(order_dates)

    def _compute_is_busy(self):
        for record in self:
            if record.active_order_count == record.capacity_per_day or record.active_order_count > record.capacity_per_day:
                self.write({"is_busy":True})
            else:
                self.write({"is_busy":False})




    def action_deactivate(self):
        self.write({"is_active":False})


    def action_deactivate(self):
        self.write({"is_active":True})




