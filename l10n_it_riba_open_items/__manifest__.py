# Copyright 2026 nextev.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "ITA - Partite aperte con scoperto RiBa",
    "summary": "Mostra nel report Partite aperte le fatture chiuse da "
    "accettazione RiBa con il relativo valore scoperto",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Nextev, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "account_financial_report",
        "l10n_it_riba_oca",
    ],
    "data": [
        "wizard/open_items_wizard_view.xml",
        "report/templates/open_items.xml",
    ],
    "installable": True,
}
