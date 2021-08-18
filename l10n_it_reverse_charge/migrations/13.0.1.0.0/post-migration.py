#  Copyright 2021 Simone Vanin - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_reverse_charge", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )

    openupgrade.logged_query(
        cr,
        """
update account_move
set
    rc_self_invoice_id = inv.rc_self_invoice_id,
    rc_purchase_invoice_id = inv.rc_purchase_invoice_id,
    rc_self_purchase_invoice_id = inv.rc_self_purchase_invoice_id
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )

    openupgrade.logged_query(
        cr,
        """
update account_move_line aml
set
    rc = invl.rc
from account_invoice_line invl
    join account_invoice inv on inv.id = invl.invoice_id
where
    aml.move_id = inv.move_id;
    """,
    )
