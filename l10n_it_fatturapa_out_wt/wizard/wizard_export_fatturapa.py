
from odoo import models
from odoo.tools.translate import _
from odoo.exceptions import Warning as UserError
from odoo.tools.float_utils import float_round
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiRitenutaType,
    DatiCassaPrevidenzialeType,
    DatiRiepilogoType
)

WT_TAX_CODE = {
    'inps': 'RT03',
    'enasarco': 'RT04',
    'enpam': 'RT05',
    'other': 'RT06'
}

TC_CODE = {
    'inps': 'TC22',
    'enasarco': 'TC07',
    'enpam': 'TC09',
}


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def getTipoRitenuta(self, wt_types, partner):
        if wt_types == 'ritenuta':
            if partner.is_company:
                tipoRitenuta = 'RT02'
            else:
                tipoRitenuta = 'RT01'
        else:
            tipoRitenuta = WT_TAX_CODE[wt_types]
        return tipoRitenuta

    def setDatiGeneraliDocumento(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiGeneraliDocumento(
            invoice, body)
        # Get consistent ordering for file generation for compare with test XML
        ritenuta_lines = invoice.withholding_tax_line_ids.sorted(
            key=lambda l: l.withholding_tax_id.code)
        for wt_line in ritenuta_lines:
            if not wt_line.withholding_tax_id.causale_pagamento_id.code:
                raise UserError(_('Missing payment reason for '
                                  'withholding tax %s!')
                                % wt_line.withholding_tax_id.name)
            tipoRitenuta = self.getTipoRitenuta(
                wt_line.withholding_tax_id.wt_types,
                invoice.partner_id
                )
            body.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta.append(
                DatiRitenutaType(
                    TipoRitenuta=tipoRitenuta,
                    ImportoRitenuta='%.2f' % float_round(wt_line.tax, 2),
                    AliquotaRitenuta='%.2f' % float_round(
                        wt_line.withholding_tax_id.tax, 2),
                    CausalePagamento=wt_line.withholding_tax_id.
                    causale_pagamento_id.code
                ))
            if wt_line.withholding_tax_id.use_daticassaprev:
                tax_id = wt_line.withholding_tax_id.daticassprev_tax_id
                tax_kind = tax_id.kind_id.code
                body.DatiGenerali.DatiGeneraliDocumento.\
                    DatiCassaPrevidenziale.append(
                        DatiCassaPrevidenzialeType(
                            TipoCassa=TC_CODE[wt_line.withholding_tax_id.wt_types],
                            AlCassa='%.2f' % float_round(
                                wt_line.withholding_tax_id.tax, 2),
                            ImportoContributoCassa='%.2f' % float_round(
                                wt_line.tax, 2),
                            AliquotaIVA='0.00',
                            Natura=tax_kind,
                            )
                        )
        return res

    def get_tax_riepilogo(self, body, tax_id):
        for riepilogo in body.DatiBeniServizi.DatiRiepilogo:
            if float(riepilogo.AliquotaIVA) == 0.0 \
                    and riepilogo.Natura == tax_id.kind_id.code:
                return riepilogo

    def setDatiRiepilogo(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiRiepilogo(
            invoice, body)
        wt_lines_to_write = invoice.withholding_tax_line_ids.filtered(
            lambda x: x.withholding_tax_id.wt_types not in ('ritenuta', 'other')
            and x.withholding_tax_id.use_daticassaprev
        )
        for wt_line in wt_lines_to_write:
            tax_id = wt_line.withholding_tax_id.daticassprev_tax_id
            tax_riepilogo = self.get_tax_riepilogo(body, tax_id)
            if tax_riepilogo:
                base_amount = float(tax_riepilogo.ImponibileImporto)
                base_amount += wt_line.tax
                tax_riepilogo.ImponibileImporto = '%.2f' % float_round(
                    base_amount, 2)
            else:
                riepilogo = DatiRiepilogoType(
                    AliquotaIVA='0.00',
                    ImponibileImporto='%.2f' % float_round(wt_line.tax, 2),
                    Imposta='0.00',
                    Natura=tax_id.kind_id.code,
                    RiferimentoNormativo=tax_id.law_reference,
                )
                body.DatiBeniServizi.DatiRiepilogo.append(riepilogo)
        return res

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision
    ):
        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
            line_no, line, body, price_precision, uom_precision
        )
        if any([wt for wt in line.invoice_line_tax_wt_ids]):
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
