from openupgradelib import openupgrade


def migrate(cr, installed_version):
    if not installed_version:
        return
    if openupgrade.table_exists(cr, "account_invoice"):
        openupgrade.logged_query(
            cr,
            """
        ALTER TABLE account_invoice
            ADD COLUMN IF NOT EXISTS amount_net_pay_residual numeric
        """,
        )
