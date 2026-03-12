from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import SUPERUSER_ID, api

from odoo.addons.l10n_it_account.migration_tools import (
    _remove_module,
    remove_modules_views,
)

OLD_MODULES = [
    "l10n_it_account_tax_kind",
    "l10n_it_declaration_of_intent",
    "l10n_it_fatturapa",
    "l10n_it_fatturapa_pec",
]

# Old OCA modules superseded in v18: split payment and reverse charge are now
# handled by Odoo core (l10n_it / account). We migrate no data for them here --
# we only drop their now-dangling views and uninstall them.
OLD_MODULES_TO_REMOVE = [
    "l10n_it_reverse_charge_start_end_dates",
    "l10n_it_reverse_charge",
    "l10n_it_split_payment",
]

# Old modules migrated here but uninstalled by their v18 replacement module
# (marked "to install" by the per-module migration functions below), so we must
# not remove them here:
#   l10n_it_declaration_of_intent -> l10n_it_edi_doi_extension
#   l10n_it_fatturapa_pec         -> l10n_it_edi_pec
MODULES_REMOVED_BY_REPLACEMENT = {
    "l10n_it_declaration_of_intent",
    "l10n_it_fatturapa_pec",
}


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


def _l10n_it_declaration_of_intent_migration(env):
    """
    Install "l10n_it_edi_doi_extension" which replaces the old
    l10n_it_declaration_of_intent module.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state = 'to install'
        WHERE name = 'l10n_it_edi_doi_extension'
        AND state = 'uninstalled'
        """,
    )


def _l10n_it_fatturapa_migration(env):
    # Remove exclusion for installation of "l10n_it_edi"
    query = """
        DELETE
        FROM ir_module_module_exclusion
        WHERE name = 'l10n_it_edi'
    """
    openupgrade.logged_query(env.cr, query)

    # Automatically install `l10n_it_edi_extension`
    # because it migrates the data of
    # `l10n_it_fatturapa` and several depending modules.
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET
            state = 'to install'
        WHERE
            name = 'l10n_it_edi_extension'
            AND state = 'uninstalled'
        """,
    )


def _l10n_it_fatturapa_pec_migration(env):
    """
    Install "l10n_it_edi_pec" which replaces the old
    l10n_it_fatturapa_pec module.
    """
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state = 'to install'
        WHERE name = 'l10n_it_edi_pec'
        AND state = 'uninstalled'
        """,
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in OLD_MODULES:
        migration_function = globals().get(f"_{module}_migration")
        if openupgrade.is_module_installed(env.cr, module) and migration_function:
            migration_function(env)
        if module not in MODULES_REMOVED_BY_REPLACEMENT:
            _remove_module(env, module)

    remove_modules_views(cr, OLD_MODULES_TO_REMOVE)
    for module in OLD_MODULES_TO_REMOVE:
        _remove_module(env, module)
