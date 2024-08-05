from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "account_move_line", "delivery_note_id"):
        openupgrade.copy_columns(
            env.cr,
            {"account_move_line": [("delivery_note_id", "old_delivery_note_id", None)]},
        )
