from odoo import models, fields, api
from datetime import date

class ServiceCentre(models.Model):
    _name = "service.center"
    _description = "Servis markazi"

    name = fields.Char(required=True)  #Servis markazi nomi
    code = fields.Char() #Markaz kodi
    is_active = fields.Boolean(default=True)   #Faol markaz
    country_id = fields.Many2one("service.country")  #davlat
    state_id = fields.Many2one("service.state")  #viloyat
    district_id = fields.Many2one("service.district") #tuman
    address = fields.Char()  #manzil
    latitude = fields.Float() #kenglik
    longitude = fields.Float() #Uzunlik
    phone = fields.Char() #telefon
    email = fields.Char() #pochta
    manager_name = fields.Char() #Mas'ul shaxs
    capacity_per_day = fields.Integer() #Kunlik quvvat (buyurtma)

    order_ids = fields.One2many("service.order", "center_id") #buyurtmalar ro‘yxati
    payment_ids = fields.One2many("service.payment","center_id") #To‘lovlar
    rating_ids = fields.One2many("service.order.rating", "center_id") #Baholar

    technician_count = fields.Integer(compute="_compute_technician_count", store=True) #Ustalar soni
    active_order_ids = fields.Many2many("service.order", compute="_compute_active_order_ids") #Faol buyurtmalar
    active_order_count = fields.Integer(compute="_compute_active_order_count") #Faol buyurtmalar soni
    done_order_ids = fields.One2many("service.order", "center_id", compute="_compute_done_order_ids") #Yakunlangan buyurtmalar
    done_order_count = fields.Integer(compute="_compute_done_order_count") #Yakunlangan buyurtmalar soni
    today_order_ids = fields.One2many("service.order", "center_id", compute="_compute_today_order_ids") #Bugungi buyurtmalar
    today_order_count = fields.Integer(compute="_compute_today_order_count") #Bugungi buyurtmalar soni
    total_revenue = fields.Float(compute="_compute_total_revenue", store=True) #Jami tushum
    avg_rating = fields.Float(compute="_compute_avg_rating") #O‘rtacha baho
    utilization_rate = fields.Float(compute="_compute_utilization") #Bandlik foizi (%)
    last_order_date = fields.Date(compute="_compute_last_order_date") #Oxirgi buyurtma sanasi

    @api.depends("order_ids.technician_id")
    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.order_ids.mapped("technician_id"))

    def _compute_active_order_ids(self):
        for record in self:

            active_orders = self.env["service.order"].search([("center_id", "=", record.id), ("state", "in", ["receive","diagnosed", "in progress"])])
            active_order_ids = active_orders.ids

            record.active_order_ids = [
                Command.set(active_order_ids)
            ]


    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)



    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = record.order_ids.filtered(lambda o: o.state == "done")

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count =  len(record.done_order_ids)


    def _compute_today_order_ids(self):
        for record in self:
            record.today_order_ids = record.order_ids.filtered(lambda o: o.order_date == date.today())


    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_revenue(self):
        for record in self:
            record.total_revenue  = sum(record.payment_ids.mapped("amount"))

    def _compute_avg_rating(self):
        for record in self:
            scores  = record.rating_ids.mapped("score")
            record.avg_rating = sum(scores) / len(scores)

    def _compute_utilization(self):
        for record in self:
            record.utilization_rate = record.active_order_count / record.capacity_per_day * 100

    def _compute_last_order_date(self):
        for record in self:
            record.last_order_date = max(record.order_ids.mapped("order_date"))

    def action_mark_inactive_if_idle(self):
        for record in self:
            if not record.active_order_ids:
                record.is_active = False


    def action_activate(self):
        self.write({"is_active": True})



    def action_cleanup_zero_payments(self):
        for record in self:
            zero_payments = record.payment_ids.filtered(lambda p: p.amount == 0)
            zero_payments.unlink()


    def action_finish_all_in_progress(self):
        self.order_ids.filtered(lambda o: o.state=="in_progress").write({"state":"done"})





