# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Apruzzese Francesco (f.apruzzese@apuliasoftware.it)
#    Copyright (C) 2015
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


class account_fiscal_position(models.Model):
    _inherit = 'account.fiscal.position'

    intrastat = fields.Boolean(string="Subject to Intrastat")
    intrastat_code_type = fields.Selection([('service', 'Service'),
                                            ('good', 'Good'),
                                            ], string='Code Type')
    intrastat_move_type = fields.Selection(
        [('sale', 'Sales'), ('purchase', 'Purchases'),
         ('refund_sale', 'Refund Sale'), ('refund_purchase', 'Refund Purchase')
         ], string='Move Type')


class account_invoice(models.Model):
    _inherit = "account.invoice"

    intrastat = fields.Boolean(string="Subject to Intrastat",
                               states={'draft': [('readonly', False)]})
    intrastat_line_ids = fields.One2many(
        'account.invoice.intrastat', 'invoice_id', string='Intrastat',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True)

    @api.multi
    def action_move_create(self):
        super(account_invoice, self).action_move_create()
        for invoice in self:
            total_amount = sum(
                l.amount_currency for l in invoice.intrastat_line_ids)
            if not total_amount == invoice.amount_untaxed:
                raise Warning(_('Total Intrastat must be ugual to\
                    Total Invoice Untaxed'))
    
    @api.one
    def compute_intrastat_lines(self):
        
        for line in self.invoice_line:
            # Code competence
            product_template = line.product_id.product_tmpl_id
            intrastat_id = product_template.get_intrastat_id() 
            print "xxx"
            
        
        return True

class account_invoice_intrastat(models.Model):
    _name = 'account.invoice.intrastat'

    @api.one
    @api.depends('amount_currency')
    def _compute_amount_euro(self):
        company_currency = self.invoice_id.company_id.currency_id
        self.amount_euro = company_currency.compute(self.amount_currency,
                                                    company_currency)

    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 required=True)
    intrastat_type_data = fields.Selection([
        ('all', 'All (Fiscal and Statistic'),
        ('fiscal', 'Fiscal'),
        ('statistic', 'Statistic'),
        ], 'Data Type', default='all', required=True)
    intrastat_code_type = fields.Selection([
        ('service', 'Service'),
        ('good', 'Good')
        ], 'Code Type', required=True, default='good')
    intrastat_code_id = fields.Many2one('report.intrastat.code',
                                        string='Intrastat Code')
    amount_euro = fields.Float(
        string='Amount Euro', compute='_compute_amount_euro',
        digits=dp.get_precision('Account'), store=True, readonly=True)
    amount_currency = fields.Float(
        string='Amount Currency', digits=dp.get_precision('Account'))
    transation_nature = fields.Many2one('account.intrastat.transation.nature',
                                        string='Transation Nature')
    weight_kg = fields.Float(string='Weight kg')
    additional_units = fields.Float(string='Additional Units')
    statistic_amount_euro = fields.Float(string='Statistic Amount Euro',
                                         digits=dp.get_precision('Account'))
    delivery_code = fields.Many2one('stock.incoterms',
                                    string='Delivery')
    transport_code = fields.Many2one('account.intrastat.transport',
                                     string='Transport')
    country_origin_id = fields.Many2one('res.country',
                                        string='Country Origin')
    country_good_origin_id = fields.Many2one('res.country',
                                             string='Country Goods Origin')
    province_destination_id = fields.Many2one('res.country.state',
                                              string='Province Destination')

class account_payment_term(models.Model):
    _inherit = 'account.payment.term'

    intrastat_code = fields.Selection([
        ('B', 'Transfer'),
        ('A', 'Accreditation'),
        ('X', 'Other'),
        ], 'Payment Method')
