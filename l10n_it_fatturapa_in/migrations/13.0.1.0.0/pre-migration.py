#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openupgradelib import openupgrade
from psycopg2 import sql

_logger = logging.getLogger(__name__)


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
    cr.execute(
        """
            SELECT eil.invoice_id, inv.move_id, eil.id
            FROM einvoice_line eil
            JOIN account_invoice inv ON inv.id = eil.invoice_id
            WHERE eil.invoice_id NOT IN (
                SELECT id FROM account_move
            )
        """,
    )
    res = cr.fetchall()
    for r in res:
        invoice_id, move_id, eil_id = r
        _logger.info(
            "Invoice with id %s and move id %s for einvoice_line id %s was not "
            "found, so it is linked to move_id found in invoice."
            % (invoice_id, move_id, eil_id)
        )
    if res:
        openupgrade.logged_query(
            cr,
            """
            UPDATE einvoice_line eil
            SET invoice_id = inv.move_id
            FROM account_invoice inv
            WHERE eil.invoice_id = inv.id
            AND eil.invoice_id NOT IN (
                SELECT id FROM account_move
            )
            """,
        )
