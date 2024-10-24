#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getImporto(self, line):
        res = super().getImporto(line)
        discount_fixed = line.discount_fixed
        if discount_fixed:
            return discount_fixed
        return res
