from odoo import models, fields, api
from odoo.odoo.exceptions import ValidationError


class ServicePart(models.Model):
    _name  = "service.payment"
    _description = "Service payment"

    name = fields.Char()
    center_id  = fields.Many2one("service.center", compute="_compute_center_id")
    order_id = fields.Many2one("service.order")
    customer_id = fields.Many2one("service.customer", computed="_compute_customer_id")
    payment_date = fields.Date()
    amount = fields.Float()
    note  = fields.Text()
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled")
    ])
    method = fields.Selection([
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank", "Bank")
    ])
    order_total = fields.Char(compute="_compute_order_total")
    order_balance_due = fields.Char(compute="_compute_order_balance_due")
    customer_total_payment = fields.Char(compute="_compute_customer_total_payment")

    def _compute_center_id(self):
        for record in self:
            record.center_id = record.order_id.center_id

    def _compute_customer_id(self):
        for record in self:
            record.customer_id = record.order_id.customer_id

    def _compute_order_total(self):
        for record in self:
            record.order_total = record.order_id.total_amount

    def _compute_order_balance_due(self):
        for record in self:
            record.order_balance_due = record.order_id.balance_due

    def _compute_customer_total_payment(self):
        for record in self:
            total_payment = self.env["service.payment"].search([
                ("customer_id", "in", record.id),
                ("state", "=", "confirmed")
            ])
            record.customer_total_payment = sum(total_payment.mapped("amount"))

    def action_confirm(self):
        for record in self:
            self.state = "confirmed"

    def action_cancel(self):
        for record in self:
            self.state = "cancelled"

    def action_reset_draft(self):
        for record in self:
            self.state = "draft"

    @api.constraints("amount", "order_id")
    def check_not_overpay(self):
        for record in self:
            if record.state == "confirmed":
                if record.order_id.total_payment + record.amount > record.order_id.total_amount + 1e-6:
                    raise ValidationError("Buyurtma bo‘yicha qabul qilingan pul buyurtma summasidan katta bo‘la olmaydi.")

    @api.constrains("payment_date")
    def _check_payment_date(self):
        for rec in self:
            if rec.payment_date and rec.payment_date > fields.Date.context_today(self):
                raise ValidationError("To‘lov sanasi kelajakdagi sana bo‘la olmaydi.")


    _sql_constraints = [
        ("payment_name_uniq", "unique(name)", "To‘lov raqami takrorlanmas bo‘lishi kerak."),
    ]