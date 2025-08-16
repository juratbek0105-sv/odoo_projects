from odoo import models, fields

class ClinicAppointment(models.Model):
    _name = 'clinic.appointment'
    _description = 'Qabul'

    name = fields.Char(required=True, default="Yangi qabul")
    patient_id = fields.Many2one('clinic.patient', required=True)
    doctor_id = fields.Many2one('clinic.doctor', required=True)
    start_time = fields.Datetime( required=True)
    end_time = fields.Datetime()
    state = fields.Selection([
        ('new', 'Yangi'),
        ('confirmed', 'Tasdiqlangan'),
        ('cancelled', 'Bekor qilingan'),
        ('done', 'Tugallangan'),
    ],default='new')
    diagnosis = fields.Text()
    urgency = fields.Selection([
        ('low', 'Past'),
        ('medium', 'O‘rta'),
        ('high', 'Yuqori'),
    ], default='low')

    prescription_ids = fields.One2many('clinic.prescription', 'appointment_id')
