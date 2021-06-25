from openupgradelib import openupgrade
from psycopg2 import sql

invoice_data = ("comunicazione_dati_iva_escludi",)


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "account_move", "old_invoice_id"):
        openupgrade.logged_query(
            env.cr,
            sql.SQL(
                """UPDATE account_move m
                   SET {}
                   FROM account_invoice i
                   WHERE m.old_invoice_id = i.id
                """
            ).format(
                sql.SQL(", ").join(
                    sql.Composed(
                        [
                            sql.Identifier(col),
                            sql.SQL(" = "),
                            sql.SQL("i."),
                            sql.Identifier(col),
                        ]
                    )
                    for col in invoice_data
                )
            ),
        )

    elif openupgrade.table_exists(env.cr, "account_invoice"):
        openupgrade.logged_query(
            env.cr,
            sql.SQL(
                """UPDATE account_move m
                                   SET {}
                                   FROM account_invoice i
                                   WHERE i.move_id = m.id
                                """
            ).format(
                sql.SQL(", ").join(
                    sql.Composed(
                        [
                            sql.Identifier(col),
                            sql.SQL(" = "),
                            sql.SQL("i."),
                            sql.Identifier(col),
                        ]
                    )
                    for col in invoice_data
                )
            ),
        )
