# Copyright 2024 Marco Colombo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "version": "16.0.0.0.1",
    "name": "ITA - Registri IVA - formato XLSX",
    "category": "Localization/Italy",
    "author": "Phi Srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "development_status": "Beta",
    "depends": [
        "base",
        "product",
        "report_xlsx_helper",
        "l10n_it_vat_registries",
    ],
    "data": [
        "wizard/print_registro_iva.xml",
        "report/reports.xml",
    ],
    "installable": True,
}
