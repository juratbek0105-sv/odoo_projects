from odoo import models, fields, api
from datetime import date

class ServiceCountry(models.Model):
    _name = "service.countryr"
    _description = "Servis davlati"

    name = fields.Char()  #Davlat nomi
    code = fields.Integer() #davlat kodi
    phone_code = fields.Char()   # Telefon kodi
    is_active = fields.Boolean()  #Faol davlat

    state_ids = fields.One2many("service.state", "country_id") #viloyatlar    state_ids = fields.One2many("service.state") #viloyatlar
    district_ids = fields.One2many("service.district", "country_id")
    center_ids = fields.One2many("service.center", "country_id") #Servis markazlari
    technician_ids = fields.One2many("service.technician", "country_id")

    technician_count = fields.Integer(computed="_compute_technician_count") #Ustalar soni
    state_count = fields.Integer(computed="_compute_state_count") #Viloyatlar soni
    center_count = fields.Integer(computed="_compute_center_count") #Servis markazlari soni
    active_order_ids = fields.Many2many("service.order", computed="_compute_active_order_ids") #Faol buyurtmalar
    active_order_count = fields.Integer(computed="_compute_active_order_count") #Faol buyurtmalar soni
    done_order_ids = fields.Many2many("service.order", computed="_compute_done_order_ids") #  Yakunlangan buyurtmalar
    done_order_count = fields.Integer(computed="_compute_done_order_count") #  Jami tushum
    today_order_ids = fields.Many2many("service.order", "country_id", compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute = "_compute_today_order_count")
    total_revenue = fields.Char(compute="_compute_total_revenue")
    avg_rating = fields.Float(computed="_compute_avg_rating") #O'rtacha baho
    last_order_date = fields.Date(computed="_compute_last_order_date") #Oxirgi buyurtma sanasi

    def _compute_technician_count(self):
        for record in self:
            record.technician_count  = len(record.technician_ids)

    def _compute_state_count(self):
        for record in self:
            record.state_count = len(record.state_ids)



    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)


    def _compute_active_order_ids(self):
        for record in self:
            active_orders = self.env["service.order"].search([
                ("center_id.country_id", "=", record.id),
                ("state", "in", ["receive","diagnosed", "in progress"])
            ])
            active_order_ids = active_orders.ids

            record.active_order_ids = [
                Command.set(active_order_ids)
            ]
    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = record.center_ids.mapped("order_ids").filtered(lambda x: x.state == "done")

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env["service.order"].search([
                ("center_id.country_id", "in", record.id),
                ("order_date" "=", date.today())
            ])

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count  = len(record.today_order_ids)


    def _compute_total_revenue(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("center_id.country_id", "in", record.id)
            ])
            record.total_revenue = sum(payments.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env["service.order.rating"].search([
                ("center_id", "in", record.id)
            ])
            scores = ratings.mapped("score")
            record.avg_rating = sum(scores) / len(scores)

    def _compute_last_order_date(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("center_id.country_id", "in", record.id)
            ])
            dates = orders.mapped("order_date")
            record.last_order_date = max(dates)


    def action_activate(self):

        self.write({"is_active": True})


    def action_deactivate(self):

        self.write({"is_active": False})

    def action_deactivate_idle_centers(self):
        for record in self:
            idle_centers = self.env["service.center"].search([
                ("country_id", "in", record.id),
                ("id", "not in", record.active_order_ids.mapped("center_id").ids)
            ])
            idle_centers.write({"is_active":False})


    def action_cleanup_zero_payments(self):
        for record in self:
            zero_payments = self.env["service.payments"].search([
                ("order_id.center_id.country_id", "in", record.id),
                ("amount", "=", 0)
            ])
            zero_payments.unlink()

    def action_finish_all_in_progress(self):
        for record in self:
            in_proggress_orders = self.env["service.order"].search([
                ("center_id.country_id", "in", record.id),
                ("state", "=", "in_progress")
            ])
            in_proggress_orders.write({"state":"done"})

    _sql_constraints = [
        ("country_name_uniq", "unique(name)", "Davlat nomi takrorlanmasligig kerak"),
        ("country_code_uniq", "unique(code)", "Davlat kodi takrorlanmas bo‘lishi kerak")
    ]