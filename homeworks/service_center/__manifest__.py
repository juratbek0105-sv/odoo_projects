# -*- coding: utf-8 -*-
{
    'name': "Service Center",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        "security/service_center_security.xml",
        "security/ir.model.access.csv",
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
        "views/order_line_views.xml"

    ]
}

