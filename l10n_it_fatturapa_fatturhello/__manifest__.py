# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Fattura elettronica - Supporto Fatturhello",
    "version": "16.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Invio e ricezione fatture elettroniche tramite Fatturhello",
    "author": "PyTech, Odoo Community Association (OCA)",
    "maintainers": [
        "aleuffre",
        "SirPyTech",
    ],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_sdi_channel",
    ],
    "data": [
        "data/ir_cron_data.xml",
        "data/sdi_channel_data.xml",
        "security/ir.model.access.csv",
        "views/fatturapa_attachment_out_views.xml",
        "views/res_company_views.xml",
        "views/sdi_channel_views.xml",
        "wizards/login_views.xml",
    ],
}
