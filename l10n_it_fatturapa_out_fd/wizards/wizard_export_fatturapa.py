#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    ScontoMaggiorazioneType,
    TipoScontoMaggiorazioneType,
)
from odoo.tools import float_round


class WizardExportFatturapa (models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setScontoMaggiorazione(self, line):
        res = super().setScontoMaggiorazione(line)
        discount_fixed = line.discount_fixed
        if discount_fixed:
            res.append(
                ScontoMaggiorazioneType(
                    Tipo=TipoScontoMaggiorazioneType.SC,
                    Importo='%.2f' % float_round(discount_fixed, 8),
                )
            )
        return res
