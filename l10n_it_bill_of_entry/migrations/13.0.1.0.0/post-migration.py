#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

INVOICE_LINE_FIELDS = [
    "advance_customs_vat",
]
INVOICE_FIELDS = {
    "simple_fields": [
        "customs_doc_type",
        "bill_of_entry_storno_id",
    ],
    "m2o_invoice": [
        "forwarder_invoice_id",
    ],
}


def _get_set_clause(fields_list, table_alias):
    set_fields_list = [
        "{f} = {second_table}.{f}".format(
            second_table=table_alias,
            f=field,
        )
        for field in fields_list
    ]
    set_fields_clause = ", ".join(set_fields_list)
    return set_fields_clause


def migrate_invoice_line_values(cr):
    set_fields_clause = _get_set_clause(INVOICE_LINE_FIELDS, "ail")
    query = """
UPDATE account_move_line aml
SET {fields}
FROM account_invoice_line ail
WHERE aml.old_invoice_line_id = ail.id
    """.format(
        fields=set_fields_clause,
    )
    return openupgrade.logged_query(cr, query)


def migrate_invoice_simple_values(cr):
    set_fields_clause = _get_set_clause(INVOICE_FIELDS.get("simple_fields"), "ai")
    query = """
UPDATE account_move am
SET {fields}
FROM account_invoice ai
WHERE am.old_invoice_id = ai.id
    """.format(
        fields=set_fields_clause,
    )
    return openupgrade.logged_query(cr, query)


def migrate_invoice_m2o_invoice_values(cr):
    for field in INVOICE_FIELDS.get("m2o_invoice"):
        query = """
UPDATE account_move am
SET {field} = am2.id
FROM account_invoice ai
JOIN account_move am2
    ON am2.old_invoice_id = ai.{field}
WHERE am.old_invoice_id = ai.id
        """.format(
            field=field,
        )
        openupgrade.logged_query(cr, query)
    return True


def migrate_invoice_sboe_rel(cr):
    new_table_name = "sboe_invoice_rel"
    old_table_name = openupgrade.get_legacy_name(new_table_name)
    query = """
INSERT INTO {new_table_name}
SELECT
    sboe_move.id as sboe_id,
    invoice_move.id as invoice_id
FROM {old_table_name} old_sboe_table
JOIN account_move sboe_move
    ON old_sboe_table.sboe_id = sboe_move.old_invoice_id
JOIN account_move invoice_move
    ON old_sboe_table.invoice_id = invoice_move.old_invoice_id
        """.format(
        new_table_name=new_table_name,
        old_table_name=old_table_name,
    )
    return openupgrade.logged_query(cr, query)


def migrate(cr, installed_version):
    migrate_invoice_line_values(cr)
    migrate_invoice_simple_values(cr)
    migrate_invoice_m2o_invoice_values(cr)
    migrate_invoice_sboe_rel(cr)
