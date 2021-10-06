from openupgradelib import openupgrade  # pylint: disable=W7936


def migrate(cr, installed_version):
    openupgrade.logged_query(
        cr,
        """
update invoice_unsolved_line_rel iulr
set
    move_id = am.id
from account_invoice inv
    join account_move am on am.id = inv.move_id
where
    iulr.move_id = inv.id;
    """,
    )
