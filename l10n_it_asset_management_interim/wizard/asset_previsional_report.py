# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class WizardAssetPrevisionalReport(models.TransientModel):
    _inherit = "wizard.asset.previsional.report"

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

    @api.depends("date")
    def _compute_interim_reversal_date(self):
        for wizard in self:
            if wizard.date:
                wizard.interim_reversal_date = wizard.date + timedelta(days=1)

    def get_interim_depreciations(self):
        """Depreciations of the assets and of the types of the report."""
        self.ensure_one()
        report = self.env["report_asset_previsional"].new(self.prepare_report_vals())
        depreciations = report.get_assets().depreciation_ids
        if self.type_ids:
            depreciations = depreciations.filtered(
                lambda dep: dep.type_id in self.type_ids
            )
        return depreciations

    def button_create_interim_depreciation(self):
        """Create and post the interim depreciation entry and its reversal,
        with the depreciation that the report shows at its date."""
        self.ensure_one()
        if not self.date:
            raise UserError(self.env._("Choose a date for interim depreciations."))
        depreciation_model = self.env["asset.depreciation"]
        moves = self.get_interim_depreciations().create_interim_moves(
            self.date, self.interim_journal_id, self.interim_reversal_date
        )
        return depreciation_model.get_interim_moves_action(moves)
