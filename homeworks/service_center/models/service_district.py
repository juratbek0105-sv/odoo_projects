from odoo import models, fields
from datetime import date

class ServiceDistrict(models.Model):
    _name = "service.district"
    _description = "Servis viloyati"

    name = fields.Char(required=True)
    code = fields.Char()
    is_active = fields.Boolean()
    state_id = fields.Many2one("service.district")
    country_id = fields.Many2one("service.country", related = "state_id.country_id", store=True)
    center_ids = fields.One2many("service.center", "district_id")
    population = fields.Integer()
    area_km2 = fields.Char()
    latitude = fields.Float()
    longitude = fields.Float()

    center_count = fields.Integer(computed="_compute_center_count")
    technician_ids = fields.One2many("service.district", "order_id", compute="_compute_technician_ids")
    technician_count = fields.Integer(computed="_compute_technician_count")
    active_order_ids = fields.Many2many(computed="_compute_active_order_ids")
    active_order_count = fields.Integer(compute = "_compute_active_order_count")
    done_order_ids = fields.Many2many(computed="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")
    today_order_ids = fields.Many2many(computed="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")
    total_revenue = fields.Char(computed="_compute_total_revenue")
    avg_rating = fields.Float(computed="_compute_avg_rating")
    last_order_date = fields.Date(computed="_compute_last_order_date")


    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    def _compute_technician_ids(self):
        for record in self:
            record.technician_ids = self.env["service.technician"].search([
                ("district_id", "in", record.id)
            ])

    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    def _compute_active_order_ids(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.district_id", "in", record.id),
                ("state", "in", ["receive","diagnosed", "in progress"])
            ])
            record.active_order_ids = orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            done_orders = self.env["service.orders"].search([
                ("center_id.district_id", "in" , record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = done_orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            today_orders = self.env["service.order"].search([
                ("center_id.district_id", "in", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = today_orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            total_revenue = self.env["service.payment"].search([
                ("center_id.district_id", "in", record.id)
            ])
            record.total_revenue = sum(total_revenue.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            orders = self.env["service.order.rating"].search([
                ("center_id.district_id", "in", record.id)
            ])
            ratings = orders.mapped("score")
            record.avg_rating = sum(ratings) / len(ratings)

    def _compute_last_order_date(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.district_id", "id", record.id)
            ])
            record.last_order_date = max(orders.mapped("order_date"))

    def action_deactivate(self):
        self.write({"is_active":False})

    def action_activate(self):
        self.write({"is_active":True})

    def action_cleanup_zero_payments(self):
        for record in self:
            payments = self.env["service.payments"].search([
                ("district_id", "in", record.id),
                ("amount", "=", 0)
            ])
            payments.unlink()

    def action_finish_all_in_progress(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.district_id", "in", record.id),
                ("state", "=", "in_progress")
            ])
            record.write({"state":"done"})

