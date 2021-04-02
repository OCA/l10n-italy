#  Copyright 2011-2012 Domsense s.r.l. (<http://www.domsense.com>)
#  Copyright 2012-17 Agile Business Group (<http://www.agilebg.com>)
#  Copyright 2012-15 LinkIt Spa (<http://http://www.linkgroup.it>)
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Liquidazione IVA",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Allow to create the 'VAT Statement'.",
    "license": "AGPL-3",
    "author": "Agile Business Group, Odoo Community Association (OCA), LinkIt Spa",
    "website": "https://github.com/OCA/l10n-italy",
    "depends": [
        "account",
        "account_tax_balance",
        "date_range",
        "l10n_it_account",
        "l10n_it_fiscalcode",
        "web",
    ],
    "data": [
        "wizard/add_period.xml",
        "wizard/remove_period.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "report/reports.xml",
        "views/report_vatperiodendstatement.xml",
        "views/config.xml",
        "views/account_view.xml",
    ],
    "installable": True,
}
