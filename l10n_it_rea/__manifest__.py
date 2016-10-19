# -*- encoding: utf-8 -*-
# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2015 Alessio Gerace <alessio.gerace@agilebg.com>
# Copyright 2016 Andrea Gallina (Apulia Software)

{
    'name': 'REA Register',
    'version': '9.0.0.1.0',
    'category': 'Localisation/Italy',
    'summary': 'Manage fields for  Economic Administrative catalogue',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": [
        'account'
    ],
    "data": [
        'views/partner_view.xml',
    ],
    'installable': True,
}
