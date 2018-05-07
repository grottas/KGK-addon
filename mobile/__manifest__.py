# -*- coding: utf-8 -*-
{
    'name': "Circles mobile",

    'summary': """
        Support for mobile app""",

    'description': """
        Support for mobile app
    """,

    'author': "Circles.vn",
    'website': "http://www.circles.vn",

    # Categories can be used to filter modules in modules listing
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','crm', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}