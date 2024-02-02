# Copyright 2023 Michele Rusticucci <https://github.com/michelerusti>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade
from psycopg2 import sql


@openupgrade.migrate()
def migrate(env, version):
    table_name = "wizard_export_fatturapa"
    constraint_name = "wizard_export_fatturapa_report_print_menu_fkey"

    env.cr.execute(
        """
            SELECT constraint_name
            FROM information_schema.table_constraints
            WHERE constraint_type = 'FOREIGN KEY' AND table_name = %s
            AND constraint_name = %s
        """,
        (table_name, "%s" % constraint_name),
    )

    res = env.cr.fetchall()
    if res and res[0]:
        alter_table_sql = sql.SQL("ALTER TABLE {} DROP CONSTRAINT {}").format(
            sql.Identifier(table_name), sql.Identifier(constraint_name)
        )
        drop_line_sql = "DELETE FROM ir_model_constraint WHERE NAME = %s"

        openupgrade.logged_query(env.cr, alter_table_sql)
        openupgrade.logged_query(env.cr, drop_line_sql, [constraint_name])
