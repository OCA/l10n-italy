# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018-2019 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2019 Gianluigi Tiesi - Netfarm S.r.l.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Base',
    'version': '12.0.2.1.0',
    'category': 'Localization/Italy',
    'summary': 'Fatture elettroniche',
    'author': 'Davide Corio, Agile Business Group, Innoviu, '
              'Odoo Italia Network, Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/12.0/'
               'l10n_it_fatturapa',
    'license': 'AGPL-3',
    'excludes': ['l10n_it_edi'],
    "depends": [
        'l10n_it_account',
        'l10n_it_fiscalcode',
        'document',
        'l10n_it_ipa',
        'l10n_it_rea',
        'base_iban',
        'l10n_it_account_tax_kind',
        'l10n_it_esigibilita_iva',
        'l10n_it_fiscal_payment_term',
        'l10n_it_split_payment',
        'l10n_it_fiscal_document_type',
        'partner_firstname',
        ],
    "data": [
        'data/fatturapa_data.xml',
        'data/welfare.fund.type.csv',
        'views/account_view.xml',
        'views/company_view.xml',
        'views/partner_view.xml',
        'views/invoice_view.xml',
        'views/related_document_type_views.xml',
        'security/ir.model.access.csv',
    ],
    "demo": ['demo/account_invoice_fatturapa.xml'],
    'installable': True,
    'external_dependencies': {
        'python': [
            'pyxb',  # pyxb 1.2.6
            'asn1crypto'
        ],
    }
}
