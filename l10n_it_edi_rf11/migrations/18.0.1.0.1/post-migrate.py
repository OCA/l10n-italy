# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# SdI states after which the XML has already left Odoo: the stored document
# type of those moves is left as it was, since it mirrors what was sent.
SENT_STATES = (
    "being_sent",
    "processing",
    "forwarded",
    "forward_failed",
    "forward_attempt",
    "accepted_by_pa_partner",
    "rejected_by_pa_partner",
    "accepted_by_pa_partner_after_expiry",
)


def migrate(cr, version):
    """Realign `l10n_it_document_type` on 74-ter bills / credit notes.

    Before 18.0.1.0.1 the module did not override
    `_l10n_it_edi_get_document_type`, so `l10n_it_edi_ndd` stored on 74-ter
    documents whatever core computed: nothing (N3.6 taxes) or TD16..TD19 (N6.9
    taxes carrying a VJ grid), while the XML was forced to TD01 even for credit
    notes. Set the field to the 74-ter rule (TD01 bill / TD04 credit note) on
    every document not yet transmitted to the SdI.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    doc_types = {
        doc_type.code: doc_type
        for doc_type in env["l10n_it.document.type"].search(
            [("code", "in", ("TD01", "TD04"))]
        )
    }
    moves = env["account.move"].search(
        [
            ("move_type", "in", ("in_invoice", "in_refund")),
            ("state", "!=", "cancel"),
            ("commercial_partner_id.is_74ter_agent", "=", True),
            ("l10n_it_edi_state", "not in", SENT_STATES),
        ]
    )
    to_fix = {}
    for move in moves:
        if not move._l10n_it_edi_is_74ter_self_billing():
            continue
        code = move._l10n_it_edi_get_document_type()
        if move.l10n_it_document_type.code != code and code in doc_types:
            to_fix.setdefault(code, env["account.move"])
            to_fix[code] |= move
    for code, code_moves in to_fix.items():
        code_moves.write({"l10n_it_document_type": doc_types[code].id})
        _logger.info(
            "l10n_it_edi_rf11: set document type %s on %d 74-ter move(s)",
            code,
            len(code_moves),
        )
