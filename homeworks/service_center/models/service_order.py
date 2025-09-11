from odoo import models, fields, api
from odoo.exceptions import ValidationError


# ---------------------------
# Service Order
# ---------------------------
class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Service Order"

    name = fields.Char(required=True)
    center_id = fields.Many2one("service.center", string="Service Center")
    customer_id = fields.Many2one("service.customer", string="Customer")
    technician_id = fields.Many2one("service.technician", string="Technician")
    order_date = fields.Date(default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Qoralama'),
        ('received', 'Qabul qilingan'),
        ('diagnosed', 'Tashxis qo‘yilgan'),
        ('in_progress', 'Jarayonda'),
        ('done', 'Yakunlangan'),
        ('cancelled', 'Bekor qilingan')
    ], default='draft', required=True)
    description = fields.Text()

    line_ids = fields.One2many("service.order.line", "order_id", string="Order Lines")
    labor_fee = fields.Float(default=0.0)
    discount_amount = fields.Float(default=0.0)

    payment_ids = fields.One2many("service.payment", "order_id", string="Payments")
    payment_total = fields.Float(compute="_compute_payment_total")
    balance_due = fields.Float(compute="_compute_balance_due", store=True)
    last_payment_date = fields.Date(compute="_compute_last_payment_date")
    rating_ids = fields.One2many("service.order.rating", "order_id", string="Ratings")
    total_amount = fields.Float(compute="_compute_total_amount")

    is_warranty = fields.Boolean(default=False)
    warranty_days = fields.Integer()

    # ------------------------
    # Compute methods
    # ------------------------
    @api.depends('line_ids.quantity', 'line_ids.price_unit', 'labor_fee', 'discount_amount')
    def _compute_total_amount(self):
        for order in self:
            line_total = sum(order.line_ids.mapped('subtotal'))
            order.total_amount = line_total + order.labor_fee - order.discount_amount

    @api.depends('payment_ids.amount', 'payment_ids.state')
    def _compute_payment_total(self):
        for order in self:
            confirmed_payments = order.payment_ids.filtered(lambda p: p.state == 'confirmed')
            order.payment_total = sum(confirmed_payments.mapped('amount'))

    @api.depends('total_amount', 'payment_total')
    def _compute_balance_due(self):
        for order in self:
            order.balance_due = order.total_amount - order.payment_total

    @api.depends('payment_ids.payment_date')
    def _compute_last_payment_date(self):
        for order in self:
            dates = order.payment_ids.mapped('payment_date')
            order.last_payment_date = max(dates) if dates else False

    # ------------------------
    # Actions
    # ------------------------
    def action_receive(self):
        self.write({'state': 'received'})

    def action_diagnose(self):
        self.write({'state': 'diagnosed'})

    def action_start_progress(self):
        self.write({'state': 'in_progress'})

    def action_finish(self):
        for order in self:
            if order.balance_due <= 0:
                order.write({'state': 'done'})
            else:
                raise ValidationError("Buyurtma yakunlanmadi, qarzdorlik mavjud")

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_cleanup_zero_payments(self):
        zero_payments = self.env['service.payment'].search([
            ('order_id', 'in', self.ids),
            ('amount', '=', 0)
        ])
        zero_payments.unlink()

    @api.constrains('is_warranty', 'warranty_days')
    def _check_warranty(self):
        for order in self:
            if order.is_warranty and not order.warranty_days:
                raise ValidationError("Kafolat kuni kiritilishi kerak")
