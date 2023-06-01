# Copyright 2020 Marco Colombo <https://github.com/TheMule71>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

# account_invoice -> account_move migration
i_m_columns = (
    ("fatturapa_payment_data", "invoice_id"),
    ("welfare_fund_data_line", "invoice_id"),
    ("withholding_data_line", "invoice_id"),
    ("discount_rise_price", "invoice_id"),
    ("fatturapa_related_document_type", "invoice_id"),
    ("faturapa_activity_progress", "invoice_id"),
    ("fatturapa_attachments", "invoice_id"),
    ("fatturapa_related_ddt", "invoice_id"),
    ("faturapa_summary_data", "invoice_id"),
)

invoice_data = (
    ("protocol_number"),
    ("tax_representative_id"),
    ("intermediary"),
    ("sender"),
    ("carrier_id"),
    ("transport_vehicle"),
    ("transport_reason"),
    ("number_items"),
    ("description"),
    ("unit_weight"),
    ("gross_weight"),
    ("net_weight"),
    ("pickup_datetime"),
    ("transport_date"),
    ("delivery_address"),
    ("delivery_datetime"),
    ("ftpa_incoterms"),
    ("related_invoice_code"),
    ("related_invoice_date"),
    ("vehicle_registration"),
    ("total_travel"),
    ("efatt_stabile_organizzazione_indirizzo"),
    ("efatt_stabile_organizzazione_civico"),
    ("efatt_stabile_organizzazione_cap"),
    ("efatt_stabile_organizzazione_comune"),
    ("efatt_stabile_organizzazione_provincia"),
    ("efatt_stabile_organizzazione_nazione"),
    ("efatt_rounding"),
    ("art73"),
)

# account_invoice_line -> account_move_line migration
il_ml_columns = (
    ("discount_rise_price", "invoice_line_id"),
    ("fatturapa_related_document_type", "invoice_line_id"),
    ("fatturapa_related_ddt", "invoice_line_id"),
)

invoice_line_data = (
    "admin_ref",
    "ftpa_line_number",
)


@openupgrade.migrate()
def migrate(env, version):
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    # check if it is a migration from 12.0
    if openupgrade.column_exists(env.cr, "account_move", "old_invoice_id"):
        for table, column in i_m_columns:
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
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET {1} = m.id
                FROM account_move m
                WHERE m.old_invoice_id = t.{1}"""
                ).format(
                    sql.Identifier(table),
                    sql.Identifier(column),
                ),
            )

    # check if it is a migration from 12.0
    if openupgrade.table_exists(
        env.cr, "account_invoice_line"
    ) and openupgrade.column_exists(env.cr, "account_move_line", "old_invoice_line_id"):
        for table, column in il_ml_columns:
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
            openupgrade.logged_query(
                env.cr,
                sql.SQL(
                    """UPDATE {0} t
                SET {1} = ml.id
                FROM account_move_line ml
                WHERE ml.old_invoice_line_id = t.{1}"""
                ).format(
                    sql.Identifier(table),
                    sql.Identifier(column),
                ),
            )
