#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.tools import DotDict

RENAMED_FIELDS = [
    [
        (
            "account.invoice",
            "note",
        ),
        (
            "account.move",
            "delivery_note",
        ),
    ],
    [
        (
            "account.invoice",
            "date_done",
        ),
        (
            "account.move",
            "delivery_transport_datetime",
        ),
    ],
    [
        (
            "account.invoice",
            "carriage_condition_id",
        ),
        (
            "account.move",
            "delivery_transport_condition_id",
        ),
    ],
    [
        (
            "account.invoice",
            "goods_description_id",
        ),
        (
            "account.move",
            "delivery_goods_appearance_id",
        ),
    ],
    [
        (
            "account.invoice",
            "transportation_reason_id",
        ),
        (
            "account.move",
            "delivery_transport_reason_id",
        ),
    ],
    [
        (
            "account.invoice",
            "transportation_method_id",
        ),
        (
            "account.move",
            "delivery_transport_method_id",
        ),
    ],
    [
        (
            "account.invoice",
            "carrier_id",
        ),
        (
            "account.move",
            "delivery_carrier_id",
        ),
    ],
    [
        (
            "account.invoice",
            "parcels",
        ),
        (
            "account.move",
            "delivery_packages",
        ),
    ],
    [
        (
            "account.invoice",
            "weight",
        ),
        (
            "account.move",
            "delivery_net_weight",
        ),
    ],
    [
        (
            "account.invoice",
            "gross_weight",
        ),
        (
            "account.move",
            "delivery_gross_weight",
        ),
    ],
    [
        (
            "account.invoice",
            "volume",
        ),
        (
            "account.move",
            "delivery_volume",
        ),
    ],
    [
        (
            "account.invoice",
            "weight_manual_uom_id",
        ),
        (
            "account.move",
            "delivery_net_weight_uom_id",
        ),
    ],
    [
        (
            "account.invoice",
            "gross_weight_uom_id",
        ),
        (
            "account.move",
            "delivery_gross_weight_uom_id",
        ),
    ],
    [
        (
            "account.invoice",
            "volume_uom_id",
        ),
        (
            "account.move",
            "delivery_volume_uom_id",
        ),
    ],
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


# def remove_models(cr, model_spec):
#     for name in model_spec:
#         logged_query(
#             cr,
#             "DELETE FROM ir_model WHERE model = %s",
#             (name,),
#         )


def migrate_old_module(cr):
    field_spec = []
    for renamed_field in RENAMED_FIELDS:
        (old_model, old_field), (new_model, new_field) = renamed_field
        field_spec.append(
            (
                old_model,
                old_model.replace(".", "_"),
                old_field,
                new_field,
            )
        )
    openupgrade.rename_fields(
        # The method only needs the cursor, not the whole Environment
        DotDict(
            cr=cr,
        ),
        field_spec,
        # Prevent Environment usage
        # whenever it will be implemented.
        no_deep=True,
    )

    full_renamed_xmlids = [
        (
            ".".join(("l10n_it_accompanying_invoice", old_xmlid)),
            ".".join(("l10n_it_accompanying_invoice", new_xmlid)),
        )
        for old_xmlid, new_xmlid in RENAMED_XMLIDS
    ]
    openupgrade.rename_xmlids(
        cr,
        full_renamed_xmlids,
    )


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, "l10n_it_accompanying_invoice"):
        openupgrade.update_module_names(
            cr,
            [
                ("l10n_it_fattura_accompagnatoria", "l10n_it_accompanying_invoice"),
            ],
            merge_modules=True,
        )
        migrate_old_module(cr)
