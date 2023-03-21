# -*- coding: utf-8 -*-

from odoo import models
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_round
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiBolloType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        if invoice.tax_stamp:
            if not invoice.company_id.tax_stamp_product_id:
                raise UserError(_(
                    "Tax Stamp Product not set for company %s"
                ) % invoice.company_id.name)
            stamp_price = invoice.company_id.tax_stamp_product_id.list_price
            body.DatiGenerali.DatiGeneraliDocumento.DatiBollo = DatiBolloType(
                BolloVirtuale="SI",
                ImportoBollo='%.2f' % float_round(stamp_price, 2),
            )
        return res
