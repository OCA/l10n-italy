# -*- coding: utf-8 -*-

from openerp import fields, models, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string='Exclude from invoices communication')

    def _compute_taxes_in_company_currency(self, vals):
        try:
            exchange_rate = abs(
                self.amount_total /
                self.move_id.amount)
        except ZeroDivisionError:
            exchange_rate = 1
        vals['ImponibileImporto'] = vals['ImponibileImporto'] / exchange_rate
        vals['Imposta'] = vals['Imposta'] / exchange_rate

    def _get_tax_comunicazione_dati_iva(self):
        self.ensure_one()
        fattura = self
        tax_code_model = self.env['account.tax.code']

        tax_lines = []
        tax_grouped = {}

        # group invoice tax lines for same tax
        # get totals for group of sale tax
        # group children taxes: sum taxes and get base from the correct tax
        tax_with_child_ids = self.env['account.tax'].search(
            [('child_ids', '!=', False)])
        taxes = set([
            x.tax_code_id for x in fattura.tax_line if
            x.tax_code_id and not self.env['account.tax'].search([
                ('tax_code_id', '=', x.tax_code_id.id)
            ]) in tax_with_child_ids.mapped('child_ids')
            and not x.tax_code_id.exclude_from_registries
        ])
        child_taxes = set([
            x.tax_code_id for x in fattura.tax_line if
            x.tax_code_id and self.env['account.tax'].search([
                ('tax_code_id', '=', x.tax_code_id.id)
            ]) in tax_with_child_ids.mapped('child_ids')
            and not x.tax_code_id.exclude_from_registries
        ])
        bases = set([
            x.base_code_id for x in fattura.tax_line if
            x.base_code_id and not x.tax_code_id
            and not x.base_code_id.exclude_from_registries
        ])
        if taxes or bases or child_taxes:
            if taxes or child_taxes:
                tax_grouped = {
                    x.id: {
                        'ImponibileImporto': 0.0,
                        'Imposta': 0.0,
                        'Aliquota': 0.0,
                        'Natura_id': False,
                        'EsigibilitaIVA': False,
                        'is_base': False
                    }
                    for x in taxes | child_taxes}
            if bases and not (taxes or child_taxes):
                tax_grouped = {
                    x.id: {
                        'ImponibileImporto': 0.0,
                        'Imposta': 0.0,
                        'Aliquota': 0.0,
                        'Natura_id': False,
                        'EsigibilitaIVA': False,
                        'is_base': True}
                    for x in bases}
            if bases and (taxes or child_taxes):
                tax_grouped.update({
                    x.id: {
                        'ImponibileImporto': 0.0,
                        'Imposta': 0.0,
                        'Aliquota': 0.0,
                        'Natura_id': False,
                        'EsigibilitaIVA': False,
                        'is_base': True}
                    for x in bases})

        for tax_line in fattura.tax_line:
            if tax_line.tax_code_id and tax_line.tax_code_id in child_taxes:
                # this is a child tax: sum amount from not deductible
                # and pop from the group
                main_tax = tax_line.tax_code_id
                tax_id = self.env['account.tax'].search(
                    [('tax_code_id', '=', main_tax.id)])
                sister_tax_id = tax_id.parent_id.child_ids.filtered(
                    lambda z: z.id != tax_id.id)[0]
                if tax_id.account_collected_id:
                    tax_grouped[sister_tax_id.tax_code_id.id][
                        'Imposta'] += tax_line.amount
                    tax_grouped[sister_tax_id.tax_code_id.id][
                        'Detraibile'] = (
                            (1 - sister_tax_id.amount) * 100)
                    tax_grouped.pop(tax_id.tax_code_id.id)
                    continue
                else:
                    tax_grouped[main_tax.id][
                        'ImponibileImporto'] += tax_line.base
                    tax_grouped[main_tax.id]['Imposta'] += tax_line.amount
                    tax_grouped[main_tax.id]['is_base'] = False
            elif tax_line.tax_code_id.id and tax_line.tax_code_id.id in \
                    tax_grouped:
                main_tax = tax_line.tax_code_id
                tax_grouped[main_tax.id]['ImponibileImporto'] += tax_line.base
                tax_grouped[main_tax.id]['Imposta'] += tax_line.amount
                tax_grouped[main_tax.id]['is_base'] = False
            elif tax_line.base_code_id.id and tax_line.base_code_id.id\
                    in tax_grouped:
                main_tax = tax_line.base_code_id
                tax_grouped[main_tax.id]['ImponibileImporto'] += tax_line.base
                tax_grouped[main_tax.id]['Imposta'] += tax_line.amount
                tax_grouped[main_tax.id]['is_base'] = True

            if not tax_grouped[main_tax.id].get('is_base', False):
                tax = main_tax.tax_ids[0]
                # if tax_id is a child of other tax, use it for aliquota
                if tax.parent_id and tax.parent_id.child_depend:
                    tax = tax.parent_id
            else:
                tax = main_tax.base_tax_ids[0]

            aliquota = tax.amount * 100
            payability = tax.payability
            kind_id = tax.kind_id.id
            tax_grouped[main_tax.id].update({
                'Aliquota': aliquota,
                'Natura_id': kind_id,
                'EsigibilitaIVA': payability,
            })

        for tax_id in tax_grouped:
            tax = tax_code_model.browse(tax_id)
            vals = tax_grouped[tax_id]
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
