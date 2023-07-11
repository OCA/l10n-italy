from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, installed_version):
    if not installed_version:
        return
    if openupgrade.table_exists(env.cr, "account_invoice"):
        openupgrade.logged_query(
            env.cr,
            """
        ALTER TABLE account_invoice
            ADD COLUMN IF NOT EXISTS amount_net_pay_residual numeric
        """,
        )
    # update invoice_line_id in table account_invoice_line_tax_wt
    # and invoice_id in account_invoice_withholding_tax and withholding_tax_statement
    if openupgrade.column_exists(env.cr, "account_move_line", "old_invoice_line_id"):
        drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
        for table, column in [
            ("account_invoice_line_tax_wt", "invoice_line_id"),
            ("account_invoice_withholding_tax", "invoice_id"),
            ("withholding_tax_statement", "invoice_id"),
        ]:
            env.cr.execute(
                """
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
                    AND constraint_name like %s
                """,
                (table, "%%%s%%" % column),
            )
            for constraint in (row[0] for row in env.cr.fetchall()):
                openupgrade.logged_query(
                    env.cr,
                    drop_sql.format(
                        sql.Identifier(table),
                        sql.Identifier(constraint),
                    ),
                )
            if table == "account_invoice_line_tax_wt":
                query = """
                    UPDATE {table}
                    SET
                        invoice_line_id = aml.id
                    FROM account_invoice_line invl
                        JOIN account_move_line aml ON aml.old_invoice_line_id = invl.id
                    WHERE
                        invoice_line_id = invl.id
                """.format(
                    table=table
                )
                openupgrade.logged_query(
                    env.cr,
                    query,
                )
            else:
                query = """
                    UPDATE {table}
                    SET
                        invoice_id = am.id
                    FROM account_invoice inv
                        JOIN account_move am ON am.old_invoice_id = inv.id
                    WHERE
                        invoice_id = inv.id
                """.format(
                    table=table
                )
                openupgrade.logged_query(
                    env.cr,
                    query,
                )
