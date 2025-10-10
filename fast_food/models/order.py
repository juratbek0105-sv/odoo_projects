from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name = "fast.food.order"
    _description = "Order"

    name = fields.Char(string="Order Reference", default="New")
    table_number = fields.Integer(string="Table Number")
    order_type = fields.Selection([
        ("dine_in", "Dine In"),
        ("takeaway", "Takeaway")
    ], default="dine_in", string="Order Type")
    currency_id = fields.Many2one('res.currency',string='Currency',)
    total_amount = fields.Monetary(compute="_compute_total_amount", store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], default="draft", group_expand="_read_group_status", store=True)
    kitchen_status = fields.Selection([
        ('to_cook', 'To Cook'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
    ], string="Preparation Status", default='to_cook', group_expand="_read_group_kitchen_status")

    order_time = fields.Datetime(string="Order Time", default=fields.Datetime.now)
    payment_ids = fields.One2many("fast.food.payment", "order_id", string="Payments")
    order_line_ids = fields.One2many("fast.food.order.line", "order_id", string="Order Lines")

    order_line_display = fields.Text(
        string="Order Line Display",
        compute="_compute_order_line_display",
        store=False,
    )

    @api.depends('order_line_ids', 'order_line_ids.product_id', 'order_line_ids.quantity')
    def _compute_order_line_display(self):
        for record in self:
            record.order_line_display = "\n".join(
                f"{line.product_id.name} x {line.quantity}" for line in record.order_line_ids
            ) or "No products"

    # ---------------- Actions ----------------
    def action_confirm(self):
        for record in self:
            if record.status == "draft":
                record.status = "confirmed"

    def action_paid(self):
        for record in self:
            if record.status == "confirmed":
                record.status = "paid"

    def action_cancel(self):
        for record in self:
            record.status = "cancelled"

    def action_reset_to_draft(self):
        for record in self:
            record.status = "draft"

    def action_kitchen_start(self):
        for record in self:
            record.kitchen_status = 'ready'

    def action_kitchen_end(self):
        for record in self:
            record.kitchen_status = 'completed'

    # ---------------- Computed Fields ----------------
    @api.depends("order_line_ids.subtotal")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.order_line_ids)

    @api.onchange('order_type')
    def _onchange_order_type(self):
        if self.order_type != 'dine_in':
            self.table_number = False

    @api.model
    def _read_group_status(self, values, domain):
        return ['draft', 'confirmed', 'paid', 'cancelled']

    @api.model
    def _read_group_kitchen_status(self, values, domain):
        return ['to_cook', 'ready', 'completed']

    # ---------------- Constraints ----------------

    @api.constrains("total_amount")
    def _check_total_amount(self):
        for order in self:
            if order.total_amount <= 0:
                raise ValidationError("Total amount should be positive.")

    @api.constrains("status", "payment_ids")
    def _check_cancelled_no_payment(self):
        for order in self:
            if order.status == "cancelled" and order.payment_ids:
                raise ValidationError("Cancelled orders should not have payments.")


    # ---------------- Create Override ----------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fast.food.order') or 'New'
        return super(Order, self).create(vals_list)



