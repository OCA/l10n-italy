# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
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
            body.DatiGenerali.DatiGeneraliDocumento.DatiBollo = DatiBolloType(
                BolloVirtuale="SI",
                ImportoBollo='%.2f' % invoice.company_id.tax_stamp_product_id.
                list_price,
            )
        return res
