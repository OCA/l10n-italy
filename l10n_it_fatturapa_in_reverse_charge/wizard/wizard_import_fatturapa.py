# -*- coding: utf-8 -*-

from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _prepare_generic_line_data(self, line):
        retLine = super(WizardImportFatturapa, self).\
            _prepare_generic_line_data(line)

        # Map Natura N6 to Reverse Charge
        if line.Natura == 'N6':
            retLine['rc'] = True

        return retLine
