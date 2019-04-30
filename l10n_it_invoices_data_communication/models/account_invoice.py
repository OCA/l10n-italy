# -*- coding: utf-8 -*-


from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string='Exclude from invoices communication')

    @api.multi
    def _compute_taxes_in_company_currency(self, vals):
        self.ensure_one()
        sign = 1 if self.type in ('out_invoice', 'in_refund') else -1
        amount_total_signed = sign * self.amount_total
        currency_id = self.currency_id.with_context(date=self.date_invoice)
        amount_total_company = currency_id.compute(
            self.amount_total, self.company_id.currency_id)
        amount_total_company_signed = sign * amount_total_company
        try:
            exchange_rate = (
                amount_total_signed /
                amount_total_company_signed)
        except ZeroDivisionError:
            exchange_rate = 1
        vals['ImponibileImporto'] = vals['ImponibileImporto'] / exchange_rate
        vals['Imposta'] = vals['Imposta'] / exchange_rate

    @api.multi
    def _get_tax_comunicazione_dati_iva(self):
        self.ensure_one()
        tax_grouped = {}
        tot_imponibile = 0
        tot_imposta = 0
        for tax_line in self.tax_line:
            tax, val = self.get_tax_line_vals(tax_line)

            tot_imponibile += val['ImponibileImporto']
            tot_imposta += val['Imposta']

            if tax.id not in tax_grouped:
                tax_grouped[tax.id] = val
            else:
                tax_grouped[tax.id]['ImponibileImporto'] += \
                    val['ImponibileImporto']
                tax_grouped[tax.id]['Imposta'] += val['Imposta']

        tax_lines = []
        if tax_grouped:
            for key in tax_grouped:
                val = tax_grouped[key]
                val = self._check_tax_comunicazione_dati_iva(key, val)
                tax_lines.append((0, 0, val))
        tot_vals = {
            'tot_imponibile': tot_imponibile,
            'tot_imposta': tot_imposta
        }
        self._check_tax_comunicazione_dati_iva_fattura(tot_vals)
        return tax_lines

    @api.multi
    def get_tax_line_vals(self, tax_line):
        self.ensure_one()
        # aliquota, natura, esigibilità
        aliquota = 0
        kind_id = False
        payability = False
        domain = [('tax_code_id', '=', tax_line.tax_code_id.id)]
        tax = self.env['account.tax'].search(domain, order='id', limit=1)
        tax_origin = tax
        if tax.parent_id:
            tax = tax.parent_id

        if tax:
            aliquota = tax.amount * 100
            kind_id = tax.kind_id.id
            payability = tax.payability
        vals_tax_line = \
            self._get_tax_comunicazione_dati_iva_tax_line_amount(tax_line)
        val = {
            'ImponibileImporto': vals_tax_line['base'],
            'Imposta': vals_tax_line['amount'],
            'Aliquota': aliquota,
            'Natura_id': kind_id,
            'EsigibilitaIVA': payability
        }
        # Detraibilità
        detraibilita = False
        if tax_origin.parent_id and tax_origin.type in ['percent']:
            if tax_origin.account_collected_id:
                detraibilita = tax_origin.amount * 100
            else:
                detraibilita = 100 - (tax_origin.amount * 100)
        if detraibilita:
            val['Detraibile'] = detraibilita
        if self.type in ('in_invoice', 'in_refund'):
            val['Detraibile'] = 100.0
        # Solo imponibile legato alla parte indetraibile
        if tax_origin.parent_id:
            if not tax_line.base_code_id:
                val['ImponibileImporto'] = 0
        return tax, val

    @api.multi
    def _get_tax_comunicazione_dati_iva_tax_line_amount(self, tax_line):
        self.ensure_one()
        vals = {
            'base': abs(tax_line.base_amount),
            'amount': abs(tax_line.tax_amount)
        }
        # Gestione righe negative
        if tax_line.base < 0 or 'refund' in self.type:
            vals['base'] = vals['base'] * -1
            vals['amount'] = vals['amount'] * -1
        return vals

    @api.multi
    def _check_tax_comunicazione_dati_iva_fattura(self, args=None):
        self.ensure_one()
        if (
            self.currency_id and
            self.currency_id.id != self.company_id.currency_id.id
        ):
            # in caso di fatture in valuta estera, non controllo amount_untaxed
            # perchè sarebbe comunque diverso dall'importo in valuta base
            return
        if not args:
            args = {}

        if 'tot_imponibile' in args:
            if not abs(round(self.amount_untaxed, 2)) ==\
                    abs(round(args['tot_imponibile'], 2)):
                raise ValidationError(
                    _("Imponibile ft {} del partner {} non congruente. \
                    Verificare dettaglio sezione imposte della fattura (\
                    imponible doc:{} - imponibile dati iva:{})"
                      ).format(self.number, self.partner_id.name,
                               str(self.amount_untaxed),
                               str(args['tot_imponibile'])))

    @api.multi
    def _check_tax_comunicazione_dati_iva(self, tax, val=None):
        self.ensure_one()
        if not val:
            val = {}
        if val['Aliquota'] == 0 and not val['Natura_id']:
            raise ValidationError(
                _(
                    "Please specify exemption kind for tax: {} - Invoice {}"
                ).format(tax.name, self.number or False))
        if not val['EsigibilitaIVA']:
            raise ValidationError(
                _(
                    "Please specify VAT payability for tax: {} - Invoice {}"
                ).format(tax.name, self.number or False))
        return val
