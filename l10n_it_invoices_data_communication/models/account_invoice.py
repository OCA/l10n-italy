

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string='Exclude from invoices communication')

    def _compute_taxes_in_company_currency(self, vals):
        try:
            exchange_rate = (
                self.amount_total_signed /
                self.amount_total_company_signed)
        except ZeroDivisionError:
            exchange_rate = 1
        vals['ImponibileImporto'] = vals['ImponibileImporto'] / exchange_rate
        vals['Imposta'] = vals['Imposta'] / exchange_rate

    def _get_tax_comunicazione_dati_iva(self):
        self.ensure_one()
        fattura = self
        tax_model = self.env['account.tax']

        tax_lines = []
        tax_grouped = {}
        for tax_line in fattura.tax_line_ids:
            tax = tax_line.tax_id
            aliquota = tax.amount
            parent = tax_model.search([('children_tax_ids', 'in', [tax.id])])
            if parent:
                main_tax = parent
                aliquota = parent.amount
                if (
                    tax.cee_type and
                    tax.amount < 0 and
                    main_tax.kind_id.code.startswith('N6')
                ):
                    continue
            else:
                main_tax = tax
            kind_id = main_tax.kind_id.id
            payability = main_tax.payability
            imposta = tax_line.amount
            base = tax_line.base
            if main_tax.id not in tax_grouped:
                tax_grouped[main_tax.id] = {
                    'ImponibileImporto': 0,
                    'Imposta': imposta,
                    'Aliquota': aliquota,
                    'Natura_id': kind_id,
                    'EsigibilitaIVA': payability,
                    'Detraibile': 0.0,
                }
                if fattura.type in ('in_invoice', 'in_refund'):
                    tax_grouped[main_tax.id]['Detraibile'] = 100.0
            else:
                tax_grouped[main_tax.id]['Imposta'] += imposta
            if tax.account_id:
                # account_id è valorizzato per la parte detraibile dell'imposta
                # In questa tax_line è presente il totale dell'imponibile
                # per l'imposta corrente
                tax_grouped[main_tax.id]['ImponibileImporto'] += base

        for tax_id in tax_grouped:
            tax = tax_model.browse(tax_id)
            vals = tax_grouped[tax_id]
            if tax.children_tax_ids:
                parte_detraibile = 0.0
                for child_tax in tax.children_tax_ids:
                    if child_tax.account_id:
                        parte_detraibile = child_tax.amount
                        break
                if vals['Aliquota'] and parte_detraibile:
                    vals['Detraibile'] = (
                        100 / (vals['Aliquota'] / parte_detraibile)
                    )
                else:
                    vals['Detraibile'] = 0.0
            vals = self._check_tax_comunicazione_dati_iva(tax, vals)
            fattura._compute_taxes_in_company_currency(vals)
            tax_lines.append((0, 0, vals))

        return tax_lines

    def _check_tax_comunicazione_dati_iva(self, tax, val=None):
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
