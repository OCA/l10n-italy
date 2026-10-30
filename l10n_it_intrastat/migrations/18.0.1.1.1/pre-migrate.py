from openupgradelib import openupgrade
from openupgradelib.openupgrade_tools import column_exists


@openupgrade.migrate()
def migrate(env, version):
    table = "account_fiscal_position"
    column = "l10n_it_oca_intrastat"
    for old_column, new_column in (
        ["intrastat_sale", "l10n_it_oca_intrastat_sale"],
        ["intrastat_purchase", "l10n_it_oca_intrastat_purchase"],
    ):
        # 1. new installation: nothing to-do
        # 2. migration from v.16/v.18 without new fields:
        #  - create new fields and fill them with already renamed l10n_it_oca_intrastat
        if not column_exists(env.cr, table, new_column):
            if column_exists(env.cr, table, old_column):
                openupgrade.add_fields(
                    env,
                    [
                        (
                            new_column,
                            ".".join(table.split("_")),
                            False,
                            "boolean",
                            False,
                            "l10n_it_intrastat",
                        )
                    ],
                )
            # workaround: only fill from l10n_it_oca_intrastat when it exists
            if column_exists(env.cr, table, column):
                openupgrade.logged_query(
                    env.cr,
                    f"""
                        UPDATE {table}
                        SET
                            {new_column} = {column}
                        WHERE {column} is true;
                    """,
                )

        else:
            # 3. migration from v14/v16 with changes already done: rename fields only
            openupgrade.rename_fields(
                env,
                [
                    (
                        ".".join(table.split("_")),
                        table,
                        old_column,
                        new_column,
                    )
                ],
            )
