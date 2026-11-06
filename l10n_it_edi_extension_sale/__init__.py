# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models
from openupgradelib import openupgrade


def _post_init_hook(env):
    if openupgrade.is_module_installed(env.cr, "l10n_it_fatturapa_sale"):
        openupgrade.logged_query(
            env.cr,
            """
                UPDATE account_move_related_document amrd
                SET
                    sale_order_id = frdt.sale_order_id,
                    sale_order_line_id = frdt.sale_order_line_id
                FROM
                    fatturapa_related_document_type frdt
                WHERE
                    (
                        frdt.sale_order_id IS NOT NULL
                        OR frdt.sale_order_line_id IS NOT NULL
                    )
                    AND (
                        amrd.invoice_id = frdt.invoice_id
                        OR amrd.invoice_line_id = frdt.invoice_line_id
                    )
            """,
        )
