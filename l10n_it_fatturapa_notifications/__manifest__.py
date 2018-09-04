# -*- coding: utf-8 -*-
# Copyright 2015-2018 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'FatturaPA - Notifications',
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Electronic invoices notifications',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa',
    ],
    "data": [
        'views/attachment_view.xml',
        'wizard/import_notification_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True
}
