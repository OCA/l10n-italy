# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models

from .efattura import EFatturaOut


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def _get_efattura_class(self):
        return EFatturaOut
