# Copyright 2024 Sergio Corato <https://github.com/sergiocorato>
# Copyright 2024 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "ITA - Fattura elettronica - Supporto GovWay",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Invio fatture elettroniche tramite GovWay",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_it_fatturapa_in",
        "l10n_it_sdi_channel",
        "web",
    ],
    "data": [
        # "security/ir.model.access.csv",
        # "views/fetchmail_view.xml",
        "views/company_view.xml",
        "views/sdi_view.xml",
        "views/ir_mail_server.xml",
        "data/fetchmail_data.xml",
        "data/config_parameter.xml",
        "data/sdi_channel_demo.xml",
    ],
    "installable": True,
}
