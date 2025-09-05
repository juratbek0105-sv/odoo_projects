# -*- coding: utf-8 -*-
{
    'name': "src/homeworks/odoo_log",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/log.xml',
    ],
}
