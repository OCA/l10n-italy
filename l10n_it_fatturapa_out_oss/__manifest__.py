# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Fattura elettronica - Emissione - OSS",
    "version": "12.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "summary": "OSS in fatturapa",
    "author": "Sergio Corato," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_fatturapa_out",
        "l10n_eu_oss",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/oss_security.xml",
        "views/account.xml",
        "views/company_view.xml",
    ],
    "installable": True,
    "autoinstall": True,
}
