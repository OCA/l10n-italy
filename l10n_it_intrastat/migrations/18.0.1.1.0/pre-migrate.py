from openupgradelib import openupgrade
from openupgradelib.openupgrade_tools import column_exists


@openupgrade.migrate()
def migrate(env, version):
    table = "account_fiscal_position"
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
            openupgrade.logged_query(
                env.cr,
                f"""
                    UPDATE account_fiscal_position
                    SET
                        {new_column} = l10n_it_oca_intrastat,
                    WHERE l10n_it_oca_intrastat is true;
                """,
            )

        else:
            # 3. migration from v14/v16 with changes already done: rename fields only
            openupgrade.rename_fields(
                env,
                [
                    (
                        "account.fiscal.position",
                        table,
                        old_column,
                        new_column,
                    )
                ],
            )
