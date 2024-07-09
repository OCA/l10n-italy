from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    for table, column in [
        ("account_fiscal_position", "intrastat_sale"),
        ("account_fiscal_position", "intrastat_purchase"),
    ]:
        if not openupgrade.column_exists(env.cr, table, column):
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
                ],
            )
    openupgrade.logged_query(
        env.cr,
        """
UPDATE account_fiscal_position
SET
    intrastat_sale = intrastat,
    intrastat_purchase = intrastat
WHERE intrastat is true;
    """,
    )
