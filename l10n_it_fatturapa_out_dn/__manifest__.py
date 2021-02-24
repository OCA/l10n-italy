# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Ruben Tonetto (Associazione PNLUG - Gruppo Odoo)
# Copyright 2020 Marco Colombo (Phi Srl)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'ITA - Fattura elettronica - Integrazione DN',
    "summary": "Modulo ponte tra emissione fatture elettroniche e DN",
    "version": "12.0.0.0.0",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy/',
    "author": "Phi Srl, Odoo Community Association (OCA)",
    "maintainers": [],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_delivery_note",
    ],
    "data": [
        "wizard/wizard_export_fatturapa_view.xml"
    ],
}
