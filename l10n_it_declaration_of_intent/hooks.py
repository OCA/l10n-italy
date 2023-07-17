#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import SUPERUSER_ID, api

OLD_MODULE_NAME = "l10n_it_dichiarazione_intento"
NEW_MODULE_NAME = "l10n_it_declaration_of_intent"


def migrate_old_module(cr):
    """
    Move data and fields
    from italian module `l10n_it_dichiarazione_intento`
    to this module.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    old_sequence = env["ir.model.data"].get_object(
        NEW_MODULE_NAME, "dichiarazione_intento_seq"
    )
    old_sequence.code = "declaration_of_intent"

    renamed_fields = [
        (
            "res.company",
            "res_company",
            "dichiarazione_yearly_limit_ids",
            "declaration_yearly_limit_ids",
        ),
        (
            "dichiarazione.intento.yearly.limit",
            "dichiarazione_intento_yearly_limit",
            "dichiarazione_id",
            "declaration_id",
        ),
        (
            "dichiarazione.intento.line",
            "dichiarazione_intento_line",
            "dichiarazione_id",
            "declaration_id",
        ),
        (
            "account.fiscal.position",
            "account_fiscal_position",
            "valid_for_dichiarazione_intento",
            "valid_for_declaration_of_intent",
        ),
        (
            "account.move.line",
            "account_move_line",
            "force_dichiarazione_intento_id",
            "force_declaration_of_intent_id",
        ),
        (
            "account.move",
            "account_move",
            "dichiarazione_intento_ids",
            "declaration_of_intent_ids",
        ),
    ]
    openupgrade.rename_fields(
        env,
        renamed_fields,
    )

    renamed_models = [
        (
            "dichiarazione.intento.yearly.limit",
            "l10n_it_declaration_of_intent.yearly_limit",
        ),
        ("dichiarazione.intento", "l10n_it_declaration_of_intent.declaration"),
        (
            "dichiarazione.intento.line",
            "l10n_it_declaration_of_intent.declaration_line",
        ),
    ]
    openupgrade.rename_models(
        cr,
        renamed_models,
    )
    renamed_tables = [
        (
            old_model.replace(".", "_"),
            new_model.replace(".", "_"),
        )
        for old_model, new_model in renamed_models
    ]
    openupgrade.rename_tables(
        cr,
        renamed_tables,
    )

    renamed_xmlids = [
        ("access_dichiarazione_intento", "access_declaration_of_intent"),
        ("access_dichiarazione_intento_base", "access_declaration_of_intent_base"),
        ("access_dichiarazione_intento_line", "access_declaration_of_intent_line"),
        (
            "access_dichiarazione_intento_yearly_limit",
            "access_declaration_of_intent_yearly_limit",
        ),
        ("dichiarazione_intento_seq", "declaration_of_intent_seq"),
        ("dichiarazione_intento_invoice_form", "declaration_of_intent_invoice_form"),
        (
            "dichiarazione_intento_invoice_line_form",
            "declaration_of_intent_invoice_line_form",
        ),
        (
            "dichiarazione_intento_account_position_form",
            "declaration_of_intent_account_position_form",
        ),
        (
            "dichiarazione_intento_view_company_form",
            "declaration_of_intent_view_company_form",
        ),
        ("dichiarazione_intento_form", "declaration_of_intent_form"),
        ("dichiarazione_intento_search", "declaration_of_intent_search"),
        ("dichiarazione_intento_tree", "declaration_of_intent_tree"),
        ("dichiarazione_intento_action", "declaration_of_intent_action"),
        ("dichiarazione_intento_menu", "declaration_of_intent_menu"),
    ]
    renamed_xmlids = [
        (".".join([NEW_MODULE_NAME, old_xmlid]), ".".join([NEW_MODULE_NAME, new_xmlid]))
        for (old_xmlid, new_xmlid) in renamed_xmlids
    ]
    openupgrade.rename_xmlids(
        cr,
        renamed_xmlids,
    )

    # Copy value of force_declaration_of_intent_id
    # from account_invoice_line
    # to corresponding account_move_line
    query = """
UPDATE account_move_line aml
SET
    force_declaration_of_intent_id = ail.force_dichiarazione_intento_id
FROM account_invoice_line ail
    JOIN account_invoice ai ON ai.id = ail.invoice_id
    JOIN account_move am ON am.id = ai.move_id
WHERE
    aml.move_id = am.id
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


def copy_m2m_values(cr, registry):

    # List of tuples
    # (old_relation_table, old_model_column, old_comodel_column,
    # new_relation_table, new_model_column, new_comodel_column)
    m2m_fields = [
        # Field l10n_it_declaration_of_intent.declaration.taxes_ids
        (
            "account_tax_dichiarazione_intento_rel",
            "dichiarazione_intento_id",
            "account_tax_id",
            "account_tax_l10n_it_declaration_of_intent_declaration_rel",
            "l10n_it_declaration_of_intent_declaration_id",
            "account_tax_id",
        ),
        # Field l10n_it_declaration_of_intent.declaration_line.taxes_ids
        (
            "account_tax_dichiarazione_intento_line_rel",
            "dichiarazione_intento_line_id",
            "account_tax_id",
            "account_tax_l10n_it_declaration_of_intent_declaration_line_rel",
            "l10n_it_declaration_of_intent_declaration_line_id",
            "account_tax_id",
        ),
        # Field l10n_it_declaration_of_intent.declaration_line.move_line_ids
        (
            "account_move_line_dichiarazione_intento_line_rel",
            "dichiarazione_intento_line_id",
            "account_move_line_id",
            "move_line_declaration_line_rel",
            "l10n_it_declaration_of_intent_declaration_line_id",
            "account_move_line_id",
        ),
    ]

    # Copy m2m values from old table
    query = sql.SQL(
        """
INSERT INTO {new_relation_table}
    ({new_model_column}, {new_comodel_column})
SELECT
    rel.{old_model_column},
    rel.{old_comodel_column}
FROM {old_relation_table} rel
"""
    )
    for (
        old_relation_table,
        old_model_column,
        old_comodel_column,
        new_relation_table,
        new_model_column,
        new_comodel_column,
    ) in m2m_fields:
        if not openupgrade.table_exists(cr, old_relation_table):
            continue
        openupgrade.logged_query(
            cr,
            query.format(
                old_relation_table=sql.Identifier(old_relation_table),
                old_model_column=sql.Identifier(old_model_column),
                old_comodel_column=sql.Identifier(old_comodel_column),
                new_relation_table=sql.Identifier(new_relation_table),
                new_model_column=sql.Identifier(new_model_column),
                new_comodel_column=sql.Identifier(new_comodel_column),
            ),
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
