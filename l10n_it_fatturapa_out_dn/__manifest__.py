# Copyright 2021 Marco Colombo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Emissione - DDT",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Localization/Italy",
    "summary": "DDT in fatture elettroniche",
    "author": "Marco Colombo," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_delivery_note",
    ],
    "data": [
        "data/invoice_it_template.xml",
        "wizard/wizard_export_fatturapa_view.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
