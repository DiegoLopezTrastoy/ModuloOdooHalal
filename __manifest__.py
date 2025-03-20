# -*- coding: utf-8 -*-
{
    'name': "my_portal",
    'summary': "Modulo creado para modificar el portal de odoo",
    'description': "Modulo creado para modificar el portal de odoo",
    'author': "Diego López Trastoy",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'portal', 'barcodes'],
    'data': [
        'security/ir.model.access.csv',
        'views/backoffice.xml',
        'views/portal_templates.xml',
        'views/reports.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}