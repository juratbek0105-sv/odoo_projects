from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ServicePayment(models.Model):
    _name = "service.payment"
    _description = "Service Payment"

    name = fields.Char(string="Payment Reference", required=True)
    center_id = fields.Many2one("service.center", string="Service Center")
    order_id = fields.Many2one("service.order", string="Order", required=True, ondelete="cascade")
    customer_id = fields.Many2one("service.customer", string="Customer", compute="_compute_customer_id", store=True)
    amount = fields.Float(string="Amount", required=True)
    payment_date = fields.Date(string="Payment Date", default=fields.Date.today)
    state = fields.Selection([
        ("draft", "Qoralama"),
        ("confirmed", "Tasdiqlangan"),
        ("cancelled", "Bekor qilingan"),
    ], default="draft", required=True)
    method = fields.Selection([
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank", "Bank")
    ], string="Payment Method")

    order_total = fields.Float(string="Order Total", compute="_compute_order_total")
    order_balance_due = fields.Float(string="Order Balance Due", compute="_compute_order_balance_due")
    customer_total_payment = fields.Float(string="Customer Total Payment", compute="_compute_customer_total_payment")

    # ---- COMPUTE FIELDS ----
    @api.depends("order_id")
    def _compute_customer_id(self):
        for record in self:
            record.customer_id = record.order_id.customer_id

    @api.depends("order_id.total_amount")
    def _compute_order_total(self):
        for record in self:
            record.order_total = record.order_id.total_amount

    @api.depends("order_id.balance_due")
    def _compute_order_balance_due(self):
        for record in self:
            record.order_balance_due = record.order_id.balance_due

    @api.depends("customer_id", "state")
    def _compute_customer_total_payment(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("customer_id", "=", record.customer_id.id),
                ("state", "=", "confirmed")
            ])
            record.customer_total_payment = sum(payments.mapped("amount"))

    # ---- ACTIONS ----
    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_draft(self):
        self.write({"state": "draft"})

    # ---- VALIDATIONS ----
    @api.constrains("amount", "order_id")
    def _check_not_overpay(self):
        for record in self:
            if record.state == "confirmed":
                if record.order_id.payment_total + record.amount > record.order_id.total_amount + 1e-6:
                    raise ValidationError("Buyurtma bo‘yicha qabul qilingan pul buyurtma summasidan katta bo‘la olmaydi.")

    @api.constrains("payment_date")
    def _check_payment_date(self):
        for record in self:
            if record.payment_date and record.payment_date > fields.Date.context_today(self):
                raise ValidationError("To‘lov sanasi kelajakdagi sana bo‘la olmaydi.")

    # ---- SQL CONSTRAINTS ----
    _sql_constraints = [
        ("payment_name_uniq", "unique(name)", "To‘lov raqami takrorlanmas bo‘lishi kerak."),
    ]
