# -*- coding: utf-8 -*-
{
    'name': "KGK commission",

    'summary': """
        Direct sales management and commissions
        """,

    'description': """
        Direct sales management and commissions
    """,

    'author': "KGK",
    'website': "http://www.kgk.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'sale_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/commission_security.xml',
        'views/views.xml',
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