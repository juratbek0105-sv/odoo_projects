from odoo import models, fields
from datetime import date


class ServiceDistrict(models.Model):
    _name = "service.customer"
    _description = "Servis Mijozi"

    name = fields.Char(required=True)
    code = fields.Char()
    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    address = fields.Char()

    center_ids = fields.Many2many("service.center","customer_id", compute="_compute_center_ids")
    order_ids = fields.One2many("service.order")
    payment_ids = fields.One2many("service.payment")
    rating_ids = fields.One2many("service.order.rating")

    order_count = fields.Integer(compute="compute_order_count")
    active_order_ids = fields.One2many("service.order", "customer_id",computed="_compute_active_order_ids")
    active_order_count = fields.Integer(compute="compute_active_order_count")
    done_order_ids = fields.One2many("service.order", "customer_id",compute="_compute_done_order_ids")
    done_order_count = fields.Integer(compute="_compute_done_order_count")
    today_order_ids = fields.One2many("service.order", "customer_id",compute="_compute_today_order_ids")
    today_order_count = fields.Integer(compute="_compute_today_order_count")
    total_payment = fields.Char(computed="_compute_total_payment")
    balance_due = fields.Char(compute="_compute_balance_due")
    avg_rating = fields.Float(computed="_compute_avg_rating")
    last_order_date = fields.Date(computed="_compute_last_order_date")
    last_payment_date = fields.Date(compute="_compute_last_payment_date")

    def _compute_center_ids(self):
        for record in self:
            record.center_ids = [
                Command.set(record.order_ids.mapped("center_id"))
            ]

    def compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)

    def _compute_active_order_ids(self):
        for record in self:
            active_orders = self.env["service.order"].search([
                ("customer_id", "in", record.id),
                ("state", "in", ["received", "diagnosed", "in_progress"])
            ])
            record.active_order_ids = active_orders

    def compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    def _compute_done_order_ids(self):
        for record in self:
            done_orders = self.env["service.orders"].search([
                ("customer_id", "in", record.id),
                ("state", "=", "done")
            ])
            record.done_order_ids = done_orders

    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    def _compute_today_order_ids(self):
        for record in self:
            today_orders = self.env["service.order"].search([
                ("customer_id", "in", record.id),
                ("order_date", "=", date.today())
            ])
            record.today_order_ids = today_orders

    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    def _compute_total_payment(self):
        for record in self:
            total_payments = self.env["service.payments"].search([
                ("customer_id", "in", record.id)
            ])
            record.total_payments = sum(total_payments.mapped("total_amount"))

    def _compute_balance_due(self):
        for record in self:
            orders = self.env["service.order"].search([
                ("customer_id", "in", record.id)
            ])
            record.balance_due = sum(orders.mapped("balance_due"))

    def _compute_avg_rating(self):
        for record in self:
            with_orders = self.env["service.order"].search([
                ("customer_id", "in", record.id),
                ("rating", "!=", False)
            ])
            ratings = with_orders.mapped("rating")
            record.avg_rating = sum(ratings) / len(ratings)

    def _compute_last_order_date(self):
        for record in self:
            last_orders = self.env["service.order"].search([
                ("customer_id", "in", record.id)
            ])
            last_orders_dates = last_orders.mapped("order_date")
            record.last_order_date = max(last_orders_dates)

    def _compute_last_payment_date(self):
        for record in self:
            last_payments = self.env["service.payment"].search([
                ("customer_id", "in", record.id)
            ])
            last_payments_date = last_payments.mapped("payment_date")
            record.last_payment_date = max(last_payments_date)



    def action_close_debt(self):
        for record in self:
            orders = self.env["service.payment"].search([
                ("customer_id", "in", record.id),
                ("balance_due", ">", 0)
            ])
            for order in orders:
                self.env["service.payment"].create({
                    "order_id": order.id,
                    "amount": order.balance_due,
                    "state": "confirmed",
                    "method": "cash",
                    "note": "Auto payment to close debt"
                })


    def action_cleanup_zero_payments(self):
        for record in self:
            zero_payments = self.env["service.amount"].search([
                ("customer_id", "in", record.id),
                ("amount", "<=", 0)
            ])
            zero_payments.unlink()


    def action_cleanup_cancelled_orders(self):
        for record in self:
            cancelled_orders = self.env["service.orders"].search([
                ("customer_id", "in", record.id),
                ("state", "=", "cancelled")
            ])
            cancelled_orders.unlink()




