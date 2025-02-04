from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import SUPERUSER_ID, api

OLD_MODULES = [
    "l10n_it_account_tax_kind",
    "l10n_it_fatturapa",
    "l10n_it_fiscalcode",
    "l10n_it_ipa",
    "l10n_it_pec",
    "l10n_it_rea",
]


def rename_fields(env, table, field_updates, condition=None):
    """Generic function to rename fields."""
    set_clauses = sql.SQL(", ").join(
        sql.SQL("{} = {}").format(sql.Identifier(target), sql.Identifier(source))
        for target, source in field_updates.items()
    )
    query = sql.SQL("""
        UPDATE {table}
        SET {set_clauses}
    """).format(table=sql.Identifier(table), set_clauses=set_clauses)
    if condition:
        query += sql.SQL(" WHERE {} ").format(sql.SQL(condition))
    openupgrade.logged_query(env.cr, query)


def update_table(env, target_table, source_table, field_updates, condition):
    """Generic function to update fields in a table based on a join."""
    set_clauses = sql.SQL(", ").join(
        sql.SQL("{} = {}.{}").format(
            sql.Identifier(target), sql.Identifier(source_table), sql.Identifier(source)
        )
        for target, source in field_updates.items()
    )
    query = sql.SQL("""
        UPDATE {target_table}
        SET {set_clauses}
        FROM {source_table}
    """).format(
        target_table=sql.Identifier(target_table),
        set_clauses=set_clauses,
        source_table=sql.Identifier(source_table),
    )
    if condition:
        query += sql.SQL(" WHERE {} ").format(sql.SQL(condition))
    openupgrade.logged_query(env.cr, query)


def add_field_if_not_exists(env, table, field_name, field_type, module):
    """Helper function to add fields if they do not exist."""
    if not openupgrade.column_exists(env.cr, table, field_name):
        sql_type_mapping = {
            "binary": "bytea",
            "boolean": "bool",
            "char": "varchar",
            "date": "date",
            "datetime": "timestamp",
            "float": "numeric",
            "html": "text",
            "integer": "int4",
            "many2many": False,
            "many2one": "int4",
            "many2one_reference": "int4",
            "monetary": "numeric",
            "one2many": False,
            "reference": "varchar",
            "selection": "varchar",
            "text": "text",
            "serialized": "text",
        }
        openupgrade.add_fields(
            env,
            [
                (
                    field_name,
                    table.replace("_", "."),
                    table,
                    field_type,
                    sql_type_mapping[field_type],
                    module,
                )
            ],
        )


def _l10n_it_account_tax_kind_migration(env):
    table = "account_tax"
    add_field_if_not_exists(env, table, "l10n_it_law_reference", "char", "l10n_it")
    rename_fields(env, table, {"l10n_it_law_reference": "law_reference"})

    add_field_if_not_exists(env, table, "l10n_it_exempt_reason", "char", "l10n_it")
    condition = "account_tax.kind_id = account_tax_kind.id"
    condition += " AND account_tax.kind_id IS NOT NULL"
    update_table(
        env, table, "account_tax_kind", {"l10n_it_exempt_reason": "code"}, condition
    )


def _l10n_it_fatturapa_migration(env):
    table = "res_partner"
    add_field_if_not_exists(env, table, "l10n_it_pa_index", "char", "l10n_it_edi")
    add_field_if_not_exists(env, table, "l10n_it_pec_email", "char", "l10n_it_edi")
    rename_fields(
        env,
        table,
        {
            "l10n_it_pa_index": "codice_destinatario",
            "l10n_it_pec_email": "pec_destinatario",
        },
    )

    table = "res_company"
    add_field_if_not_exists(
        env, table, "l10n_it_tax_representative_partner_id", "many2one", "l10n_it_edi"
    )
    rename_fields(
        env,
        table,
        {"l10n_it_tax_representative_partner_id": "fatturapa_tax_representative"},
    )


def _l10n_it_fiscalcode_migration(env):
    table = "res_partner"
    add_field_if_not_exists(env, table, "l10n_it_codice_fiscale", "char", "l10n_it_edi")
    rename_fields(env, table, {"l10n_it_codice_fiscale": "fiscalcode"})


def _l10n_it_ipa_migration(env):
    table = "res_partner"
    add_field_if_not_exists(env, table, "l10n_it_pa_index", "char", "l10n_it_edi")
    condition = "ipa_code IS NOT NULL"
    rename_fields(env, table, {"l10n_it_pa_index": "ipa_code"}, condition=condition)


def _l10n_it_pec_migration(env):
    table = "res_partner"
    add_field_if_not_exists(env, table, "l10n_it_pec_email", "char", "l10n_it_edi")
    condition = "pec_mail IS NOT NULL"
    rename_fields(env, table, {"l10n_it_pec_email": "pec_mail"}, condition=condition)


def _l10n_it_rea_migration(env):
    table = "res_company"
    add_field_if_not_exists(
        env, table, "l10n_it_eco_index_office", "many2one", "l10n_it_edi"
    )
    add_field_if_not_exists(
        env, table, "l10n_it_eco_index_number", "char", "l10n_it_edi"
    )
    add_field_if_not_exists(
        env, table, "l10n_it_eco_index_share_capital", "float", "l10n_it_edi"
    )
    add_field_if_not_exists(
        env, table, "l10n_it_eco_index_sole_shareholder", "selection", "l10n_it_edi"
    )
    add_field_if_not_exists(
        env, table, "l10n_it_eco_index_liquidation_state", "selection", "l10n_it_edi"
    )
    condition = "res_company.partner_id = res_partner.id"
    condition += " AND res_partner.rea_office IS NOT NULL"
    update_table(
        env,
        table,
        "res_partner",
        {
            "l10n_it_eco_index_office": "rea_office",
            "l10n_it_eco_index_number": "rea_code",
            "l10n_it_eco_index_share_capital": "rea_capital",
            "l10n_it_eco_index_sole_shareholder": "rea_member_type",
            "l10n_it_eco_index_liquidation_state": "rea_liquidation_state",
        },
        condition,
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in OLD_MODULES:
        migration_function = globals().get(f"_{module}_migration")
        if openupgrade.is_module_installed(env.cr, module) and migration_function:
            migration_function(env)
