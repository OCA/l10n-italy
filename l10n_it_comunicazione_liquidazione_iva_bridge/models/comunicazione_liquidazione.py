# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ComunicazioneLiquidazioneVp(models.Model):
    _inherit = 'comunicazione.liquidazione.vp'

    liquidazioni_ids = fields.Many2many(
        'account.vat.period.end.statement',
        'comunicazione_iva_liquidazioni_rel',
        'comunicazione_id',
        'liquidazione_id',
        string='Liquidazioni')

    def _reset_values(self):
        for quadro in self:
            quadro.imponibile_operazioni_attive = 0
            quadro.imponibile_operazioni_passive = 0
            quadro.iva_esigibile = 0
            quadro.iva_detratta = 0
            quadro.debito_periodo_precedente = 0
            quadro.credito_periodo_precedente = 0
            quadro.credito_anno_precedente = 0
            quadro.versamento_auto_UE = 0
            quadro.crediti_imposta = 0
            quadro.interessi_dovuti = 0
            quadro.accounto_dovuto = 0

    @api.multi
    @api.onchange('liquidazioni_ids')
    def compute_from_liquidazioni(self):

        for quadro in self:
            # Reset valori
            quadro._reset_values()

            interests_account_id = quadro.comunicazione_id.company_id.\
                of_account_end_vat_statement_interest_account_id.id or False

            for liq in quadro.liquidazioni_ids:

                for period in liq.date_range_ids:

                    # Operazioni attive
                    debit_taxes = self.env['account.tax']
                    for debit in liq.debit_vat_account_line_ids:
                        debit_taxes |= debit.tax_id
                    for debit_tax in debit_taxes:
                        tax = debit_taxes.with_context({
                            'from_date': period.date_start,
                            'to_date': period.date_end,
                        }).browse(debit_tax.id)
                        quadro.imponibile_operazioni_attive += (
                            tax.base_balance)

                    # Operazioni passive
                    credit_taxes = self.env['account.tax']
                    for credit in liq.credit_vat_account_line_ids:
                        credit_taxes |= credit.tax_id
                    for credit_tax in credit_taxes:
                        tax = credit_taxes.with_context({
                            'from_date': period.date_start,
                            'to_date': period.date_end,
                        }).browse(credit_tax.id)
                        quadro.imponibile_operazioni_passive -= (
                            tax.base_balance)

                # Iva esigibile
                for vat_amount in liq.debit_vat_account_line_ids:
                    quadro.iva_esigibile += vat_amount.amount
                # Iva detratta
                for vat_amount in liq.credit_vat_account_line_ids:
                    quadro.iva_detratta += vat_amount.amount
                # credito/debito periodo precedente
                quadro.debito_periodo_precedente =\
                    liq.previous_debit_vat_amount
                quadro.credito_periodo_precedente =\
                    liq.previous_credit_vat_amount
                # Credito anno precedente (NON GESTITO)
                # Versamenti auto UE (NON GESTITO)
                # Crediti d’imposta (NON GESTITO)
                # Da altri crediti e debiti calcolo:
                # 1 - Interessi dovuti per liquidazioni trimestrali
                # 2 - Decremento iva esigibile con righe positive
                # 3 - Decremento iva detratta con righe negative
                for line in liq.generic_vat_account_line_ids:
                    if interests_account_id and \
                            (line.account_id.id == interests_account_id):
                        quadro.interessi_dovuti += (-1 * line.amount)
                    elif line.amount > 0:
                        quadro.iva_esigibile -= line.amount
                    else:
                        quadro.iva_detratta += line.amount
