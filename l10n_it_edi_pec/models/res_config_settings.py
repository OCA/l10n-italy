# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_it_edi_use_pec = fields.Boolean(
        related="company_id.l10n_it_edi_use_pec",
        readonly=False,
    )
    l10n_it_edi_pec_server_id = fields.Many2one(
        related="company_id.l10n_it_edi_pec_server_id",
        readonly=False,
    )
    l10n_it_edi_pec_fetch_server_id = fields.Many2one(
        related="company_id.l10n_it_edi_pec_fetch_server_id",
        readonly=False,
    )
    l10n_it_edi_pec_email_exchange_system = fields.Char(
        related="company_id.l10n_it_edi_pec_email_exchange_system",
        readonly=False,
    )
