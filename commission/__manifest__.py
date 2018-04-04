# -*- coding: utf-8 -*-
{
    'name': "Circles commission",

    'summary': """
        Direct sales management and commissions
        """,

    'description': """
        Direct sales management and commissions
    """,

    'author': "Circles",
    'website': "http://www.circles.vn",

    # Categories can be used to filter modules in modules listing
    'category': 'CRM',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'sale_management', 'hr'],

    # always loaded
    'data': [        
        'security/ir.model.access.csv',
        'security/commission_security.xml',
        'views/views.xml',
        'report/report_commission.xml',
        'views/views_employee.xml',
        'views/templates.xml',
        'views/views_commission_scheme.xml',
        'views/menu_commission.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}