#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.add_fields(
        env,
        [("amount_sp", "account.move", False, "float", False, "l10n_it_split_payment")],
    )
    openupgrade.logged_query(
        env.cr,
        """
        update account_move
        set
            amount_sp = inv.amount_sp
        from account_invoice inv
        where
            account_move.id = inv.move_id;
    """,
    )
