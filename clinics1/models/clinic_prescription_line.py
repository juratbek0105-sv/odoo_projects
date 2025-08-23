from odoo import models, fields

class ClinicPrescriptionLine(models.Model):
    _name = 'clinic.prescription.line'
    _description = 'Retsept liniyasi'

    prescription_id = fields.Many2one('clinic.prescription', required=True, ondelete='cascade')
    medicine_id = fields.Many2one('clinic.medicine', required=True)
    dosage = fields.Char()
    frequency = fields.Char()
    duration = fields.Char()
    notes = fields.Text()