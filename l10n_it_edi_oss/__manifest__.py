# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Italy - E-invoicing - OSS",
    "version": "18.0.1.1.0",
    "category": "Accounting/Localizations/EDI",
    "development_status": "Beta",
    "summary": "Bridge module between l10n_eu_oss and Italian electronic invoicing",
    "author": "Lorenzo Battistini, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi",
        "l10n_eu_oss",
    ],
    "external_dependencies": {"python": ["openupgradelib"]},
    "installable": True,
    "pre_init_hook": "pre_absorb_old_module",
    "post_init_hook": "_l10n_it_edi_oss_post_init_hook",
}
