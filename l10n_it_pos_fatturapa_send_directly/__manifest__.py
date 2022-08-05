# Copyright 2021 Lorenzo Battistini @ TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - POS - Fattura elettronica - Invio diretto",
    "summary": "Inviare automaticamente a SDI la fattura elettronica dal POS",
    "version": "12.0.2.0.0",
    "development_status": "Beta",
    "category": "Point Of Sale",
    "website": "https://github.com/OCA/l10n-italy"
               "/tree/12.0/l10n_it_pos_fatturapa_send_directly",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "l10n_it_pos_fatturapa",
        "l10n_it_sdi_channel",
    ],
    'qweb': [
    ],
    'data': [
    ],
}
