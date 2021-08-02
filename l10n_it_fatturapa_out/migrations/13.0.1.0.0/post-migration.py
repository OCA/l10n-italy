from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.load_data(
        cr, "l10n_it_fatturapa_out", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )

    openupgrade.logged_query(
        cr,
        """
update account_move
set
    fatturapa_attachment_out_id = inv.fatturapa_attachment_out_id
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )
