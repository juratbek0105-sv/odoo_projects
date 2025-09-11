from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ServiceOrderRating(models.Model):
    _name = "service.order.rating"
    _description = "Service Order Rating"

    center_id = fields.Many2one("service.center", string="Service Center")
    order_id = fields.Many2one("service.order", string="Order")
    customer_id = fields.Many2one("service.customer", string="Customer")
    technician_id = fields.Many2one(
        "service.technician",
        string="Technician",
        compute="_compute_technician_id",
        store=True
    )
    score = fields.Selection([
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5")
    ], string="Rating", required=True)
    comment = fields.Text(string="Comment")
    rating_date = fields.Date(string="Rating Date")

    @api.depends("order_id")
    def _compute_technician_id(self):
        for record in self:
            record.technician_id = record.order_id.technician_id if record.order_id else False

    @api.constrains("score")
    def _check_score(self):
        for record in self:
            if record.score and (record.score < 1 or record.score > 5):
                raise ValidationError("Baholash bali 1 dan 5 gacha bo'lishi kerak")
