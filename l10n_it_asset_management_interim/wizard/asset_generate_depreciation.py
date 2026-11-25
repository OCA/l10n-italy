# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _inherit = "wizard.asset.generate.depreciation"

    interim = fields.Boolean(
        string="Interim Depreciation",
        help="Create a journal entry with the depreciation until the date, "
        "and its reversal, without creating depreciation lines.",
    )
    interim_journal_id = fields.Many2one(
        comodel_name="account.journal",
        check_company=True,
        domain="[('company_id', '=', company_id)]",
        string="Interim Journal",
    )
    interim_reversal_date = fields.Date(
        compute="_compute_interim_reversal_date",
        store=True,
        readonly=False,
        string="Reversal Date",
    )

    @api.depends("date_dep")
    def _compute_interim_reversal_date(self):
        for wizard in self:
            if wizard.date_dep:
                wizard.interim_reversal_date = wizard.date_dep + timedelta(days=1)

    def do_generate(self):
        if self.interim:
            return self.do_generate_interim()
        return super().do_generate()

    def do_generate_interim(self):
        """Create and post the interim depreciation entry and its reversal."""
        self.ensure_one()
        if not self.company_id:
            raise UserError(self.env._("Choose a company for interim depreciations."))
        depreciation_model = self.env["asset.depreciation"]
        moves = self.get_depreciations().create_interim_moves(
            self.date_dep, self.interim_journal_id, self.interim_reversal_date
        )
        return depreciation_model.get_interim_moves_action(moves)
