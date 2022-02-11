# Copyright 2021 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models

from .efattura import EFatturaOut


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def _get_efattura_class(self):
        return EFatturaOut

    @api.model
    def getSign(self, invoice):
        sign = 1
        if invoice.move_type in [
            "out_refund",
            "in_refund",
        ] and invoice.fiscal_document_type_id.code not in ["TD04", "TD08"]:
            sign = -1
        return sign

    @api.model
    def getImportoTotale(self, invoice):
        amount_total = super().getImportoTotale(invoice)
        amount_total *= self.getSign(invoice)
        return amount_total
