# -*- coding: utf-8 -*-
{
    'name': "Pilot Log",

    'summary': """
        Flights module extention to manage individual pilot logbook records""",

    'description': """
        Flights module extention to manage individual pilot logbook records
    """,

    'author': "Apexive Studio LLC, Ivan Elizaryev",
    'website': "https://apexive.com",
    'license': "Other OSI approved licence",  # MIT

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Industries',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['flights'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/flight_pilot_event_kind_data.xml',
        'data/flight_pilottime_kind_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
