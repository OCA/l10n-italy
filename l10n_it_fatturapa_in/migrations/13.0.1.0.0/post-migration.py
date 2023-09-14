#  Copyright 2021 Alfredo Zamora - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(
        env.cr, "l10n_it_fatturapa_in", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )
    openupgrade.logged_query(
        env.cr,
        """
update account_move
set
    fatturapa_attachment_in_id = inv.fatturapa_attachment_in_id,
    inconsistencies = inv.inconsistencies,
    e_invoice_amount_untaxed = inv.e_invoice_amount_untaxed,
    e_invoice_amount_tax = inv.e_invoice_amount_tax,
    e_invoice_amount_total = inv.e_invoice_amount_total,
    e_invoice_reference = inv.e_invoice_reference,
    e_invoice_date_invoice = inv.e_invoice_date_invoice,
    e_invoice_force_validation = inv.e_invoice_force_validation,
    e_invoice_received_date = inv.e_invoice_received_date
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )
