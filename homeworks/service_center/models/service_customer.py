from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class ServiceCustomer(models.Model):
    _name = "service.customer"
    _description = "Servis Mijozi"

    name = fields.Char(required=True)
    code = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    address = fields.Char()

    # ================= Orders =================
    order_ids = fields.One2many("service.order", "customer_id", string="Orders")
    order_count = fields.Integer(compute="_compute_order_count")

    active_order_ids = fields.One2many("service.order", "customer_id", compute="_compute_active_order_ids")
    active_order_count = fields.Integer(compute="_compute_active_order_count")

    done_order_ids = fields.One2many("service.order", "customer_id", compute="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")

    today_order_ids = fields.One2many("service.order", "customer_id", compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")

    total_payment = fields.Float(compute="_compute_total_payment")
    balance_due = fields.Float(compute="_compute_balance_due")
    avg_rating = fields.Float(compute="_compute_avg_rating")
    last_order_date = fields.Date(compute="_compute_last_order_date")
    last_payment_date = fields.Date(compute="_compute_last_payment_date")

    # ================= Compute Methods =================
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def _compute_active_order_ids(self):
        for record in self:
            orders = self.order_ids.filtered(lambda o: o.state in ["received", "diagnosed", "in_progress"])
            record.active_order_ids = orders

    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            orders = self.order_ids.filtered(lambda o: o.state == "done")
            record.done_order_ids = orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            orders = self.order_ids.filtered(lambda o: o.order_date == date.today())
            record.today_order_ids = orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_payment(self):
        for record in self:
            confirmed_payments = sum(record.order_ids.mapped("payment_total"))
            record.total_payment = confirmed_payments

    def _compute_balance_due(self):
        for record in self:
            balances = sum(record.order_ids.mapped("balance_due"))
            record.balance_due = balances

    def _compute_avg_rating(self):
        for record in self:
            ratings = record.order_ids.mapped("rating_ids.score")
            record.avg_rating = sum(ratings)/len(ratings) if ratings else 0.0

    def _compute_last_order_date(self):
        for record in self:
            dates = record.order_ids.mapped("order_date")
            record.last_order_date = max(dates) if dates else False

    def _compute_last_payment_date(self):
        for record in self:
            payments = record.order_ids.mapped("payment_ids.payment_date")
            record.last_payment_date = max(payments) if payments else False

    # ================= Actions =================
    def action_close_debt(self):
        for record in self:
            for order in record.order_ids.filtered(lambda o: o.balance_due > 0):
                self.env["service.payment"].create({
                    "order_id": order.id,
                    "amount": order.balance_due,
                    "state": "confirmed",
                    "method": "cash",
                    "payment_date": date.today()
                })

    def action_cleanup_zero_payments(self):
        zero_payments = self.env["service.payment"].search([
            ("order_id.customer_id", "=", self.id),
            ("amount", "<=", 0)
        ])
        zero_payments.unlink()

    def action_cleanup_cancelled_orders(self):
        cancelled_orders = self.order_ids.filtered(lambda o: o.state == "cancelled")
        cancelled_orders.unlink()
