from odoo import models, fields, api
from datetime import date

from odoo.odoo.exceptions import ValidationError


class ServiceState(models.Model):
    _name = "service.state"
    _description = "Servis viloyati"

    name = fields.Char()  #viloyat nomi
    code = fields.Char() #viloyat kodi
    is_active = fields.Boolean()  #Faol viloyat

    country_id = fields.Many2one("service.country")  #davlat
    district_ids = fields.One2many("service.district", "state_id") #Tumanlar
    center_ids = fields.One2many("service.center", "state_id") #Servis markazlari

    population = fields.Integer() #Aholi soni
    area_km2 = fields.Char()
    latitude = fields.Float()  # kenglik
    longitude = fields.Float()  # Uzunlik

    district_count = fields.Integer(computed="_compute_district_count")
    center_count = fields.Integer(computed="_compute_center_count")
    technician_ids = fields.Many2many("service.technician", compute="_compute_technician_ids")
    technician_count = fields.Integer(computed="_compute_technician_count")
    active_order_ids = fields.One2many("service.order","center_id", computed="_compute_active_order_ids")
    active_order_count = fields.Integer(computed="_compute_active_order_count")
    done_order_ids = fields.One2many("service.order", "center_id" ,computed="_compute_done_order_ids")
    done_order_count = fields.Integer(computed="_compute_done_order_count")
    today_order_ids = fields.One2many("service.order", "center_id" ,computed="_compute_today_order_ids")
    today_order_count = fields.Integer(computed="_compute_today_order_count")
    total_revenue = fields.Float(compute="_compute_total_revenue", store=True)
    avg_rating = fields.Float(computed="_compute_avg_rating")
    last_order_date = fields.Date(computed="_compute_last_order_date")


    def _compute_district_count(self):
        for record in self:
            record.district_count = len(record.district_ids)

    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    def _compute_technician_ids(self):
        for record in self:
            record.technician_ids = self.env["service.technician"].search([
                ("state_id", "in", record.id)
            ])

    def _compute_technician_count(self):
        for record in self:
            record.technician_count =  len(record.technician_ids)

    def _compute_active_order_ids(self):
        for record in self:
            active_orders = self.env["service.order"].search([
                ("center_id.state_id", "in", record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = active_orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            done_orders = self.env["service.order"].search([
                ("center_id.state_id", "in", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = done_orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count =  len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            today_orders = self.env["service.orders"].search([
                ("center_id.state_id", "in", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = today_orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("state_id", "in", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            users = self.env["service.order.rating"].search([
                ("center_id.state_id", "in", record.id)
            ])
            ratings = users.mapped("score")
            record.avg_rating = sum(ratings) / len(ratings)

    def _compute_last_order_date(self):
        for record in self:
            orders_ids = self.env["service.order"].search([
                ("center_id.state_id", "in", record.id)
            ])
            last_orders = orders_ids.mapped("order_date")
            record.last_order_date = max(last_orders)


    def action_deactivate(self):
        self.write({"is_active":False})


    def action_activate(self):
        self.write({"is_active":True})

    def action_deactivate_idle_centers(self):
        for record in self:
            idle_centers = self.env["service.center"].search([
                ("state_id", "in", record.id),
                (record.active_order_count, "=", 0)
            ])
            idle_centers.write({"is_active":False})

    def action_cleanup_zero_payments(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("order_id.center_id.state_id", "in", record.id),
                ("amount", "=", 0)
            ])
            payments.unlink()

    def action_finish_all_in_progress(self):
        for record in self:
            in_progress = self.env("service.order").search([
                ("center_id.state_id", "in", record.id),
                ("state", "=", "in_progress")
            ])
            in_progress.write({"state":"done"})


    @api.constrains("population", "area_km2")
    def check_positive(self):
        for record in self:
            if record.population < 0:
                raise ValidationError("Aholi soni musbat bo'lishi kerak")
            if record.area_km2 < 0:
                raise ValidationError("Maydon musbat bo'lishi kerak")