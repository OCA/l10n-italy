# -*- coding: utf-8 -*-
# Copyright 2011-2013 Associazione OpenERP Italia
# (<http://www.openerp-italia.org>).
# Copyright 2012-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# Copyright 2017 Lara Baggio - LinkIt Srl (<http://http://www.linkgroup.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Italian Localization - VAT Registries - Cash Basis',
    'version': '10.0.0.0.0',
    'category': 'Hidden',
    "author": "LinkIt Srl, Agile Business Group"
              ", Odoo Community Association (OCA)",
    'website': 'http://www.linkgroup.it/',
    'license': 'AGPL-3',
    'description': """ Modulo per la corretta visualizzione del registro IVA
    delle fatture in caso di attivazione della gestione di IVA cassa
    """,
    "depends": [
         'l10n_it_vat_registries',
         'account_tax_cash_basis'
        ],
    "data": [
    ],
    'installable': True,
    'auto_install': True,
}
