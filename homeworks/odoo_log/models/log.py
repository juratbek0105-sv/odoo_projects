from odoo import models, fields

class Log(models.Model):
    _name = "product.log"
    _description = "Log"

    username = fields.Char(required=True)
    message = fields.Text()


