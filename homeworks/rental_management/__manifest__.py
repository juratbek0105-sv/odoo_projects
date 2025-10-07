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

        'data/ir.sequence.xml',
        'data/configuration.xml',

        'wizard/check_broken.xml',
        
        'report/order_report.xml',
        'report/product_report.xml',
        'report/price_report.xml'
    ],
    'demo': [
        'demo/demo.xml'],
}

