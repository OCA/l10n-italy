# Copyright 2022 Marco Colombo <marco.colombo@phi.technology>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def getImportoTotale(self, invoice):
        amount_total = super().getImportoTotale(invoice)
        if invoice.split_payment:
            amount_total += invoice.amount_sp
        return amount_total
