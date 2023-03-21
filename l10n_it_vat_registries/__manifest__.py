# Copyright 2011-2013 Associazione OpenERP Italia
# (<http://www.openerp-italia.org>).
# Copyright 2012 Domsense srl (<http://www.domsense.com>)
# Copyright 2012-2018 Lorenzo Battistini - Agile Business Group
# Copyright 2012-15 LinkIt srl (<http://http://www.linkgroup.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'version': '12.0.1.2.4',
    'name': 'ITA - Registri IVA',
    'category': 'Localization/Italy',
    "author": "Agile Business Group, Odoo Community Association (OCA)"
              ", LinkIt Srl",
    'website': 'https://github.com/OCA/l10n-italy/tree/12.0/'
               'l10n_it_vat_registries',
    'license': 'AGPL-3',
    'development_status': 'Production/Stable',
    "depends": [
        'base_setup',
        'account',
        'l10n_it_account',
        'web',
        'account_tax_balance',
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
