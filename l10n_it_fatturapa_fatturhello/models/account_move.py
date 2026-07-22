# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.l10n_it_fatturapa_out.models.account import (
    fatturapa_attachment_state_mapping,
)

fatturapa_attachment_state_mapping["sent_to_fatturhello"] = "sent_to_fatturhello"


class AccountMove(models.Model):
    _inherit = "account.move"

    fatturapa_state = fields.Selection(
        selection_add=[
            # Before the `sent` status
            ("sent_to_fatturhello", "Sent to Fatturhello"),
            ("sent",),
        ],
    )
