# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.tools.translate import _
from odoo.exceptions import Warning as UserError
from odoo.tools.float_utils import float_round
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiRitenutaType,
    AltriDatiGestionaliType,
    DatiCassaPrevidenzialeType,
    DatiRiepilogoType
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        ritenuta_lines = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types == 'ritenuta')
        if len(ritenuta_lines) > 1:
            raise UserError(
                _("More than one withholding tax in invoice!"))
        for wt_line in ritenuta_lines:
            if not wt_line.withholding_tax_id.causale_pagamento_id.code:
                raise UserError(_('Missing payment reason for '
                                  'withholding tax %s!')
                                % wt_line.withholding_tax_id.name)
            body.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta\
                = DatiRitenutaType(
                    TipoRitenuta="RT02" if invoice.partner_id.is_company
                    else "RT01",  # RT02 persona giuridica
                    ImportoRitenuta='%.2f' % float_round(wt_line.tax, 2),
                    AliquotaRitenuta='%.2f' % float_round(
                        wt_line.withholding_tax_id.tax, 2),
                    CausalePagamento=wt_line.withholding_tax_id.
                    causale_pagamento_id.code
                )
        enasarco_lines = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types == 'enasarco')
        for enas_line in enasarco_lines:
            if enas_line.withholding_tax_id.use_daticassaprev_for_enasarco:
                body.DatiGenerali.DatiGeneraliDocumento.\
                    DatiCassaPrevidenziale.append(
                        DatiCassaPrevidenzialeType(
                            TipoCassa='TC07',
                            AlCassa='%.2f' % float_round(
                                enas_line.withholding_tax_id.tax, 2),
                            ImportoContributoCassa='%.2f' % float_round(
                                enas_line.tax, 2),
                            AliquotaIVA='0.00',
                            Natura='N2'
                            )
                        )
        return res

    def get_n2_tax_riepilogo(self, body):
        for riepilogo in body.DatiBeniServizi.DatiRiepilogo:
            if float(riepilogo.AliquotaIVA) == 0 and riepilogo.Natura == 'N2':
                return riepilogo

    def setDatiRiepilogo(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiRiepilogo(
            invoice, body)
        enasarco_lines_to_write = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types == 'enasarco' and
            x.withholding_tax_id.use_daticassaprev_for_enasarco
        )
        if enasarco_lines_to_write:
            n2_riepilogo = self.get_n2_tax_riepilogo(body)
            enasarco_base = sum(enasarco_lines_to_write.mapped('tax'))
            if n2_riepilogo:
                base_amount = float(n2_riepilogo.ImponibileImporto)
                base_amount += enasarco_base
                n2_riepilogo.ImponibileImporto = '%.2f' % float_round(base_amount, 2)
            else:
                riepilogo = DatiRiepilogoType(
                    AliquotaIVA='0.00',
                    ImponibileImporto='%.2f' % float_round(enasarco_base, 2),
                    Imposta='0.00',
                    Natura='N2',
                    RiferimentoNormativo='Escluso Art. 13 5C DPR 633/72',
                )
                body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)
        return res

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision
    ):
        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision
        )
        for wt in line.invoice_line_tax_wt_ids:
            if wt.wt_types == 'enasarco':
                amount = wt.compute_tax(line.price_subtotal)['tax']
                DettaglioLinea.AltriDatiGestionali.append(
                    AltriDatiGestionaliType(
                        TipoDato="CASSA-PREV",
                        RiferimentoTesto=('ENASARCO TC07 (%s%%)' % wt.tax),
                        RiferimentoNumero='%.2f' % float_round(amount, 2),
                    )
                )
            else:
                DettaglioLinea.Ritenuta = 'SI'
        return DettaglioLinea

    def setDatiPagamento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiPagamento(
            invoice, body)
        if invoice.withholding_tax_line_ids and invoice.payment_term_id:
            payment_line_ids = invoice.get_receivable_line_ids()
            index = 0
            rate = invoice.amount_net_pay / invoice.amount_total
            move_line_pool = self.env['account.move.line']
            for move_line_id in payment_line_ids:
                move_line = move_line_pool.browse(move_line_id)
                body.DatiPagamento[0].DettaglioPagamento[index].\
                    ImportoPagamento = '%.2f' % float_round(
                        (move_line.amount_currency or move_line.debit) * rate, 2)
                index += 1
        return res
