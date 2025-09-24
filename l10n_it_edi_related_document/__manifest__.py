# Copyright 2025 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Related Documents for EDI",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Nextev Srl, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["l10n_it_edi"],
    "data": [
        "views/related_document_views.xml",
        "views/l10n_it_views.xml",
        "views/account_move_related_documents.xml",
        "data/invoice_it_template.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "post_init_hook": "_l10n_it_edi_related_document_post_init_hook",
}
