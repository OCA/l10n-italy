# Copyright 2020 Marcelo Frare (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Close Period",
    "version": "12.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Stock Close Period",
    "author": "Pordenone Linux User Group (PNLUG), "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
    ],
    "data": [
        "security/stock_close_group.xml",
        "security/ir.model.access.csv",
        "data/action_server.xml",
        "views/stock_close_views.xml",
        "wizards/stock_close_import.xml",
        "wizards/stock_close_print.xml",
        "reports/xlsx_stock_close_print.xml",
    ],
    "installable": True,
}
