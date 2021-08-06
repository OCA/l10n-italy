from odoo import models

from .efattura import EFatturaOut


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def _get_efattura_class(self):
        return EFatturaOut
