# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from openupgradelib import openupgrade


def _insert_account_move_related_document(cr, version):
    cr.execute("SELECT * FROM fatturapa_related_document_type LIMIT 1")
    if cr.fetchone():
        openupgrade.logged_query(
            cr,
            """
            INSERT INTO account_move_related_document (
                type, name, lineRef, invoice_id, invoice_line_id, date,
                numitem, code, cig, cup
            )
            SELECT
                type, name, lineRef, invoice_id, invoice_line_id, date,
                numitem, code, cig, cup
            FROM fatturapa_related_document_type
            """,
        )


@openupgrade.migrate()
def migrate(cr, version):
    _insert_account_move_related_document(cr)
