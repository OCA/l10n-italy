# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italy - E-invoicing - Testo Unico IVA references",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "development_status": "Beta",
    "summary": "Cite the Testo Unico IVA (D.Lgs. 10/2026) references in "
    "e-invoices dated from 1 January 2027",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it",
        "l10n_it_edi",
    ],
    "data": [
        "views/account_tax_views.xml",
        "views/report_invoice_document.xml",
    ],
    "installable": True,
}
