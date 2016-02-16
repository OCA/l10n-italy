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
from openerp.exceptions import except_orm, ValidationError
from openerp import netsvc


class withholding_tax(models.Model):
    _name = 'withholding.tax'
    _description = 'Withholding Tax'
    
    
    @api.one
    @api.depends('rate_ids.date_start', 'rate_ids.date_stop', 'rate_ids.base', 
                 'rate_ids.tax')
    def _get_rate(self):
        self.env.cr.execute('''
            SELECT tax, base FROM withholding_tax_rate 
                WHERE withholding_tax_id = %s
                 and (date_start <= current_date or date_start is null)
                ORDER by date_start LIMIT 1''', 
                (self.id,))
        rate = self.env.cr.fetchone()
        if rate:
            self.tax = rate[0]
            self.base = rate[1]
        else:
            self.tax = 0
            self.base = 1
    
    active = fields.Boolean('Active', default = True)
    name = fields.Char('Name', size=256, required=True)
    certification = fields.Boolean('Certification')
    comment = fields.Text('Text')
    account_receivable_id = fields.Many2one('account.account', 
            'Account Receivable', required=True, 
            domain=[('type','=', 'receivable')])
    account_payable_id = fields.Many2one('account.account', 
            'Account Payable', required=True, domain=[('type','=', 'payable')])
    payment_term = fields.Many2one('account.payment.term', 'Payment Terms', 
                                   required=True)
    tax = fields.Float(string='Tax %', compute='_get_rate')
    base = fields.Float(string='Base', compute='_get_rate')
    rate_ids = fields.One2many('withholding.tax.rate', 'withholding_tax_id', 
                               'Rates', required=True)

    def compute_amount(self, amount_invoice, invoice_id=None):
        invoice_obj = self.env['account.invoice']
        res = {
            'base' : 0,
            'tax' : 0
            }
        if not amount_invoice and invoice_id:
            invoice = invoice_obj.browse(invoice_id)
            amount_invoice = invoice.amount_untaxed
        #v7->v8 removed tax = self.browse(cr, uid, withholding_tax_id)
        base = amount_invoice * self.base
        tax = base * ((self.tax or 0.0)/100.0)
        
        res['base'] = base
        res['tax'] = tax
        
        return res
    
    @api.one
    def get_base_from_tax(self, wt_amount):
        '''
        100 * wt_amount        1
        ---------------  *  -------
              % tax          Coeff
        '''
        dp_obj = self.env['decimal.precision']
        base = 0
        if wt_amount:
            #wt = self.browse(cr, uid, withholding_tax_id)
            base = round( (100 * wt_amount / self.tax) * (1 / self.base), \
                            dp_obj.precision_get('Account'))
        return base
    

class withholding_tax_rate(models.Model):
    _name = 'withholding.tax.rate'
    _description = 'Withholding Tax Rates'
    
    
    @api.one
    @api.constrains('date_start', 'date_stop')
    def _check_date(self):
        if self.withholding_tax_id.active:
            where = []
            if self.date_start:
                where.append("((date_stop>='%s') or (date_stop is null))" % \
                             (self.date_start,))
            if self.date_stop:
                where.append("((date_start<='%s') or (date_start is null))" % \
                             (self.date_stop,))

            self.env.cr.execute('SELECT id ' \
                    'FROM withholding_tax_rate ' \
                    'WHERE '+' and '.join(where) + (where and ' and ' or '') +
                        'withholding_tax_id = %s ' \
                        'AND id <> %s', (
                            self.withholding_tax_id.id,
                            self.id))
            if self.env.cr.fetchall():
                raise ValidationError(
                    _('Error! You cannot have 2 pricelist versions that \
                    overlap!'))

    withholding_tax_id = fields.Many2one('withholding.tax', 
                                         string='Withholding Tax', 
                                         ondelete='cascade', readonly=True)
    date_start = fields.Date(string='Date Start')
    date_stop = fields.Date(string='Date Stop')
    comment = fields.Text(string='Text')
    base = fields.Float(string='Base Coeff.', default=1)
    tax = fields.Float(string='Tax %')
    


