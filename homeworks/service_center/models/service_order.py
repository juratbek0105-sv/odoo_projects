from odoo import models, fields, api
from odoo.odoo.exceptions import ValidationError


class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Service Order"

    name = fields.Char(required=True)
    center_id = fields.Many2one("service.center")
    customer_id = fields.Many2one("service.customer")
    technician_id = fields.Many2one("service.technician")
    order_date = fields.Date()
    state = fields.Selection([
        ('draft', 'Qoralama'),
        ('received', 'Qabul qilingan'),
        ('diagnosed', 'Tashxis qo‘yilgan'),
        ('in_progress', 'Jarayonda'),
        ('done', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan')
    ], default="draft", required=True)
    description = fields.Text()
    line_ids = fields.One2many("service.order.line")
    labor_fee = fields.Float()
    discount_amount = fields.Float()

    payment_ids = fields.One2many("service.payment", compute="_compute_payment_ids")
    payment_total = fields.Float(computed="_compute_payment_total")
    balance_due = fields.Float(computed="_computed_balance_due")
    last_payment_date = fields.Date(computed="_compute_last_payment_date")
    rating_ids = fields.One2many("service.order.rating", compute="_compute_rating_ids")
    total_amount = fields.Float(computed="_compute_total_amount")
    is_warranty = fields.Boolean()
    warranty_days = fields.Integer()

    def _compute_payment_ids(self):
        for record in self:
            record.payments_ids = self.env["service.order"].search([
                ("order_id", "in", record.id)
            ])

    def _compute_payment_total(self):
        for record in self:
            payments = self.env["service.payment"].search([
                ("order_id", "in", record.id),
                ("state", "=", "confirmed")
            ])
            payments_amount = payments.mapped("amount")
            record.payment_total = sum(payments_amount)


    def _computed_balance_due(self):
        for record in self:
            record.balance_due = record.total_amount - record.payment_total

    def _compute_last_payment_date(self):
        for record in self:
            last_payments = self.env["service.payment"].search([
                ("order_id", "in", record.id)
            ])
            last_payments_date = last_payments.mapped("payment_date")
            record.last_payment_date = max(last_payments_date)

    def _compute_rating_ids(self):
        for record in self:
            ratings = self.env["service.order.rating"].search([
                ("order_id", "in", record.id)
            ])
            record.rating_ids = [
                Command.set(ratings)
            ]

    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.labor_fee - record.discount_amount

    def action_receive(self):
        self.write({"state":"received"})

    def action_diagnose(self):
        self.write({"state":"diagnosed"})

    def action_start_progress(self):
        self.write({"state":"in_progress"})

    def action_finish(self):
        for record in self:
            if record.balance_due <= 0:
                self.write({"state":"done"})
            else:
                raise ValueError("Buyurtma yakunlanmadi, qardorlik mavzud")

    def action_cancel(self):
        self.write({"state":"cancelled"})


    def action_cleanup_zero_payments(self):
        for record in self:
            zero_payments = self.env["service.payment"].search([
                ("order_id", "in", record.id),
                ("amount", "=", 0)
            ])
            zero_payments.unlink()


    def action_close_if_paid(self):
        for record in self:
            if record.balance_due <= 0:
                self.write({"state":"done"})

    @api.constains("is_warranty", "warranty_days")
    def _check_warranty(self):
        for record in self:
            if record.is_warranty and not record.warranty_days:
                raise ValidationError("Kafolat kuni kiritilishi kerak")


