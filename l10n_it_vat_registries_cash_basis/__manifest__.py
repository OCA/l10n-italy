# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - VAT Registries - Cash Basis',
    'version': '10.0.0.0.0',
    'category': 'Hidden',
    "author": "LinkIt Srl, Agile Business Group",
    'website': 'http://www.linkgroup.it/',
    'license': 'LGPL-3',
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
