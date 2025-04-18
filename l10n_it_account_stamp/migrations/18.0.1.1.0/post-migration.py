#  Copyright 2025 Sergio Zanchetta
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move_line aml
        SET
           is_stamp_line = NULL
        WHERE aml.product_id IS NOT NULL AND aml.is_stamp_line = True
        """,
    )
