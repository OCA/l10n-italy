#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.logged_query(
        cr,
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
        cr,
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
