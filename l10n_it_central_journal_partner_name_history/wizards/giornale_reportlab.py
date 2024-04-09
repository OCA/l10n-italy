#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models


class WizardGiornaleReportlab(models.TransientModel):
    _inherit = "wizard.giornale.reportlab"

    def create_report_giornale_reportlab(self):
        return super(
            WizardGiornaleReportlab,
            self.with_context(
                use_partner_name_history=True,
            ),
        ).create_report_giornale_reportlab()
