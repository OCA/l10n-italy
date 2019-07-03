# -*- coding: utf-8 -*-
# Copyright 2011-2013 Associazione OpenERP Italia
# (<http://www.openerp-italia.org>).
# Copyright 2012 Domsense srl (<http://www.domsense.com>)
# Copyright 2012-2018 Lorenzo Battistini - Agile Business Group
# Copyright 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Registri IVA',
    'version': '10.0.1.3.0',
    'category': 'Localization/Italy',
    "author": "Agile Business Group, Odoo Community Association (OCA)"
              ", LinkIt Srl",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'development_status': 'Production/Stable',
    "depends": [
        'base_setup',
        'account',
        'l10n_it_account',
        'report',
        'account_tax_balance',
        'account_accountant',
        'date_range',
        ],
    "data": [
        'security/ir.model.access.csv',
        'security/vat_registry_security.xml',
        'views/account_journal_view.xml',
        'views/account_tax_registry_view.xml',
        'views/account_view.xml',
        'wizard/print_registro_iva.xml',
        'report/reports.xml',
        'report/report_registro_iva.xml'
    ],
    'installable': True,
}
