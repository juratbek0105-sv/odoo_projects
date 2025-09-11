from odoo import models, fields


class ServicePart(models.Model):
    _name = "service.part"
    _description = "Service Part"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    is_active = fields.Boolean(string="Active", default=True)
    description = fields.Text(string="Description")

    _sql_constraints = [
        ('code_unique', 'unique(code)', "Code must be unique!"),
        ('name_unique', 'unique(name)', "Name must be unique!"),
    ]

    def action_deactivate(self):
        """Set the part as inactive"""
        self.write({"is_active": False})

    def action_activate(self):
        """Set the part as active"""
        self.write({"is_active": True})
