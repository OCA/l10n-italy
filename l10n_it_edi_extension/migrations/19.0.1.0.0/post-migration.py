# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tools.sql import SQL, column_exists, table_exists

_logger = logging.getLogger(__name__)


def _migrate_doc_attachments(cr):
    """Move the e-invoice attachments of 18.0 to the new list.

    In 18.0 each attachment is a `l10n_it_edi.attachment` record, wrapping an
    `ir.attachment` already linked to its invoice. Only customer invoices and
    credit notes are moved: the attachments of vendor bills come from the
    received XML, that is shown as it is, so they stay plain attachments.
    The invoice PDF that l10n_it_fatturapa_out added at the export
    (`is_pdf_invoice_print`), if the 16.0 table is still there, is skipped
    because l10n_it_edi already includes it.
    """
    if not table_exists(cr, "l10n_it_edi_attachment"):
        return
    skip_invoice_pdf = SQL()
    if column_exists(cr, "fatturapa_attachments", "is_pdf_invoice_print"):
        skip_invoice_pdf = SQL(
            """
            AND NOT EXISTS (
                SELECT 1
                FROM fatturapa_attachments fa
                WHERE fa.ir_attachment_id = la.ir_attachment_id
                    AND fa.is_pdf_invoice_print
            )
            """
        )
    cr.execute(
        SQL(
            """
        INSERT INTO account_move_l10n_it_edi_ext_doc_attachment_rel
            (move_id, attachment_id)
        SELECT DISTINCT la.invoice_id, la.ir_attachment_id
        FROM l10n_it_edi_attachment la
        JOIN account_move am ON am.id = la.invoice_id
        JOIN ir_attachment ia ON ia.id = la.ir_attachment_id
        WHERE am.move_type IN ('out_invoice', 'out_refund') %s
        ON CONFLICT DO NOTHING
        """,
            skip_invoice_pdf,
        )
    )
    _logger.info("%s e-invoice attachments moved to the new list", cr.rowcount)
    cr.execute(
        """
        UPDATE ir_attachment ia
        SET res_field = 'l10n_it_edi_ext_doc_attachment_ids'
        FROM account_move_l10n_it_edi_ext_doc_attachment_rel rel
        WHERE ia.id = rel.attachment_id
            AND ia.res_model = 'account.move'
            AND ia.res_id = rel.move_id
            AND ia.res_field IS NULL
        """
    )


def migrate(cr, version):
    _migrate_doc_attachments(cr)
