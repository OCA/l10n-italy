# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Italy - E-invoicing - Integrazione vendite",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Nextev Srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_edi_sale",
        "l10n_it_edi_extension",
        "l10n_it_edi_related_document",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
    ],
    "installable": True,
    "post_init_hook": "_post_init_hook",
}
