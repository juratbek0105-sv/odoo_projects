from odoo import models, fields


class Author(models.Model):
    _name = "ecommercy.book"
    _description = "Book"

    name = field{
    'name': 'Clinic Management',
    'version': '1.0',
    'author': 'Sizning Ismingiz',
    'summary': 'Klinika boshqaruvi tizimi',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'application': True,
    'installable': True,
}
s.Char()