#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    TipoCessionePrestazioneType,
)


class WizardExportFatturapa (models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision,
    ):
        DettaglioLinea = super().setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision,
        )
        if line.is_complimentary:
            DettaglioLinea.TipoCessionePrestazione = \
                TipoCessionePrestazioneType.AB
        return DettaglioLinea
