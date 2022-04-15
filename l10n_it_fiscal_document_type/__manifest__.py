# Copyright 2017 Alessandro Camilli
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# Copyright 2021 Andrea Cometa (https://www.apuliasoftware.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Tipi di documento fiscale per dichiarativi",
    "version": "14.0.1.0.6",
    "category": "Localization/Italy",
    "author": "Link It srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",  # Depends on AGPL modules
    "depends": ["l10n_it_account"],
    "data": [
        "views/fiscal_document_type_view.xml",
        "views/res_partner_view.xml",
        "views/account_move_view.xml",
        "views/account_view.xml",
        "data/fiscal.document.type.csv",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
