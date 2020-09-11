# -*- coding: utf-8 -*-

from odoo import models
from odoo.tools.float_utils import float_round, float_is_zero
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiBolloType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        if invoice.tax_stamp:
            body.DatiGenerali.DatiGeneraliDocumento.DatiBollo = DatiBolloType(
                BolloVirtuale="SI")
            if invoice.company_id.tax_stamp_product_id:
                stamp_price = invoice.company_id.tax_stamp_product_id.list_price
                if not float_is_zero(stamp_price, precision_digits=2):
                    body.DatiGenerali.DatiGeneraliDocumento.DatiBollo.ImportoBollo = \
                        '%.2f' % float_round(stamp_price, 2)
        return res
