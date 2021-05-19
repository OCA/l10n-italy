#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def copy_invoice_m2m_values(
    env, field_name, old_relation_table=None, old_comodel_column=None
):
    """
    Copy values for m2m field `field_name`
    from account.invoice to account.move.

    :param env: Odoo Environment
    :param field_name: name of the new field
    :param old_relation_table: name of the relation for the old field
    :param old_comodel_column: name of the comodel for the old field
    """
    old_model_name = "account.invoice"
    new_model_name = "account.move"
    field = env[new_model_name]._fields[field_name]
    new_model_column = field.column1
    new_comodel_column = field.column2
    old_comodel_column = old_comodel_column or new_comodel_column

    new_relation_table = field.relation
    if not old_relation_table:
        old_relation_table = new_relation_table.replace(
            new_model_name.replace(".", "_"),
            old_model_name.replace(".", "_"),
        )
    query = """
INSERT INTO %(new_relation_table)s
    (%(new_model_column)s, %(new_comodel_column)s)
VALUES (
    SELECT
        am.id,
        rel.%(old_comodel_column)s
    FROM %(old_relation_table)s rel
    JOIN account_invoice ai ON ai.id = rel.account_invoice_id
    JOIN account_move am on am.id = ai.move_id
)
"""
    return openupgrade.logged_query(
        env.cr,
        query,
        dict(
            new_model_column=new_model_column,
            new_comodel_column=new_comodel_column,
            new_relation_table=new_relation_table,
            old_comodel_column=old_comodel_column,
            old_relation_table=old_relation_table,
        ),
    )


@openupgrade.migrate()
def migrate(env, version):
    # Copy link between invoice and declaration
    copy_invoice_m2m_values(
        env,
        "declaration_of_intent_ids",
        old_relation_table="account_invoice_dichiarazione_intento_rel",
        old_comodel_column="declaration_of_intent_id",
    )

    # Copy value of force_declaration_of_intent_id
    # from account_invoice_line
    # to corresponding account_move_line
    query = """
UPDATE account_move_line
SET
    force_declaration_of_intent_id = ail.force_declaration_of_intent_id
FROM account_invoice_line ail
    JOIN account_invoice ai ON ai.id = ail.invoice_id
    JOIN account_move am ON am.id = ai.move_id
WHERE
    move_id = am.id
    AND aml.tax_line_id IS NULL
    AND aml.account_id <> ai.account_id
    AND ail.quantity = aml.quantity
    AND ((ail.product_id IS NULL AND aml.product_id IS NULL)
        OR ail.product_id = aml.product_id)
    AND ((ail.uom_id IS NULL AND aml.product_uom_id IS NULL)
        OR ail.uom_id = aml.product_uom_id)
"""
    openupgrade.logged_query(
        env.cr,
        query,
    )

    # Update invoice_id in declaration line
    # from pointing to account.invoice
    # to pointing to account.move
    query = """
UPDATE l10n_it_declaration_of_intent_declaration_line
SET
    invoice_id = ai.move_id
FROM account_invoice ai
WHERE
    ai.id = invoice_id
"""
    openupgrade.logged_query(
        env.cr,
        query,
    )
