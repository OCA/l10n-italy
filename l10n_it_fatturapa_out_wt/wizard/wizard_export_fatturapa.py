# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa_v_1_2 import (
    DatiRitenutaType,
    AltriDatiGestionaliType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        ritenuta_lines = invoice.withholding_tax_line.filtered(
            lambda x: x.withholding_tax_id.wt_types == 'ritenuta')
        if len(ritenuta_lines) > 1:
            raise UserError(
                _("More than one withholding tax in invoice!"))
        for wt_line in ritenuta_lines:
            if not wt_line.withholding_tax_id.causale_pagamento_id.code:
                raise UserError(_('Missing causale pagamento for '
                                  'withholding tax %s!')
                                % wt_line.withholding_tax_id.name)
            body.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta\
                = DatiRitenutaType(
                    TipoRitenuta="RT02" if invoice.partner_id.is_company
                    else "RT01",  # RT02 persona giuridica
                    ImportoRitenuta='%.2f' % wt_line.tax,
                    AliquotaRitenuta='%.2f' % (
                        wt_line.tax / wt_line.base * 100),
                    CausalePagamento=wt_line.withholding_tax_id.
                    causale_pagamento_id.code
                )
        return res

    def setDettaglioLinee(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDettaglioLinee(
            invoice, body)
        enasarco_lines = invoice.withholding_tax_line.filtered(
            lambda x: x.withholding_tax_id.wt_types == 'enasarco')
        if len(enasarco_lines) > 1:
            raise UserError(
                _("More than one Enasarco tax in invoice!"))
        for wt_line in enasarco_lines:
            # tmp put values in the first line
            # todo split values for lines with withholding type enasarco
            body.DatiBeniServizi.DettaglioLinee[0].AltriDatiGestionali.append(
                AltriDatiGestionaliType(
                    TipoDato="CASSA-PREV",
                    RiferimentoTesto='ENASARCO %s' % wt_line.
                    withholding_tax_id.welfare_fund_type_id.name,
                    RiferimentoNumero='%.2f' % wt_line.tax,
                )
            )
        return res
