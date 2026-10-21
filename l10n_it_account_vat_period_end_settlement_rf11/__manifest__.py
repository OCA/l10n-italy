# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Supporto IVA 74-ter - Liquidazione IVA",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Localization/Italy",
    "summary": "Supporto IVA secondo art. 74-ter, DPR 633/72 - Agenzie viaggi "
    "e turismo - per la liquidazione IVA",
    "author": "Innovyou, Odoo Community Association (OCA)",
    "maintainers": ["eLBati", "LorenzoC0"],
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    # NOTE (v18 port): the Odoo 16 module depended on the OCA
    # `account_vat_period_end_statement`, which in Odoo 18 was renamed to
    # `l10n_it_account_vat_period_end_settlement`. `account_tax_balance`
    # (kept explicit as in v16) provides `base_balance` used by the 74-ter
    # "base su base" computation.
    "depends": [
        "account",
        "account_tax_balance",
        "l10n_it_account_vat_period_end_settlement",
    ],
    "data": [
        "views/account_tax_views.xml",
        "views/account_vat_period_end_views.xml",
        "report/report_vatperiodendstatement.xml",
    ],
    "external_dependencies": {
        "python": [
            "openupgradelib",
        ],
    },
    # Absorbs the Odoo 16 module `account_vat_period_end_statement_rf11`
    # (renaming it into this one, preserving every 74-ter value) when this
    # module is installed on a v16-upgraded DB. A pre_init_hook (not a
    # migrations/ script) because this module name is new in v18: from Odoo's
    # point of view it is a fresh install, and migration scripts run only on
    # upgrades, never on installs.
    "pre_init_hook": "pre_absorb_old_module",
    "installable": True,
}
