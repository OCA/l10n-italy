# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Delivery Note Comments",
    "summary": "Comments texts templates on Delivery Note",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Nextev Srl, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "l10n_it_delivery_note",
        "base_comment_template",
    ],
    "data": [
        "views/delivery_note_view.xml",
        "views/base_comment_template_view.xml",
        "views/report_delivery_note.xml",
        "data/res_config.xml",
    ],
}
