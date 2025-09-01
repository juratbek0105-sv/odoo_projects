# -*- coding: utf-8 -*-
{
    'name': "Service Center",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/service_center_security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/country_views.xml",
        "views/state_views.xml",
        "views/district_views.xml",
        "views/center_views.xml",
        "views/technician_views.xml",
        "views/customer_views.xml",
        "views/part_views.xml",
        "views/order_views.xml",
        "views/payment_views.xml",
        "views/rating_views.xml",
    ]
}

