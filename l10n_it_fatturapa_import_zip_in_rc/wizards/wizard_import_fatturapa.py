#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _is_in_reverse_charge_line(self, line):
        if self._is_import_attachment_out():
            result = False
        else:
            result = super()._is_in_reverse_charge_line(line)
        return result
