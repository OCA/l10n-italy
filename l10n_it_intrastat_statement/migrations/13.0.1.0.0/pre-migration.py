from openupgradelib import openupgrade
from psycopg2 import sql


def migrate(cr, installed_version):
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    to_be_updated = (
        ("account_intrastat_statement_sale_section1", "invoice_id"),
        ("account_intrastat_statement_sale_section2", "invoice_id"),
        ("account_intrastat_statement_sale_section3", "invoice_id"),
        ("account_intrastat_statement_sale_section4", "invoice_id"),
        ("account_intrastat_statement_purchase_section1", "invoice_id"),
        ("account_intrastat_statement_purchase_section2", "invoice_id"),
        ("account_intrastat_statement_purchase_section3", "invoice_id"),
        ("account_intrastat_statement_purchase_section4", "invoice_id"),
    )

    if openupgrade.table_exists(cr, "account_invoice"):
        for table, column in to_be_updated:
            cr.execute(
                """
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
                    AND constraint_name like %s
                """,
                (table, "%%%s%%" % "invoice_id"),
            )
            for constraint in (row[0] for row in cr.fetchall()):
                openupgrade.logged_query(
                    cr,
                    drop_sql.format(
                        sql.Identifier(table),
                        sql.Identifier(constraint),
                    ),
                )
            openupgrade.logged_query(
                cr,
                sql.SQL(
                    """UPDATE {table} t
                SET {column} = ai.move_id
                FROM account_invoice ai
                WHERE t.{column} = ai.id and ai.move_id is NOT NULL"""
                ).format(
                    table=sql.Identifier(table),
                    column=sql.Identifier(column),
                ),
            )
