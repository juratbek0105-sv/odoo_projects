from odoo import models, fields

class ClinicPrescription(models.Model):
    _name = 'clinic.prescription'
    _description = 'Retsept'

    appointment_id = fields.Many2one('clinic.appointment', required=True)
    date_prescribed = fields.Date(default=fields.Date.today)
    doctor_id = fields.Many2one('clinic.doctor', required=True)
    general_instructions = fields.Text()

    line_ids = fields.One2many('clinic.prescription.line', 'prescription_id')
