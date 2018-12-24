# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    DatiBolloType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        if invoice.tax_stamp:
            price_precision = self.env['decimal.precision'].precision_get(
                'Product Price')
            if price_precision < 2:
                price_precision = 2
            if not invoice.company_id.tax_stamp_product_id:
                raise UserError(_(
                    "Tax Stamp Product not set for company %s"
                ) % invoice.company_id.name)
            body.DatiGenerali.DatiGeneraliDocumento.DatiBollo = DatiBolloType(
                BolloVirtuale="SI",
                ImportoBollo=('%.' + str(
                    price_precision
                ) + 'f') % invoice.company_id.tax_stamp_product_id.list_price,
            )
        return res
