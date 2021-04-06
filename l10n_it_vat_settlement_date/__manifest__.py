#  Copyright 2021 Marco Colombo (<https://github/TheMule71)
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Data competenza IVA",
    "version": "12.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Settlement date for VAT Statement",
    "license": "AGPL-3",
    "author": "Marco Colombo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "depends": [
        "account_vat_period_end_statement",
        "l10n_it_vat_registries",
        ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice_view.xml",
        "report/report_registro_iva.xml"
    ],
    "installable": True,
}
