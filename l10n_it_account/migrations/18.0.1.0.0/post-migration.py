from openupgradelib import openupgrade
from psycopg2 import sql

from odoo import SUPERUSER_ID, api

OLD_MODULES = [
    "l10n_it_account_tax_kind",
    "l10n_it_fatturapa",
    "l10n_it_fiscalcode",
    "l10n_it_ipa",
    "l10n_it_rea",
]


def rename_fields(env, table, field_updates):
    """Generic function to rename fields."""
    set_clauses = ", ".join(
        f"{target_field} = {source_field}"
        for target_field, source_field in field_updates.items()
    )
    query = f"""
        UPDATE
            {table}
        SET
            {set_clauses}
    """
    openupgrade.logged_query(env.cr, sql.SQL(query))


def update_table(env, target_table, source_table, field_updates, condition):
    """Generic function to update fields in a table based on a join."""
    set_clauses = ", ".join(
        f"{target_field} = {source_table}.{source_field}"
        for target_field, source_field in field_updates.items()
    )
    query = f"""
        UPDATE
            {target_table}
        SET
            {set_clauses}
        FROM
            {source_table}
    """
    if condition:
        query += f"""
            WHERE
                {condition}
        """
    openupgrade.logged_query(env.cr, sql.SQL(query))


def _l10n_it_account_tax_kind_migration(env):
    rename_fields(
        env,
        table="account_tax",
        field_updates={"l10n_it_law_reference": "law_reference"},
    )

    condition = "account_tax.kind_id = account_tax_kind.id"
    condition += " AND account_tax.kind_id IS NOT NULL"
    update_table(
        env,
        target_table="account_tax",
        source_table="account_tax_kind",
        field_updates={"l10n_it_exempt_reason": "code"},
        condition=condition,
    )


def _l10n_it_fatturapa_migration(env):
    rename_fields(
        env,
        table="res_partner",
        field_updates={
            "l10n_it_pa_index": "codice_destinatario",
            "l10n_it_pec_email": "pec_destinatario",
        },
    )
    rename_fields(
        env,
        table="res_company",
        field_updates={
            "l10n_it_tax_representative_partner_id": "fatturapa_tax_representative",
        },
    )


def _l10n_it_fiscalcode_migration(env):
    rename_fields(
        env,
        table="res_partner",
        field_updates={"l10n_it_codice_fiscale": "fiscalcode"},
    )


def _l10n_it_ipa_migration(env):
    rename_fields(
        env,
        table="res_partner",
        field_updates={"l10n_it_pa_index": "ipa_code"},
    )


def _l10n_it_rea_migration(env):
    condition = "res_company.partner_id = res_partner.id"
    condition += " AND res_partner.rea_office IS NOT NULL"
    update_table(
        env,
        target_table="res_company",
        source_table="res_partner",
        field_updates={
            "l10n_it_eco_index_office": "rea_office",
            "l10n_it_eco_index_number": "rea_code",
            "l10n_it_eco_index_share_capital": "rea_capital",
            "l10n_it_eco_index_sole_shareholder": "rea_member_type",
            "l10n_it_eco_index_liquidation_state": "rea_liquidation_state",
        },
        condition=condition,
    )


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for module in OLD_MODULES:
        migration_function = globals().get(f"_{module}_migration")
        if openupgrade.is_module_installed(env.cr, module) and migration_function:
            migration_function(env)
