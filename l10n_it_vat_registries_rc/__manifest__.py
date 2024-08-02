# Copyright 2024 Lorenzo Battistini
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Registri IVA con Reverse Charge",
    "summary": "Integrazione l10n_it_vat_registries e l10n_it_reverse_charge",
    "version": "16.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Innovyou, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "preloadable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_vat_registries",
        "l10n_it_reverse_charge",
    ],
    "data": [
        "report/report_registro_iva.xml",
    ],
}
