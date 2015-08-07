# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Openforce di Camilli Alessandro (www.openforce.it)
#    Copyright (C) 2015
#    Author: Apruzzese Francesco (f.apruzzese@apuliasoftware.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
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


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"
    
    def _prepare_intrastat_line(self):
        res = {
            'intrastat_code_id' : False,
            'intrastat_code_type' : False,
            'amount_currency' : False,
            'weight_kg' : False,
            'additional_units' : False,
            # origin
            'country_origin_id' : False,
            'country_good_origin_id' : False,
            'province_origin_id' : False,
            # destination
            'country_destination_id' : False,
            'province_destination_id' : False,
            # invoice ref
            'supply_method' : False,
            'payment_method' : False,
            'country_payment_id' : False,
        }
        product_template = self.product_id.product_tmpl_id
        # Code competence
        intrastat_data = product_template.get_intrastat_data()
        res.update({'intrastat_code_id': intrastat_data['intrastat_code_id']})
        # Type
        res.update({'intrastat_code_type': intrastat_data['intrastat_type']})
        # Amount
        amount_currency = self.price_subtotal
        res.update({'amount_currency': amount_currency})
        # Weight
        intrastat_uom_kg = self.invoice_id.company_id.intrastat_uom_kg_id
        # ...Weight compute in Kg
        # ...If Uom has the same category of kg -> Convert to Kg
        # ...Else the weight will be product weight * qty
        weight_kg = 0
        weight_line = self.quantity * product_template.weight
        if intrastat_uom_kg and product_template.uom_id.category_id.id == \
            intrastat_uom_kg.category_id.id:
                weight_line_kg = self.env['product.uom']._compute_qty(
                    #self.env.cr,
                    #self.env.user.id,
                    product_template.uom_id.id,
                    self.quantity,
                    intrastat_uom_kg.id
                    )
                weight_kg = weight_line_kg
        else:
            weight_kg = weight_line
        res.update({'weight_kg': weight_kg})
        res.update({'additional_units': weight_kg})
        # ---------
        # Origin
        # ---------
        # Country Origin
        country_origin_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            country_origin_id = \
                self.invoice_id.company_id.partner_id.country_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            country_origin_id = \
                self.invoice_id.partner_id.country_id.id
        res.update({'country_origin_id': country_origin_id})
        # Country Good Origin
        country_good_origin_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            country_good_origin_id = \
                self.invoice_id.company_id.partner_id.country_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            country_good_origin_id = \
                self.invoice_id.partner_id.country_id.id
        res.update({'country_good_origin_id': country_good_origin_id})
        # Province Origin
        province_origin_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):    
            province_origin_id = \
                self.invoice_id.partner_id.state_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            province_origin_id = \
                self.invoice_id.company_id.partner_id.state_id.id
        res.update({'province_origin_id': province_origin_id})
        # ---------
        # Destination
        # ---------
        # Country Destination
        country_destination_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):    
            country_destination_id = \
                self.invoice_id.partner_id.country_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            country_destination_id = \
                self.invoice_id.company_id.partner_id.country_id.id
        res.update({'country_destination_id': country_destination_id})
        # Province Destination
        province_destination_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):    
            province_destination_id = \
                self.invoice_id.partner_id.state_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            province_destination_id = \
                self.invoice_id.company_id.partner_id.state_id.id
        res.update({'province_destination_id': province_destination_id})
        # ---------
        # Transportation
        # ---------
        # ---------
        # Invoice Ref #
        # ---------
        # Supply method
        supply_method = False
        # Payment method
        payment_method = False
        if self.invoice_id.payment_term \
                and self.invoice_id.payment_term.intrastat_code:
            payment_method = self.invoice_id.payment_term.intrastat_code
        res.update({'payment_method': payment_method})
        # Country Payment
        country_payment_id = False
        if self.invoice_id.type in ('out_invoice', 'out_refund'):
            country_payment_id = \
                self.invoice_id.partner_id.country_id.id
        elif self.invoice_id.type in ('in_invoice', 'in_refund'):
            country_payment_id = \
                self.invoice_id.company_id.partner_id.country_id.id
        res.update({'country_payment_id': country_payment_id})
        return res
    

