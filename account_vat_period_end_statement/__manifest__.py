#    Copyright (C) 2011-2012 Domsense s.r.l. (<http://www.domsense.com>).
#    Copyright (C) 2012-17 Agile Business Group (<http://www.agilebg.com>)
#    Copyright (C) 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
#    Copyright (C) 2015 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).

{
    "name": "Liquidazione IVA",
    "version": "11.0.1.0.0",
    'category': 'Localization/Italy',
    'license': 'AGPL-3',
    "author": "Agile Business Group, Odoo Community Association (OCA)"
              ", LinkIt Spa",
    'website': 'https://github.com/OCA/l10n-italy/tree/11.0/'
               'account_vat_period_end_statement',
    "depends": [
        "account_invoicing",
        "account_tax_balance",
        "date_range",
        "l10n_it_account",
        "l10n_it_fiscalcode",
        "web",
        ],
    'data': [
        'wizard/add_period.xml',
        'wizard/remove_period.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/reports.xml',
        'views/report_vatperiodendstatement.xml',
        'views/config.xml',
        'views/account_view.xml',
    ],
    'installable': True,
}
