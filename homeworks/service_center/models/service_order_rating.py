from odoo import models, fields, api
from odoo.odoo.exceptions import ValidationError


class ServicePart(models.Model):
    _name  = "service.order.rating"
    _description = "service order rating"

    center_id = fields.Many2one("service.center")
    order_id  = fields.Many2one("service.order")
    customer_id = fields.Many2one("service.customer")
    technician_id = fields.Many2one("service.technician", compute="_compute_technician_id")
    score = fields.Selection([
        (1,"bir"),
        (2, "ikki"),
        (3, "uch"),
        (4, "turt"),
        (5, "besh")
    ])
    comment = fields.Text()
    rating_date = fields.Date()

    @api.constarints("score")
    def check_score(self):
        for record in self:
            if record.score > 5 or record.score < 1:
                raise ValidationError("Baholash bali 1dan 5gacha bo'lishi kerak")

