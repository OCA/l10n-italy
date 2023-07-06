# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Causali pagamento",
    "summary": "Aggiunge la tabella delle causali di pagamento da usare ad esempio "
    "nelle ritenute d'acconto",
    "version": "14.0.1.1.0",
    "development_status": "Production/Stable",
    "category": "Account",
    "author": "Agile Business Group," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/payment_reason_data.xml",
        "views/payment_reason_view.xml",
    ],
    "installable": True,
    "pre_init_hook": "rename_old_italian_module",
}
