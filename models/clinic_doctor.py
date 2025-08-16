from odoo import models, fields

class ClinicDoctor(models.Model):
    _name = "clinic.doctor"
    _description = "Doktor"


    name = fields.Char()
    mutaxasislik = fields.Char()
    ish_rejemi = fields.Text()
    xona_raqami = fields.Integer()
    litsenziya = fields.Char()
    amaliy_tajriba = fields.Integer()
    til = fields.Char()

    appointment_ids = fields.One2many('clinic.appointment', 'doctor_id')
