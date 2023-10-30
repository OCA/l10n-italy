#  Copyright 2021 Simone Rubino - Agile Business Group
#  Copyright 2023 Sergio Corato
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql

from odoo.addons.l10n_it_declaration_of_intent import hooks


@openupgrade.migrate()
def migrate(env, version):
    # Used by OpenUpgrade when module is in `apriori`
    if not version:
        return
    # Update invoice_id in declaration line
    # from pointing to account.invoice
    # to pointing to account.move
    drop_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}")
    table = "dichiarazione_intento_line"
    column = "invoice_id"
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
    query = """
UPDATE dichiarazione_intento_line dil
SET
    invoice_id = ai.move_id
FROM account_invoice ai
JOIN account_move am on am.id = ai.move_id
WHERE
    ai.id = dil.invoice_id
"""
    openupgrade.logged_query(
        env.cr,
        query,
    )
    hooks.migrate_old_module(env.cr)
