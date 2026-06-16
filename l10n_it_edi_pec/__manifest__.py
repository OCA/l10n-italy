# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Fattura elettronica - Supporto PEC",
    "version": "18.0.1.1.0",
    "category": "Localization/Italy",
    "summary": "Invio e ricezione fatture elettroniche tramite PEC",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    "depends": [
        "l10n_it_account",
        "l10n_it_edi_sdi",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/fetchmail_data.xml",
        "views/res_config_settings_views.xml",
        "views/fetchmail_view.xml",
        "views/ir_mail_server_view.xml",
    ],
    "installable": True,
    "pre_init_hook": "_l10n_it_edi_pec_pre_init_hook",
    "post_init_hook": "_l10n_it_edi_pec_post_init_hook",
}
