# Copyright 2024 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Supporto IVA 74-ter - Export XML FatturaPA",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "summary": "Supporto IVA secondo art.74-ter, DPR 633/72 - Agenzie viaggi e turismo per la generazione del file XML FatturaPA",
    "author": "Innovyou, Odoo Community Association (OCA)",
    "maintainers": ["eLBati", "LorenzoC0"],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_fatturapa_out",
        "l10n_it_reverse_charge",
    ],
    "data": [
        'views/res_partner_views.xml',
        'data/invoice_it_template.xml',
        "views/account_move_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
