#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, version):
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    env.cr.execute(
        """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
            AND constraint_name like %s
        """,
        ("account_invoice_intrastat", "%%%s%%" % "invoice_id"),
    )
    for constraint in (row[0] for row in env.cr.fetchall()):
        openupgrade.logged_query(
            env.cr,
            drop_sql.format(
                sql.Identifier("account_invoice_intrastat"),
                sql.Identifier(constraint),
            ),
        )
    if not openupgrade.column_exists(env.cr, "account_move", "intrastat"):
        openupgrade.add_fields(
            env,
            [
                (
                    "intrastat",
                    "account.move",
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
update account_move
set
    intrastat = inv.intrastat
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )

    openupgrade.logged_query(
        env.cr,
        """
update account_invoice_intrastat
set
    invoice_id = am.id
from account_invoice inv
    join account_move am on am.id = inv.move_id
where
    invoice_id = inv.id;
    """,
    )
