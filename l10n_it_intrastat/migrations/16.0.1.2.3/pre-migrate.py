from openupgradelib import openupgrade
from openupgradelib.openupgrade_tools import column_exists


@openupgrade.migrate()
def migrate(env, version):
    table = "account_fiscal_position"
    old_column = "intrastat"
    new_columns = ("intrastat_sale", "intrastat_purchase")
    if not column_exists(env.cr, table, old_column):
        return
    columns_to_fill = [
        column for column in new_columns if not column_exists(env.cr, table, column)
    ]
    if not columns_to_fill:
        return
    openupgrade.add_fields(
        env,
        [
            (
                column,
                ".".join(table.split("_")),
                False,
                "boolean",
                False,
                "l10n_it_intrastat",
            )
            for column in columns_to_fill
        ],
    )
    for column in columns_to_fill:
        openupgrade.logged_query(
            env.cr,
            f"""
            UPDATE {table}
            SET {column} = {old_column}
            WHERE {old_column} IS TRUE
            """,
        )
