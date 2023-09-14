# Copyright 2023 Sergio Corato
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

invoice_data = ("comunicazione_dati_iva_escludi",)


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(
        env.cr, "account_move", "comunicazione_dati_iva_escludi"
    ):
        openupgrade.add_fields(
            env,
            [
                (
                    "comunicazione_dati_iva_escludi",
                    "account.move",
                    False,
                    "boolean",
                    False,
                    "l10n_it_invoices_data_communication",
                )
            ],
        )
    # remove constraint for invoice_id
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    for table in [
        "comunicazione_dati_iva_fatture_ricevute_body",
        "comunicazione_dati_iva_fatture_emesse_body",
    ]:
        env.cr.execute(
            """
                SELECT constraint_name
                FROM information_schema.table_constraints
                WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
                AND constraint_name like %s
            """,
            (table, "%%%s%%" % "invoice_id"),
        )
        for constraint in (row[0] for row in env.cr.fetchall()):
            openupgrade.logged_query(
                env.cr,
                drop_sql.format(
                    sql.Identifier(table),
                    sql.Identifier(constraint),
                ),
            )
        # update invoice_id ref in table
        query = """
            UPDATE {table}
            SET
                invoice_id = am.id
            FROM account_invoice inv
                JOIN account_move am ON am.id = inv.move_id
            WHERE
                invoice_id = inv.id
        """.format(
            table=table
        )
        openupgrade.logged_query(
            env.cr,
            query,
        )
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
