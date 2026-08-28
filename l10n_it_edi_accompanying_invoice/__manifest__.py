# Copyright 2026 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Fattura elettronica - Integrazione fattura accompagnatoria",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Popolare DatiTrasporto nella fattura elettronica.",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_accompanying_invoice",
        "l10n_it_edi_extension",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "auto_install": True,
}
