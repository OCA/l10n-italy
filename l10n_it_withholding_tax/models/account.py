# -*- coding: utf-8 -*-
##############################################################################
#    
#    @author: Alessandro Camilli (alessandrocamilli@openforce.it)
#    Copyright (C) 2015
#    Openforce (<http://www.openforce.it>)
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning


class account_move(models.Model):
    _inherit = "account.move"
    
    @api.one
    def _prepare_wt_values(self):
        
        partner = False
        wt_competence = {}
        
        # Fist : Partner and WT competence
        for line in self.line_id:
            if line.partner_id:
                partner = line.partner_id
                if partner.property_account_position:
                    for wt in \
                        partner.property_account_position.withholding_tax_ids:
                        wt_competence[wt.id] = {
                                'withholding_tax_id': wt.id,
                                'partner_id': partner.id,
                                'date': self.date,
                                'account_move_id': self.id,
                                'wt_account_move_line_id': False,
                                'base': 0,
                                'amount': 0,
                            } 
                break
        # After : Loking for WT lines
        base = 0
        wt_amount = 0
        for line in self.line_id:
            domain = []
            # WT line
            if line.credit:
                domain.append(('account_payable_id', '=', \
                                                line.account_id.id))
                amount = line.credit
            else:
                domain.append(('account_receivable_id', '=', \
                                                line.account_id.id))
                amount = line.debit
            wt_ids = self.pool['withholding.tax'].search(self.env.cr,
                                                         self.env.uid,
                                                         domain)
            if wt_ids:
                wt_amount += amount
                if wt_competence and wt_competence[wt_ids[0]] \
                    and 'amount' in wt_competence[wt_ids[0]]:
                    wt_competence[wt_ids[0]]['wt_account_move_line_id'] =\
                                            line.id
                    wt_competence[wt_ids[0]]['amount'] = wt_amount
                    wt_competence[wt_ids[0]]['base'] = \
                        self.pool['withholding.tax'].get_base_from_tax(
                                            self.env.cr, self.env.uid, 
                                            wt_ids[0], wt_amount)
            # WT Base 
            #if line.account_id.type in ['other']:
        
        wt_codes = []
        if wt_competence:
            for key, val in wt_competence.items():
                wt_codes.append(val)
        res = {
            'partner_id' : partner and partner.id or False,
            'move_id' : self.id,
            'invoice_id' : False,
            'date' : self.date,
            'base': wt_codes and wt_codes[0]['base'] or 0,
            'tax': wt_codes and wt_codes[0]['amount'] or 0,
            'withholding_tax_id' : wt_codes and \
                wt_codes[0]['withholding_tax_id'] or False,
            'wt_account_move_line_id' : wt_codes and \
                wt_codes[0]['wt_account_move_line_id'] or False,
            'amount' : wt_codes[0]['amount'],
        }                
        
        return res


class account_move_line(models.Model):
    _inherit = "account.move.line"
    
    withholding_tax_amount = fields.Float(string = 'Withholding Tax Amount')
    
    
class account_fiscal_position(models.Model):
    _inherit = "account.fiscal.position"
            
    withholding_tax_ids = fields.Many2many(
        'withholding.tax', 'account_fiscal_position_withholding_tax_rel', 
        'fiscal_position_id', 'withholding_tax_id', string='Withholding Tax')
    
    
