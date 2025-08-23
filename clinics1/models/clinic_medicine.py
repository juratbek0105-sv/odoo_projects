from odoo import models, fields

class ClinicMedicine(models.Model):
    _name = 'clinic.medicine'
    _description = 'Dori'

    name = fields.Char( required=True)
    generic_name = fields.Char()
    dosage_unit = fields.Selection([
        ('mg', 'Milligram'),
        ('ml', 'Millilitr'),
        ('tablet', 'Tabletka'),
    ], string="Dozalash birligi")
    description = fields.Text()
    manufacturer = fields.Char()
    contraindications = fields.Text()

    incompatible_ids = fields.Many2many(
        'clinic.medicine',
        'medicine_incompatible_rel',
        'medicine_id', 'incompatible_id')
