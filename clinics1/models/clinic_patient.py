from odoo import models, fields

class Patient(models.Model):
    _name = "clinic.patient"
    _description = "Bemor"

    name = fields.Char(required=True)
    birth_date = fields.Date(required=True)
    telephone_email = fields.Text()
    sugurta_raqami = fields.Char()
    manzil = fields.Integer(required=True)
    allergies = fields.Text()
    emmergency_call_name = fields.Char()
    emmergency_call_phone = fields.Text()
    gender = fields.Selection([
        ("male", "erkak"),
        ("female", "ayol"),
        ("boshqa", "other")
    ])

    appointment_ids = fields.One2many('clinic.appointment', 'patient_id')
