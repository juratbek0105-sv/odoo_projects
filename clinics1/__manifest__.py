{
    'name': 'Clinic Management',
    'version': '0.1',
    'summary': 'Klinika boshqaruvi tizimi',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/clinic_patient_view.xml',
        'views/clinic_doctor_view.xml',
        'views/clinic_appointment_views.xml',
        'views/clinic_medicine_views.xml',
        'views/clinic_prescription_views.xml',
        'views/clinic_prescription_line_views.xml'
    ],
    'application': True,
    'installable': True,
}
