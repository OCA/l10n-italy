from openupgradelib import openupgrade  # pylint: disable=W7936


def migrate(cr, installed_version):
    if not openupgrade.column_exists(cr, "invoice_unsolved_line_rel", "move_id"):
        openupgrade.logged_query(
            cr,
            """ALTER TABLE invoice_unsolved_line_rel
               ADD COLUMN move_id int""",
        )
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

    # delete action_wizard_riba_file_export which has been changed from act_window
    # to ir.actions.server
    renamed_act_window = "l10n_it_ricevute_bancarie.action_wizard_riba_file_export"
    openupgrade.logged_query(
        cr,
        """
DELETE FROM ir_model_data
WHERE module=%s AND name=%s
""",
        tuple(renamed_act_window.split(".")),
    )
