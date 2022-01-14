from openupgradelib import openupgrade
from psycopg2 import sql


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_intrastat_statement", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )

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
