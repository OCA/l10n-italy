# -*- coding: utf-8 -*-

import time
from odoo import api, models


class ReportRegistroIvaVendite(models.AbstractModel):
    _name = 'report.l10n_it_vat_registries.report_registro_iva'
    
    @api.model
    def render_html(self, docids, data=None):
         report_obj = self.env['report']
         context = dict(self._context or {})
         ctx = context.copy()
         ctx['used_tax_codes'] = {}
         #report = report_obj._get_report_from_name('l10n_it_vat_registries.report_registro_iva')
         docargs = {
            'doc_ids': data['ids'],
            'doc_model': self.env['account.move'],
            'data': data['form'],
            'docs': self.env['account.move'].browse(data['ids']),
            'time': time,
            'get_move': self._get_move,
            'tax_lines': self._get_tax_lines,
            'tax_codes': self._get_tax_codes,
            'from_date': data['form']['from_date'],
            'to_date': data['form']['to_date'],
            'registry_type': data['form']['registry_type'],
            'invoice_total': self._get_invoice_total,
         }

         return self.env['report'].with_context(ctx).render('l10n_it_vat_registries.report_registro_iva', docargs)

    def _tax_amounts_by_tax_id(self, data, move):
        res = {}
        tax_list = []
        tax_list_used_tax_codes = []
        for move_line in move.line_ids:
            if move_line.tax_line_id:
                tax_parent = self.env['account.tax'].search([('children_tax_ids','in', move_line.tax_line_id.id)])
                if tax_parent:
                    tax = tax_parent
                else:
                    tax = move_line.tax_line_id
                
                tax_list.append({
                          'is_base':False,
                          'tax': tax,
                          'amount': move_line.debit or move_line.credit
                          })
            elif move_line.tax_ids:
                for tax in move_line.tax_ids:
                     tax_list.append({
                          'is_base':True,
                          'tax': tax,
                          'amount': move_line.debit or move_line.credit
                          })

        for tax_line in tax_list:
            if (
                tax_line['tax'] and not
                tax_line['tax'].exclude_from_registries and
                tax_line['amount']
            ):
                # eslcudo i conti imposta in base alla natura della
                # stampa e al tipo conto imposta
                if (
                    (
                        data['registry_type'] == 'supplier' and
                        tax_line['tax'].type_tax_use == 'purchase'
                    ) or
                    ((
                        data['registry_type'] == 'customer' or
                        data['registry_type'] == 'corrispettivi'
                    ) and
                        tax_line['tax'].type_tax_use == 'sale')
                ):
                    
                    tax_list_used_tax_codes.append(tax_line['tax'])
                    self.calc_tax(tax_line['tax'], tax_line['is_base'], tax_line['amount'], res)

        return res, tax_list_used_tax_codes
    
  
    
    
    
    def _get_move(self, data, move_ids):
        move_list = self.env['account.move'].browse(move_ids)
        return move_list
    
    def _get_tax_lines(self, data, move):
        res = []
        
        # index è usato per non ripetere la stampa dei dati fattura quando ci
        # sono più codici IVA
        index = 0
        invoice = False
        
        for move_line in move.line_ids:
            if invoice and invoice != move_line.invoice_id:
                raise Exception(
                    _("Move %s contains different invoices") % move.name)
            invoice = move_line.invoice_id
            res1 = self._tax_amounts_by_tax_id(data, move)
        amounts_by_tax_id = res1[0]
        used_tax_codes = res1[1]
       
        if invoice and (invoice.type =='out_invoice' or  invoice.type =='in_invoice'):
            invoice_type ="FA"
        else:
            invoice_type ="NC"
        for tax_code_id in amounts_by_tax_id:
            tax_item = {
                'tax_code_name': amounts_by_tax_id[tax_code_id]['name'],
                'base': amounts_by_tax_id[tax_code_id]['base'],
                'tax': amounts_by_tax_id[tax_code_id]['tax'],
                'index': index,
                'invoice_type': invoice_type,
                'invoice_date': (invoice and invoice.date_invoice or
                                 move.date or ''),
                'reference': (
                    invoice and invoice.reference or '')
            }
            res.append(tax_item)
            index += 1

        return res#{'line_move': res, 'used_tax_codes': res}
    
    def _get_invoice_total(self, move):
        total = 0.0
        receivable_payable_found = False
        for move_line in move.line_ids:
            if move_line.account_id.user_type_id.type == 'receivable':
                total += move_line.debit or (- move_line.credit)
                receivable_payable_found = True
            elif move_line.account_id.user_type_id.type == 'payable':
                total += (- move_line.debit) or move_line.credit
                receivable_payable_found = True
        if receivable_payable_found:
            return abs(total)
        else:
            return abs(move.amount)
    
    def build_parent_tax_codes(self, tax_code):
        res = {}
        if tax_code.parent_id and tax_code.parent_id.parent_id:
            res[tax_code.parent_id.id] = True
            res.update(self.build_parent_tax_codes(tax_code.parent_id))
        return res
    
    def is_totally_undeductable(self, tax):
        children_tax_codes = []
        for tax in tax.child_ids:
            children_tax_codes.append(tax.tax_code_id.id)
        if len(set(children_tax_codes)) == 1:
            return True
        else:
            return False
    
    def get_undeductible_balances(self, tax):
        total_undeduct = 0
        total_deduct = 0
        if self.is_totally_undeductable(tax):
            total_undeduct = self.compute_tax_code_total(
                tax.child_ids[0].tax_code_id)
        else:
            for child in tax.child_ids:
                # deductibile
                if child.tax_code_id and child.account_collected_id:
                    total_deduct = self.compute_tax_code_total(
                        child.tax_code_id)
                # undeductibile
                elif child.tax_code_id:
                    total_undeduct = self.compute_tax_code_total(
                        child.tax_code_id)
        return (total_undeduct, total_deduct)
    
    def _compute_totals_tax(self, tax_code_ids):
        res = []
        tax_obj = self.pool.get('account.tax')
        tax_list = []
        for tax_code_id in tax_code_ids:
            tax_id = self.get_tax_by_tax_code(tax_code_id)
            if tax_id not in tax_list:
                tax_list.append(tax_id)
        tax_list_obj = tax_obj.browse(tax_list)
        for tax in tax_list_obj:
            total_undeduct = 0
            total_deduct = 0
            total_tax = 0
            total_base = 0
            if tax.nondeductible:
                # detraibile / indetraibile
                # recupero il valore dell'imponibile
                if tax.base_code_id:
                    total_base = self.compute_tax_code_total(tax.base_code_id)
                else:
                    raise Exception(
                        _("Can't compute base amount for tax %s")
                        % tax.name)
                total_undeduct, total_deduct = self.get_undeductible_balances(
                    tax)
                total_tax = total_deduct + total_undeduct
            else:
                # recupero il valore dell'imponibile
                if tax.base_code_id:
                    total_base = self.compute_tax_code_total(tax.base_code_id)
                # recupero il valore dell'imposta
                if tax.tax_code_id:
                    total_tax = self.compute_tax_code_total(tax.tax_code_id)
                total_deduct = total_tax
            res.append((
                tax.name, total_base, total_tax, total_deduct,
                total_undeduct))
        return res
    
    def get_tax_by_tax_code(self, tax_code_id):
        # assumendo l'univocità fra tax code e tax senza genitore, risale
        # all account.tax collegato al tax code passato al metodo
        obj_tax = self.pool.get('account.tax')
        tax_ids = obj_tax.search(self.cr, self.uid, [
            '&',
            '&',
            '|',
            ('base_code_id', '=', tax_code_id),
            '|',
            ('tax_code_id', '=', tax_code_id),
            '|',
            ('ref_base_code_id', '=', tax_code_id),
            ('ref_tax_code_id', '=', tax_code_id),
            ('parent_id', '=', False),
            ('price_include', '=', False),
        ])
        if not tax_ids:
            # I'm in the case of partially deductible VAT
            child_tax_ids = obj_tax.search(self.cr, self.uid, [
                '&',
                '|',
                ('base_code_id', '=', tax_code_id),
                '|',
                ('tax_code_id', '=', tax_code_id),
                '|',
                ('ref_base_code_id', '=', tax_code_id),
                ('ref_tax_code_id', '=', tax_code_id),
                ('price_include', '=', False),
            ])
            for tax in obj_tax.browse(self.cr, self.uid, child_tax_ids):
                if tax.parent_id:
                    if tax.parent_id.id not in tax_ids:
                        tax_ids.append(tax.parent_id.id)
                else:
                    if tax.id not in tax_ids:
                        tax_ids.append(tax.id)
        if len(tax_ids) != 1:
            raise Exception(
                _("Tax code %s is not linked to 1 and only 1 tax")
                % tax_code_id)
        return tax_ids[0]
    
    def compute_tax_code_total(self, tax_code):
        journal_ids = self.localcontext['data']['form']['journal_ids']
        res_dict = {}
        for period_id in self.localcontext['data']['form']['period_ids']:
            # taking the first and only, as tax_code is 1 record
            tax_sum = tax_code.sum_by_period_and_journals(
                period_id, journal_ids)[0]
            if not res_dict.get(tax_code.id):
                res_dict[tax_code.id] = 0.0
            res_dict[tax_code.id] += (
                tax_sum)# * self.localcontext['data']['form']['tax_sign'])
        return res_dict[tax_code.id]

    def _get_tax_codes(self, data):
        return self._compute_totals_tax({})

    def calc_tax(self, tax, is_base, amount, res):
        if not res.get(tax.id):
            res[tax.id] = {'name': tax.name,
                           'base': 0,
                           'tax': 0,
                           }
  
        if is_base:
            # recupero il valore dell'imponibile
            res[tax.id]['base'] += amount
        else:
            # recupero il valore dell'imposta
            res[tax.id]['tax'] += amount


