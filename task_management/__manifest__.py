# -*- coding: utf-8 -*-
{
    'name': "task_management",

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',

        'views/project.xml',
        'views/task.xml',
        'views/menu_items.xml'
    ],
}

