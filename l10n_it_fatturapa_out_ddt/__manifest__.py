# Copyright 2018 Lorenzo Battistini
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Ruben Tonetto (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'ITA - Fattura elettronica - Integrazione DDT',
    "summary": "Modulo ponte tra emissione fatture elettroniche e DDT",
    "version": "12.0.1.4.1",
    "development_status": "Beta",
    "category": "Hidden",
    'website': 'https://github.com/OCA/l10n-italy'
               '/tree/12.0/l10n_it_fatturapa_out_ddt',
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "maintainers": [
        "eLBati",
    ],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_ddt",
    ],
    "data": [
        "wizard/wizard_export_fatturapa_view.xml",
        "views/res_config_settings_views.xml",
    ],
}
