from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(
        env.cr, "account_move", "old_invoice_id"
    ) and openupgrade.column_exists(env.cr, "account_invoice", "corrispettivo"):
        # l10n_it_corrispettivi handled sale receipts only
        openupgrade.logged_query(
            env.cr,
            "UPDATE account_move m "
            "SET move_type = 'out_receipt' "
            "FROM account_invoice i "
            "WHERE i.corrispettivo = true AND i.id = m.old_invoice_id",
        )

    if openupgrade.column_exists(env.cr, "account_journal", "corrispettivi"):
        openupgrade.logged_query(
            env.cr,
            "UPDATE account_journal "
            "SET receipts = true "
            "WHERE corrispettivi = true",
        )
