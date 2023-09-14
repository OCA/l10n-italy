from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, installed_version):
    if not installed_version:
        return
    if openupgrade.table_exists(env.cr, "account_invoice"):
        if not openupgrade.column_exists(
            env.cr, "account_move", "fatturapa_attachment_out_id"
        ):
            openupgrade.add_fields(
                env,
                [
                    (
                        "fatturapa_attachment_out_id",
                        "account.move",
                        False,
                        "integer",
                        False,
                        "l10n_it_fatturapa_out",
                    )
                ],
            )
        openupgrade.logged_query(
            env.cr,
            """
    update account_move
    set
        fatturapa_attachment_out_id = inv.fatturapa_attachment_out_id
    from account_invoice inv
    where
        account_move.id = inv.move_id;
        """,
        )
