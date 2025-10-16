from odoo import models, fields, api


class Project(models.Model):
    _name = 'task_management.project'
    _description = 'Project'

    name = fields.Char(string="Project Name")
    task_ids = fields.One2many("task_management.task", "project_id", string="Tasks")
    responsible_id = fields.Many2one("res.users", string="Responsible")
