from odoo import models, fields, api

class Task(models.Model):
    _name = 'task_management.task'
    _description = 'Task'

    project_id = fields.Many2one("task_management.project", string="Project")
    name = fields.Char(string="Task Name")
    assignee_id = fields.Many2one("res.users", string="Assignee")
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('ready_for_test', 'Ready For Test'),
        ('done', 'Done')
    ], default="to_do", group_expand="_read_group_status")

    @api.model
    def _read_group_status(self, values, domain):
        return ['to_do', 'in_progress', 'ready_for_test', 'done']

