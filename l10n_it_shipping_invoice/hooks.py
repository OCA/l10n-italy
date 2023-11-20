#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade
from openupgradelib.openupgrade import logged_query

from odoo.tools import DotDict

NEW_MODULE_NAME = "l10n_it_accompanying_invoice"
OLD_MODULE_NAME = "l10n_it_shipping_invoice"

RENAMED_FIELDS = [
    (
        "account.move",
        "account_move",
        "note",
        "delivery_note",
    ),
    (
        "account.move",
        "account_move",
        "date_done",
        "delivery_transport_datetime",
    ),
]

RENAMED_XMLIDS = [
    (
        "invoice_form_view_uom",
        "view_move_form",
    ),
    (
        "invoice_form_view_uom",
        "shipping_invoice_report",
    ),
    (
        "invoice_form_view_uom",
        "shipping_invoice_template",
    ),
    (
        "invoice_form_view_uom",
        "report_shipping_invoice",
    ),
]


def remove_models(cr, model_spec):
    for name in model_spec:
        logged_query(
            cr,
            "DELETE FROM ir_model WHERE model = %s",
            (name,),
        )


def migrate_old_module(cr):
    openupgrade.rename_fields(
        # The method only needs the cursor, not the whole Environment
        DotDict(
            cr=cr,
        ),
        RENAMED_FIELDS,
        # Prevent Environment usage
        # whenever it will be implemented.
        no_deep=True,
    )
    full_renamed_xmlids = [
        (
            ".".join((NEW_MODULE_NAME, old_xmlid)),
            ".".join((NEW_MODULE_NAME, new_xmlid)),
        )
        for old_xmlid, new_xmlid in RENAMED_XMLIDS
    ]
    openupgrade.rename_xmlids(
        cr,
        full_renamed_xmlids,
    )


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, OLD_MODULE_NAME):
        openupgrade.update_module_names(
            cr,
            [
                (OLD_MODULE_NAME, NEW_MODULE_NAME),
            ],
            merge_modules=True,
        )
        migrate_old_module(cr)
