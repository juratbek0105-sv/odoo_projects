from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Payment(models.Model):
    _name = "fast.food.payment"
    _description = "Payment"

    order_id = fields.Many2one("fast.food.order", string="Order")
    order_line_ids = fields.One2many("fast.food.order.line", "payment_id")
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('click', 'Click')
    ])
    currency_id = fields.Many2one('res.currency',string='Currency',)
    amount = fields.Monetary(string="Total Paid Amount", required=True)
    payment_time = fields.Datetime(string="Payment Time", readonly=True)
    status = fields.Selection([
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('cancelled', 'Cancelled')
    ], compute="_compute_status", store=True)

    @api.depends("amount", "order_id.total_amount")
    def _compute_status(self):
        for record in self:
            if record.amount >= record.order_id.total_amount:
                record.status = 'paid'
                record.payment_time = fields.Datetime.now()
            elif 0 < record.amount < record.order_id.total_amount:
                record.status = 'partial'
                record.payment_time = False
            else:
                record.status = 'cancelled'
                record.payment_time = False

    @api.constrains("amount")
    def _check_amount_positive(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError("Payment amount should be positive.")

    @api.constrains("order_id", "amount")
    def _check_payment_does_not_exceed_total(self):
        for record in self:
            if record.order_id:
                total_paid = sum(p.amount for p in record.order_id.payment_ids if p.id != record.id and p.status != 'cancelled')
                if total_paid + record.amount > record.order_id.total_amount:
                    raise ValidationError(
                        f"Paid amount more than total price!\n"
                        f"Total amount: {record.order_id.total_amount}, Paid: {total_paid}"
                    )

    def action_cancel_payment(self):
        for record in self:
            record.status = 'cancelled'
            record.amount = 0.0
            record.payment_time = False
