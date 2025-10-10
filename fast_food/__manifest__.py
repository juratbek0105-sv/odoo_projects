# -*- coding: utf-8 -*-
{
    'name': "Fast Food",
    'version': "1.0",
    'category': 'Sales',
    'summary': "Fast Food Management",
    'description': "Manage products, categories, orders, and payments for a fast food business.",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/category.xml',
        'views/order.xml',
        'views/order_line.xml',
        'views/payment.xml',
        'views/kitchen_display.xml',
        'views/actions.xml',
        'views/menus.xml',
        'data/ir.sequence.xml',
        'report/product_report.xml',
        'report/category_report.xml',
        'report/order_report.xml',
        'report/payment_report.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