class account_invoice(models.Model):
    _inherit = "account.invoice"
    
    @api.multi
    @api.depends('withholding_tax_line')
    def _amount_withholding_tax(self):
        res = {}
        dp_obj = self.env['decimal.precision']
        for invoice in self:
            withholding_tax_amount = 0.0
            for wt_line in invoice.withholding_tax_line:
                withholding_tax_amount += round(wt_line.tax, 
                                                dp_obj.precision_get('Account'))
            invoice.amount_net_pay = invoice.amount_total - \
                withholding_tax_amount
            invoice.withholding_tax_amount = withholding_tax_amount
        return res
    
    withholding_tax = fields.Boolean('Withholding Tax')
    withholding_tax_line = fields.One2many(
        'account.invoice.withholding.tax', 'invoice_id', 'Withholding Tax', 
        readonly=True, states={'draft':[('readonly',False)]})
    withholding_tax_amount = fields.Float(compute='_amount_withholding_tax', 
        digits=dp.get_precision('Account'), string='Withholding tax', 
        store=True, readonly=True)
    amount_net_pay = fields.Float(compute='_amount_withholding_tax', 
        digits_compute=dp.get_precision('Account'), string='Net To Pay', 
        store=True, readonly=True)
    
    @api.multi
    def action_move_create(self):
        '''
        Split amount withholding tax on account move lines
        '''
        dp_obj = self.env['decimal.precision']
        res = super(account_invoice, self).action_move_create()
        
        for inv in self:
            # Rates
            rate_num = 0
            for move_line in inv.move_id.line_id:
                if not move_line.date_maturity:
                    continue
                rate_num += 1
            #
            if rate_num:
                wt_rate = round(inv.withholding_tax_amount / rate_num, \
                                dp_obj.precision_get('Account'))
            wt_residual = inv.withholding_tax_amount
            # Re-read move lines to assign the amounts of wt
            i = 0
            for move_line in inv.move_id.line_id:
                if not move_line.date_maturity:
                    continue
                i += 1
                if i == rate_num:
                    wt_amount = wt_residual
                else:
                    wt_amount = wt_rate
                wt_residual -= wt_amount
                # update line
                move_line.write({'withholding_tax_amount': wt_amount})
        
            # Align with WT statement
            for wt_inv_line in inv.withholding_tax_line:
                wt_inv_line._align_statement()
        
        return res
    
    @api.multi
    def compute_all_withholding_tax(self):
        
        for invoice in self:
            # Clear for recompute o because there isn't withholding_tax to True 
            if invoice.fiscal_position or not invoice.withholding_tax:
                self.env.cr.execute("DELETE FROM \
                    account_invoice_withholding_tax WHERE invoice_id=%s ", 
                    (invoice.id,))
            if invoice.withholding_tax and invoice.fiscal_position and \
                    invoice.fiscal_position.withholding_tax_ids:
                for tax in invoice.fiscal_position.withholding_tax_ids:
                    tot_invoice = 0
                    withholding_tax = tax.compute_amount(tot_invoice, 
                                                         invoice.id)
                    val = {
                        'invoice_id' : invoice.id,
                        'withholding_tax_id' : tax.id,
                        'base': withholding_tax['base'],
                        'tax': withholding_tax['tax']
                        }
                    self.env['account.invoice.withholding.tax'].create(val)
    
    @api.one
    def button_reset_taxes(self):
        res = super(account_invoice, self).button_reset_taxes()
        self.compute_all_withholding_tax()
        return res
    
    @api.onchange('fiscal_position')
    def onchange_fiscal_position(self):
        use_wt = False
        if self.fiscal_position and self.fiscal_position.withholding_tax_ids:
            use_wt= True
        self.withholding_tax = use_wt
            
    
class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"
    '''
    def compute_amount_line(self, cr, uid, line):
        
        dp_obj = self.pool['decimal.precision']
        price_subtotal = 0  
        price = line['price_unit'] * (1-(line['discount'] or 0.0)/100.0)
        if 'discount2' in line: # field of my customization
            price = price * (1-(line['discount2'] or 0.0)/100.0)
        price_subtotal = round(price * line['quantity'], 
            dp_obj.precision_get(cr, uid, 'Account'))
        
        return price_subtotal'''


class account_invoice_withholding_tax(models.Model):
    '''
    Withholding tax lines in the invoice
    '''
    
    _name = 'account.invoice.withholding.tax'
    _description = 'Invoice Withholding Tax Line'
    
    invoice_id = fields.Many2one('account.invoice', string='Invoice', 
                                 ondelete="cascade")
    withholding_tax_id = fields.Many2one('withholding.tax', 
                                         string='Withholding tax')
    base = fields.Float('Base')
    tax = fields.Float('Tax')
    
    @api.multi
    def _align_statement(self):
        '''
        Align statement values with wt lines invoice
        '''
        wt_st_id =False
        for wt_inv_line in self:
            domain = [('move_id', '=', wt_inv_line.invoice_id.move_id.id),
                      ('withholding_tax_id', '=', 
                       wt_inv_line.withholding_tax_id.id)]
            wt_st_ids = self.env['withholding.tax.statement'].search(domain)
            # Create statemnt if doesn't exist
            if not wt_st_ids:
                vals = {
                    'date' : wt_inv_line.invoice_id.move_id.date,
                    'move_id' : wt_inv_line.invoice_id.move_id.id,
                    'invoice_id' : wt_inv_line.invoice_id.id,
                    'partner_id' : wt_inv_line.invoice_id.partner_id.id,
                    'withholding_tax_id' : wt_inv_line.withholding_tax_id.id,
                }
                wt_st_id = self.env['withholding.tax.statement'].create(vals)
            else:
                wt_st_id = wt_st_ids
            # Update values
            vals = {
                'base': wt_inv_line.base,
                'tax': wt_inv_line.tax
            }
            wt_st_id.write(vals)
            
        return wt_st_id
    
    @api.onchange('fiscal_position')
    def onchange_fiscal_position(self):
        use_wt = False
        if self.fiscal_position and self.fiscal_position.withholding_tax_ids:
            use_wt= True
        self.withholding_tax = use_wt
    
    @api.onchange('withholding_tax_id')
    def onchange_withholding_tax_id(self):
        res = {}
        if self.withholding_tax_id:
            tot_invoice = 0
            for inv_line in self.invoice_id.invoice_line:
                tot_invoice += inv_line.price_subtotal
            tax = self.withholding_tax_id.compute_amount(tot_invoice, 
                                                             invoice_id=None)
            self.base = tax['base']
            self.tax = tax['tax']
        
        