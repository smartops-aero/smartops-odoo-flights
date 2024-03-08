# -*- coding: utf-8 -*-
{
    'name': "flights Ops",
    'author': "Apexive Studio LLC, Ivan Elizaryev",
    'website': "https://apexive.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Industries',
    'version': '16.0.0.1',
    'license': "Other OSI approved licence",  # MIT

    # any module necessary for this one to work correctly
    'depends': [
        'flights',
        'resource_booking',
        'hr',
    ],

    # always loaded
    'data': [
    ],
}
