# -*- coding: utf-8 -*-
# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2017-2019 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Comunicazione dati fatture',
    'summary': 'Comunicazione dati fatture (c.d. "nuovo spesometro" o '
               '"esterometro")',
    'version': '8.0.1.1.0',
    'category': 'Account',
    'author': "Openforce di Camilli Alessandro, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/l10n-italy/tree/'
               '8.0/l10n_it_invoices_data_communication',
    'license': 'LGPL-3',
    'depends': [
        'account',
        'account_invoice_entry_date',
        'l10n_it_account',
        'l10n_it_account_tax_kind',
        'l10n_it_codici_carica',
        'l10n_it_esigibilita_iva',
        'l10n_it_fiscal_document_type',
        'l10n_it_fiscalcode',
        'report_intrastat',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/compute_fiscal_document_type_view.xml',
        'wizard/split_big_communication_view.xml',
        'views/comunicazione.xml',
        'views/account.xml',
        'views/account_invoice_view.xml',
        'wizard/export_file_view.xml',
        'security/security.xml',
    ],
    'installable': True,
}
