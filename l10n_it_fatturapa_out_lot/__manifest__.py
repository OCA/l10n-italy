# Copyright 2023 Giuseppe Borruso
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Emissione - Lotti",
    "version": "14.0.1.0.2",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "summary": "Lotti in fatturapa",
    "author": "Giuseppe Borruso, Odoo Community Association (OCA)",
    "maintainers": ["Borruso"],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "account_invoice_production_lot",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "installable": True,
}
