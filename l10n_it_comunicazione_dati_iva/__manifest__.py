# -*- coding: utf-8 -*-
# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-2019 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Comunicazione dati IVA',
    'version': '10.0.1.0.1',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro",
    'website': 'http://www.odoo-italia.net',
    'license': 'LGPL-3',
    'depends': [
        'account', 'l10n_it_fiscal_document_type', 'l10n_it_codici_carica',
        'l10n_it_fiscalcode', 'l10n_it_esigibilita_iva',
        'l10n_it_account_tax_kind', 'report_intrastat'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/compute_fiscal_document_type_view.xml',
        'views/comunicazione.xml',
        'views/account.xml',
        'views/account_invoice_view.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