class withholding_tax_statement(models.Model):
    '''
    The Withholding tax statement are created at the invoice validation
    '''
    
    _name = 'withholding.tax.statement'
    _description = 'Withholding Tax Statement'
    
    @api.multi
    @api.depends('move_ids.amount', 'move_ids.state')
    def _compute_total(self):
        for statement in self:
            tot_wt_amount = 0
            tot_wt_amount_paid = 0
            for wt_move in statement.move_ids:
                tot_wt_amount += wt_move.amount
                if wt_move.state == 'paid':
                    tot_wt_amount_paid += wt_move.amount
            statement.amount = tot_wt_amount
            statement.amount_paid = tot_wt_amount_paid
    
    
    date = fields.Date('Date')
    move_id = fields.Many2one('account.move', 'Account move', 
                               ondelete='cascade')
    invoice_id = fields.Many2one('account.invoice', 'Invoice', 
                                  ondelete='cascade')
    partner_id = fields.Many2one('res.partner', 'Partner')
    withholding_tax_id = fields.Many2one('withholding.tax', 
                                          string='Withholding Tax')
    base = fields.Float('Base')
    tax = fields.Float('Tax')
    amount = fields.Float(string='WT amount', store=True, readonly=True,
                           compute='_compute_total')
    amount_paid = fields.Float(string='WT amount paid', store=True, 
                               readonly=True, compute='_compute_total')
    move_ids = fields.One2many('withholding.tax.move', 
                        'statement_id', 'Moves')
    
class withholding_tax_move(models.Model):
    '''
    The Withholding tax moves are created at the payment of invoice using
    voucher
    '''
    _name = 'withholding.tax.move'
    _description = 'Withholding Tax Move'
    
    state = fields.Selection([
        ('due', 'Due'),
        ('paid', 'Paid'),
        ], 'Status', readonly=True, copy=False, select=True, 
                              default='due')
    statement_id = fields.Many2one('withholding.tax.statement', 'Statement')
    date = fields.Date('Date Competence') 
    wt_voucher_line_id = fields.Many2one('withholding.tax.voucher.line', 
                                         'WT Account Voucher Line', 
                                         ondelete='cascade')
    move_line_id = fields.Many2one('account.move.line', 'Account Move line', 
        ondelete='cascade', help="Used from trace WT from other parts(BS)")
    withholding_tax_id = fields.Many2one('withholding.tax', 'Withholding Tax')
    amount = fields.Float('Amount')
    partner_id = fields.Many2one('res.partner', 'Partner')
    date_maturity = fields.Date('Date Maturity')
    account_move_id = fields.Many2one('account.move', 'Account Move', 
                         ondelete='cascade')
    
    @api.multi
    def action_paid(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'paid', 
                                    self.env.cr)
        return True
    
    @api.multi
    def action_set_to_draft(self):
        for pt in self:
            wf_service = netsvc.LocalService("workflow")
            wf_service.trg_validate(self.env.uid, self._name, pt.id, 'cancel', 
                                    self.env.cr)
        return True
    
    @api.multi
    #def move_paid(self, cr, uid, ids, *args):
    def move_paid(self):
        for move in self:
            if move.state in ['due']:
                move.write({'state': 'paid'})
        return True
    
    @api.multi
    #def move_set_due(self, cr, uid, ids, *args):
    def move_set_due(self):
        for move in self:
            if move.state in ['paid']:
                move.write({'state': 'due'})
        return True
    
    @api.multi
    def unlink(self):
        # To avoid if move is linked to voucher
        for move in self:
            if move.wt_voucher_line_id \
                    and move.wt_voucher_line_id.voucher_line_id:
                raise ValidationError(
                    _('Warning! You cannot delet move linked to voucher.You \
                    must before delete the voucher.'))
        return super(withholding_tax_move, self).unlink()
    