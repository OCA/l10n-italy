# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Compute invoice taxes with e-invoice values",
    "summary": "This module enables recomputation of the invoice on e-invoices values "
               "as if imported with custom precisions, these values will not be "
               "mantained.",
    "version": "12.0.1.0.0",
    "development_status": "Alpha",
    "category": "Accounting & Finance",
    "website": "https://github.com/OCA/l10n-italy/tree/12.0/"
               "l10n_it_fatturapa_in_recompute",
    "author": "Sergio Corato, Odoo Community Association (OCA)",
    "maintainers": ["sergiocorato"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "l10n_it_fatturapa_in",
    ],
    "data": [
        "views/account_invoice_view.xml",
    ],
}
