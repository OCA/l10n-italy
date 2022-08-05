# Copyright 2020 Lorenzo Battistini @ TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Codice fiscale nel preventivo",
    "summary": "Mostra il codice fiscale del cliente nella stampa del preventivo",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_fiscalcode_sale",
    "author": "TAKOBI, Nextev Srl, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "sale",
        "l10n_it_fiscalcode",
    ],
    "data": [
        "views/sale_order_report.xml",
    ],
}
