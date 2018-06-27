# -*- coding: utf-8 -*-
# Author: Gianmarco Conte - Dinamiche Aziendali Srl
# Copyright 2018
# Dinamiche Aziendali Srl <www.dinamicheaziendali.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Account central journal',
    'version': '11.0.0.0.1',
    'category': 'Localization/Italy',
    'author': 'Dinamiche Aziendali, Odoo Community Association (OCA)',
    'website': 'http://www.dinamicheaziendali.it',
    'license': 'AGPL-3',
    "depends": [
        'account',
        'date_range'
        ],
    "data": [
        'security/ir.model.access.csv',
        'report/internal_layout.xml',
        'report/reports.xml',
        'wizard/print_giornale.xml',
        'views/report_account_central_journal.xml',
        'views/date_range_view.xml'
    ],
    "installable": True,
}
