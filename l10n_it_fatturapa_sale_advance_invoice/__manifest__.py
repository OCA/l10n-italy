# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Sale advance invoice compatibility",
    "version": "12.0.1.0.0",
    "website": "https://github.com/OCA/l10n-italy/tree/"
               "12.0/l10n_it_fatturapa_sale_advance_invoice",
    "author": "Sergio Corato, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Hidden",
    "auto_install": True,
    "depends": [
        "l10n_it_fiscal_document_type",
        "sale_management",
    ],
    "data": [
        "views/journal.xml",
    ],
}
