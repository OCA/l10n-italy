from openupgradelib import openupgrade
from openupgradelib.openupgrade_tools import column_exists


@openupgrade.migrate()
def migrate(env, version):
    table = "account_fiscal_position"
    model = "account.fiscal.position"
    old_single_column = "l10n_it_oca_intrastat"
    for old_column, new_column in (
        ("intrastat_sale", "l10n_it_oca_intrastat_sale"),
        ("intrastat_purchase", "l10n_it_oca_intrastat_purchase"),
    ):
        if column_exists(env.cr, table, new_column):
            # Already migrated or installed with the split fields: keep them.
            continue
        if column_exists(env.cr, table, old_column):
            # 14.0/16.0 split flag: preserve its value.
            openupgrade.rename_fields(
                env,
                [
                    (
                        model,
                        table,
                        old_column,
                        new_column,
                    )
                ],
            )
        elif column_exists(env.cr, table, old_single_column):
            # 18.0 single flag: create and populate the split column.
            openupgrade.add_fields(
                env,
                [
                    (
                        new_column,
                        model,
                        False,
                        "boolean",
                        False,
                        "l10n_it_intrastat",
                    )
                ],
            )
            openupgrade.logged_query(
                env.cr,
                f"""
                UPDATE {table}
                SET {new_column} = {old_single_column}
                WHERE {old_single_column} IS TRUE
                """,
            )
