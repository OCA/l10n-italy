from openupgradelib import openupgrade  # pylint: disable=W7936


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_withholding_tax", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )

    openupgrade.logged_query(
        cr,
        """
update account_move
set
    withholding_tax = inv.withholding_tax,
    withholding_tax_amount = inv.withholding_tax_amount,
    amount_net_pay = inv.amount_net_pay,
    amount_net_pay_residual = inv.amount_net_pay_residual
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )

    openupgrade.logged_query(
        cr,
        """
update account_invoice_withholding_tax
set
    invoice_id = am.id
from account_invoice inv
    join account_move am on am.id = inv.move_id
where
    invoice_id = inv.id;
    """,
    )
