#  Copyright 2022 Alex Comba - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        update account_move
        set
            tax_stamp = inv.tax_stamp
        from account_invoice inv
        where
            account_move.id = inv.move_id;
    """,
    )
