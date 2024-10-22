#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class WizardAssetJournalReport(models.TransientModel):
    _inherit = "wizard.asset.journal.report"

    def export_asset_journal_report(self, report_type=None):
        return super(
            WizardAssetJournalReport,
            self.with_context(
                use_partner_name_history=True,
            ),
        ).export_asset_journal_report(
            report_type=report_type,
        )
