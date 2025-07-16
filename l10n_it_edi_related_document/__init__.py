# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from openupgradelib import openupgrade


def _insert_account_move_related_document(env):
    cr = env.cr
    cr.execute("SELECT * FROM fatturapa_related_document_type LIMIT 1")
    if cr.fetchone():
        cr.execute("""
            INSERT INTO account_move_related_document (
                type, name, "lineRef", invoice_id, invoice_line_id, date,
                numitem, code, cig, cup
            )
            SELECT
                type, name, "lineRef", invoice_id, invoice_line_id, date,
                numitem, code, cig, cup
            FROM fatturapa_related_document_type
        """)


def _l10n_it_edi_related_document_post_init_hook(env):
    module = "l10n_it_fatturapa"
    if openupgrade.is_module_installed(env.cr, module):
        _insert_account_move_related_document(env)