class account_invoice(models.Model):
    _inherit = "account.invoice"

    intrastat = fields.Boolean(string="Subject to Intrastat",
                               states={'draft': [('readonly', False)]})
    intrastat_line_ids = fields.One2many(
        'account.invoice.intrastat', 'invoice_id', string='Intrastat',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    
    @api.onchange('fiscal_position')
    def change_fiscal_position(self):
        self.intrastat = self.fiscal_position.intrastat

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
        intrastat_lines = []
        # Unlink existing lines
        for int_line in self.intrastat_line_ids:
            int_line.unlink()
        i_line_by_code = {}
        lines_to_split = []
        for line in self.invoice_line:
            # Lines to compute
            if not line.product_id:
                continue
            product_template = line.product_id.product_tmpl_id
            intrastat_data = product_template.get_intrastat_data()
            if not 'intrastat_code_id' in intrastat_data \
                or not intrastat_data['intrastat_code_id'] \
                or intrastat_data['intrastat_code_id'] == 'exclude':
                continue
            # lines to split at the end
            if intrastat_data['intrastat_code_id'] == 'misc':
                lines_to_split.append(line)
                continue
            
            # Group by intrastat code
            intra_line = line._prepare_intrastat_line()
            if intra_line['intrastat_code_id'] in i_line_by_code:
                i_line_by_code[intra_line['intrastat_code_id']]['amount_currency']+=\
                    intra_line['amount_currency']
                i_line_by_code[intra_line['intrastat_code_id']]['weight_kg']+=\
                    intra_line['weight_kg']
                i_line_by_code[intra_line['intrastat_code_id']]['weight_kg']+=\
                    intra_line['weight_kg']
            else:
                intra_line['statement_section'] = \
                    self.env['account.invoice.intrastat'].\
                        with_context(
                            intrastat_code_type = \
                                intra_line['intrastat_code_type'],
                            invoice_type=self.type).\
                        _get_statement_section()
                i_line_by_code[intra_line['intrastat_code_id']] = intra_line
           
        for key, val in i_line_by_code.iteritems():
            intrastat_lines.append((0,0,val))
        if intrastat_lines:
            self.write({'intrastat_line_ids' : intrastat_lines})


class account_invoice_intrastat(models.Model):
    _name = 'account.invoice.intrastat'

    @api.one
    @api.depends('amount_currency')
    def _compute_amount_euro(self):
        company_currency = self.invoice_id.company_id.currency_id
        self.amount_euro = company_currency.compute(self.amount_currency,
                                                    company_currency)
        self.statistic_amount_euro = self.amount_euro
    @api.one
    @api.depends('invoice_id.partner_id')
    def _compute_partner_data(self):
        self.country_partner_id = self.invoice_id.partner_id.country_id.id
    
    def _get_statement_section(self):
        '''
        Compute where the invoice intrastat data will be computed.
        This field is used to show the right values to fill in
        '''
        invoice_type = self.env.context.get('invoice_type')
        intrastat_code_type = self.env.context.get('intrastat_code_type')
        if not invoice_type:
            invoice_type = self.invoice_id.type
        if not intrastat_code_type:
            intrastat_code_type = self.intrastat_code_type
        section = False
        # Purchase
        if invoice_type in ('in_invoice', 'in_refund'):
            if intrastat_code_type == 'good':
                if invoice_type == 'in_invoice':
                    section = 'purchase_s1'
                else:
                    section = 'purchase_s2'
            else:
                if invoice_type == 'in_invoice':
                    section = 'purchase_s3'
                else:
                    section = 'purchase_s4'
        # Sale
        elif invoice_type in ('out_invoice', 'out_refund'):
            if intrastat_code_type == 'good':
                if invoice_type == 'out_invoice':
                    section = 'sale_s1'
                else:
                    section = 'sale_s2'
            else:
                if invoice_type == 'out_invoice':
                    section = 'sale_s3'
                else:
                    section = 'sale_s4'
        return section
    
    #-------------
    # Defaults
    #-------------
    @api.model
    def _default_province_origin(self):
        if self.invoice_id.company_id.partner_id.state_id:
            return self.invoice_id.company_id.partner_id.state_id
        else:
            return False
    
    @api.model
    def _default_country_destination(self):
        if self.invoice_id.partner_id.country_id:
            return self.invoice_id.partner_id.country_id
        else:
            return False
    

    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', required=True)
    intrastat_type_data = fields.Selection([
        ('all', 'All (Fiscal and Statistic'),
        ('fiscal', 'Fiscal'),
        ('statistic', 'Statistic'),
        ], 'Data Type', default='all', required=True)
    intrastat_code_type = fields.Selection([
        ('service', 'Service'),
        ('good', 'Good')
        ], 'Code Type', required=True, default='good')
    intrastat_code_id = fields.Many2one(
        'report.intrastat.code', string='Intrastat Code', required=True)
    statement_section = fields.Selection([
        ('sale_s1', 'Sale s1'),
        ('sale_s2', 'Sale s2'),
        ('sale_s3', 'Sale s3'),
        ('sale_s4', 'Sale s4'),
        ('purchase_s1', 'Purchase s1'),
        ('purchase_s2', 'Purchase s2'),
        ('purchase_s3', 'Purchase s3'),
        ('purchase_s4', 'Purchase s4'),
        ], 'Statement Section', default=_get_statement_section
        )
    
    amount_euro = fields.Float(
        string='Amount Euro', compute='_compute_amount_euro',
        digits=dp.get_precision('Account'), store=True, readonly=True)
    amount_currency = fields.Float(
        string='Amount Currency', digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one('account.intrastat.transation.nature',
                                        string='Transation Nature')
    weight_kg = fields.Float(string='Weight kg')
    additional_units = fields.Float(string='Additional Units')
    statistic_amount_euro = fields.Float(string='Statistic Amount Euro',
                                         digits=dp.get_precision('Account'))
    country_partner_id = fields.Many2one(
        'res.country', string='Country Partner', 
        compute='_compute_partner_data', store=True, readonly=True)
    ## Origin ##
    province_origin_id = fields.Many2one(
         'res.country.state', string='Province Origin',
         default =_default_province_origin)
    country_origin_id = fields.Many2one('res.country', string='Country Origin')
    country_good_origin_id = fields.Many2one(
        'res.country', string='Country Goods Origin')
    ## Destination ##
    delivery_code_id = fields.Many2one('stock.incoterms', string='Delivery')
    transport_code_id = fields.Many2one(
        'account.intrastat.transport', string='Transport')
    province_destination_id = fields.Many2one('res.country.state',
                                              string='province destination')
    country_destination_id = fields.Many2one(
        'res.country', string='Country Destination',
         default =_default_country_destination)
    ## Invoice Ref ##
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    supply_method = fields.Selection([
        ('I', 'Instant'),
        ('R', 'Repeatedly'),
        ], 'Supply Method')
    payment_method = fields.Selection([
        ('B', 'Transfer'),
        ('A', 'Accreditation'),
        ('X', 'Other'),
        ], 'Payment Method')
    country_payment_id= fields.Many2one('res.country', 'Country Payment')
                                
    @api.onchange('weight_kg')
    def change_weight_kg(self):
        self.additional_units = self.weight_kg
    
    @api.onchange('amount_euro')
    def change_amount_euro(self):
        self.statistic_amount_euro = self.amount_euro 
        
    @api.onchange('intrastat_code_type')
    def change_intrastat_code_type(self):
        self.statement_section = self._get_statement_section()
        self.intrastat_code_id = False
    
    
class account_payment_term(models.Model):
    _inherit = 'account.payment.term'

    intrastat_code = fields.Selection([
        ('B', 'Transfer'),
        ('A', 'Accreditation'),
        ('X', 'Other'),
        ], 'Payment Method')
