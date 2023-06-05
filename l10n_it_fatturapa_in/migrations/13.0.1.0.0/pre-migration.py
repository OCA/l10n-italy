#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


def migrate(cr, installed_version):
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    table = "einvoice_line"
    column = "invoice_id"
    cr.execute(
        """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
            AND constraint_name like %s
        """,
        (table, "%%%s%%" % column),
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
        """
update einvoice_line eil
set
    invoice_id = am.id
from account_invoice inv
    join account_move am on am.id = inv.move_id
where
    eil.invoice_id = inv.id;
    """,
    )
