# -*- coding: utf-8 -*-
{
    'name': "Rental Management",

    'depends': ['base'],


    'data': [
        'security/ir.model.access.csv',

        'views/category.xml',
        'views/customer.xml',
        'views/product.xml',
        'views/rental_order.xml',
        'views/rental_price.xml',
    ],
    'demo': [
        'demo/demo.xml'],
}

