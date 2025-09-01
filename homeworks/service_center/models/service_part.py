from odoo import models, fields


class ServicePart(models.Model):
    _name  = "service.part"
    _description = "Service part"

    name = fields.Char()
    code  = fields.Char()
    is_active = fields.Boolean()
    description = fields.Text()


    def action_deactivate(self):
        self.write({"is_active":False})


    def action_activate(self):
        self.write({"is_active":True})
