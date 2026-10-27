# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Italy - E-invoicing - Oss",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "summary": "OSS support for Italian e-invoicing",
    "author": "Giuseppe Borruso, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": ["openupgradelib"],
    },
    "depends": [
        "l10n_eu_oss_oca",
        "l10n_it_edi",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "installable": True,
    "pre_init_hook": "pre_absorb_old_module",
}
