# Copyright 2026 Lorenzo Battistini (https://github.com/eLBati)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Registri IVA - Stampa retrocompatibile",
    "summary": "Stampa registri IVA retrocompatibile "
    "con dati registrati in versione 16",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Associazione Odoo Italia, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_vat_registries",
        "report_xlsx_helper",
    ],
    "data": [
        "report/reports.xml",
        "report/report_registro_iva.xml",
        "wizard/print_registro_iva.xml",
    ],
    "installable": True,
    "development_status": "Beta",
}
