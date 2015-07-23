# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2014
#    Openforce di Camilli Alessandro (www.openforce.it)
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
from datetime import datetime, date

class account_intrastat_custom(models.Model):
    _name = 'account.intrastat.custom'
    _description = 'Account INTRASTAT - Customs'
    
    code = fields.Char(string='Code', size=6)
    name = fields.Char(string='Name')
    date_start = fields.Date(string='Date start')
    date_stop = fields.Date(string='Date stop')


class report_intrastat_code(models.Model):

    _inherit = 'report.intrastat.code'

    active = fields.Boolean(default=True)
    type = fields.Selection(
        [('good', 'Good'), ('service', 'Service')])


class account_intrastat_transport(models.Model):
    _name = 'account.intrastat.transport'
    _description = 'Account INTRASTAT - Transport'
    
    code = fields.Char(string='Code', size=1, required=True)
    name = fields.Char(string='Name')


class account_intrastat_transation_nature(models.Model):
    _name = 'account.intrastat.transation.nature'
    _description = 'Account INTRASTAT - Transation Nature'
    
    code = fields.Char(string='Code', size=1, required=True)
    name = fields.Char(string='Name')


class account_intrastat_statement(models.Model):
    _name = 'account.intrastat.statement'
    _description = 'Account INTRASTAT - Statement'

    @api.model
    def _default_company(self):
        company_id = self._context.get('company_id',
                                       self.env.user.company_id.id)
        return company_id
    
    @api.model
    def _default_company_vat(self):
        company_id = self._context.get(
            'company_id', self.env.user.company_id.id)
        if company_id:
            return self.env['res.company'].browse(company_id).partner_id.vat
        else:
            return False

    @api.one
    @api.depends('sale_section1_ids.amount_euro')
    def _compute_amount_sale_s1(self):
        self.sale_section1_operation_number = len(self.sale_section1_ids)
        self.sale_section1_operation_amount = sum(
            line.amount_euro for line in self.sale_section1_ids)

    @api.one
    @api.depends('sale_section2_ids.amount_euro')
    def _compute_amount_sale_s2(self):
        self.sale_section2_operation_number = len(self.sale_section2_ids)
        self.sale_section2_operation_amount = sum(
            line.amount_euro for line in self.sale_section2_ids)

    @api.one
    @api.depends('sale_section3_ids.amount_euro')
    def _compute_amount_sale_s3(self):
        self.sale_section3_operation_number = len(self.sale_section3_ids)
        self.sale_section3_operation_amount = sum(
            line.amount_euro for line in self.sale_section3_ids)

    @api.one
    @api.depends('sale_section4_ids.amount_euro')
    def _compute_amount_sale_s4(self):
        self.sale_section4_operation_number = len(self.sale_section4_ids)
        self.sale_section4_operation_amount = sum(
            line.amount_euro for line in self.sale_section4_ids)

    @api.one
    @api.depends('purchase_section1_ids.amount_euro')
    def _compute_amount_purchase_s1(self):
        self.purchase_section1_operation_number = len(
            self.purchase_section1_ids)
        self.purchase_section1_operation_amount = sum(
            line.amount_euro for line in self.purchase_section1_ids)

    @api.one
    @api.depends('purchase_section2_ids.amount_euro')
    def _compute_amount_purchase_s2(self):
        self.purchase_section2_operation_number = len(
            self.purchase_section2_ids)
        self.purchase_section2_operation_amount = sum(
            line.amount_euro for line in self.purchase_section2_ids)

    @api.one
    @api.depends('purchase_section3_ids.amount_euro')
    def _compute_amount_purchase_s3(self):
        self.purchase_section3_operation_number = len(
            self.purchase_section3_ids)
        self.purchase_section3_operation_amount = sum(
            line.amount_euro for line in self.purchase_section3_ids)

    @api.one
    @api.depends('purchase_section4_ids.amount_euro')
    def _compute_amount_purchase_s4(self):
        self.purchase_section4_operation_number = len(
            self.purchase_section4_ids)
        self.purchase_section4_operation_amount = sum(
            line.amount_euro for line in self.purchase_section4_ids)
        
    @api.model
    def _compute_progressive(self):
        '''
        Assign univoque progressive to statement
        '''
        # From last statement
        st = self.search([], order='number', limit=1)
        if st:
            self.write({'number' : st.number+1})
        else:
            self.write({'number' : 1})

    number = fields.Integer(string='Number', store=True, 
                         readonly=True, compute='_compute_progressive')
    company_id = fields.Many2one(
        'res.company', string='Company', default=_default_company, 
        required=True)
    vat_taxpayer = fields.Char(
        string='Vat taxpayer', required=True, default=_default_company_vat)
    fiscalyear_id = fields.Many2one(
        'account.fiscalyear', string='Year', required=True)
    period_type = fields.Selection([
        ('M', 'Month'),
        ('T', 'Quarterly'),
        ], 'Period Type', required=True)
    period_number = fields.Integer(
        string='Period',
        help="Values accepted:\
        - Month : From 1 to 12 \
        - Quarterly: From 1 to 4", required=True)
    content_type = fields.Selection([
        ('0', 'Normal Period'),
        ('8', 'Change Period in quarterly: only first month operations'),
        ('9', 'Change Period in quarterly: only first and second month \
            operations'),
        ], 'Content Type', required=True, default="0")
    special_cases = fields.Selection([
        ('7', 'First Statement'),
        ('8', 'Change VAT or Close Activity'),
        ('9', 'First Statement in Change VAT or Close Activity'),
        ('0', 'None of the above cases'),
        ], 'Special Cases', required=True, default="0")
        
    sale = fields.Boolean(string='Sale', default=True)
    purchase = fields.Boolean(string='Purchase', default=True)

    intrastat_type_data = fields.Selection([
        ('all', 'All (Fiscal and Statistic'),
        ('fiscal', 'Fiscal'),
        ('statistic', 'Statistic'),
        ], 'Data Type', required=True, default='all')
    intrastat_code_type = fields.Selection([
        ('service', 'Service'),
        ('good', 'Good')
        ], 'Code Type', required=True, default='good')

    sale_section1_ids = fields.One2many(
        'account.intrastat.statement.sale.section1',
        'statement_id', string='Sale - Section 1')
    sale_section1_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_sale_s1')
    sale_section1_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_sale_s1')
    sale_section2_ids = fields.One2many(
        'account.intrastat.statement.sale.section2',
        'statement_id', string='Sale - Section 2')
    sale_section2_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_sale_s2')
    sale_section2_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_sale_s2')
    sale_section3_ids = fields.One2many(
        'account.intrastat.statement.sale.section3',
        'statement_id', string='Sale - Section 3')
    sale_section3_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_sale_s3')
    sale_section3_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_sale_s3')
    sale_section4_ids = fields.One2many(
        'account.intrastat.statement.sale.section4',
        'statement_id', string='Sale - Section 4')
    sale_section4_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_sale_s4')
    sale_section4_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_sale_s4')

    purchase_section1_ids = fields.One2many(
        'account.intrastat.statement.purchase.section1',
        'statement_id', string='Purchase - Section 1')
    purchase_section1_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_purchase_s1')
    purchase_section1_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_purchase_s1')
    purchase_section2_ids = fields.One2many(
        'account.intrastat.statement.purchase.section2',
        'statement_id', string='Purchase - Section 2')
    purchase_section2_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_purchase_s2')
    purchase_section2_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_purchase_s2')
    purchase_section3_ids = fields.One2many(
        'account.intrastat.statement.purchase.section3',
        'statement_id', string='Purchase - Section 3')
    purchase_section3_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_purchase_s3')
    purchase_section3_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_purchase_s3')
    purchase_section4_ids = fields.One2many(
        'account.intrastat.statement.purchase.section4',
        'statement_id', string='Purchase - Section 4')
    purchase_section4_operation_number = fields.Integer(
        string='Operation Nr', store=True, readonly=True,
        compute='_compute_amount_purchase_s4')
    purchase_section4_operation_amount = fields.Integer(
        string='Operation Amount', store=True, readonly=True,
        compute='_compute_amount_purchase_s4')

    @api.one
    def compute_statement(self):
        # Unlink existing lines
        for line in self.sale_section1_ids:
            line.unlink()
        for line in self.sale_section2_ids:
            line.unlink()
        for line in self.sale_section3_ids:
            line.unlink()
        for line in self.sale_section4_ids:
            line.unlink()
        for line in self.purchase_section1_ids:
            line.unlink()
        for line in self.purchase_section2_ids:
            line.unlink()
        for line in self.purchase_section3_ids:
            line.unlink()
        for line in self.purchase_section4_ids:
            line.unlink()
        # Setting period
        date_start_year = datetime.strptime(self.fiscalyear_id.date_start, 
                                            '%Y-%m-%d')
        if self.period_type == 'M':
            period_date_start = datetime(date_start_year.year, 
                                         self.period_number, 
                                         1)
            period_date_stop = datetime(date_start_year.year, 
                                        self.period_number, 
                                        31)
        else:
            if self.period_number == 1:
                period_date_start = datetime(date_start_year.year, 1, 1)
                period_date_stop = datetime(date_start_year.year, 3, 31)
            elif self.period_number == 2:
                period_date_start = datetime(date_start_year.year, 3, 1)
                period_date_stop = datetime(date_start_year.year, 6, 30)
            elif self.period_number == 3:
                period_date_start = datetime(date_start_year.year, 7, 1)
                period_date_stop = datetime(date_start_year.year, 9, 30)
            elif self.period_number == 4:
                period_date_start = datetime(date_start_year.year, 10, 1)
                period_date_stop = datetime(date_start_year.year, 12, 31)
                
        # Search intrastat lines
        domain = [('move_id.date', '>=', period_date_start),
                  ('move_id.date', '<=', period_date_stop),
                  ('intrastat', '=', True)]
        
        statement_lines_sale_s1 = []
        statement_lines_sale_s2 = []
        statement_lines_sale_s3 = []
        statement_lines_sale_s4 = []
        statement_lines_purchase_s1 = []
        statement_lines_purchase_s2 = []
        statement_lines_purchase_s3 = []
        statement_lines_purchase_s4 = []
        for inv in self.env['account.invoice'].search(domain):
            print inv.name
            for inv_intra_line in inv.intrastat_line_ids:
                # Sale - Section 1
                if inv_intra_line.statement_section == 'sale_s1':
                    st_line = \
                        self.env['account.intrastat.statement.sale.section1']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_sale_s1):
                            st_line['progressive'] = \
                                len(statement_lines_sale_s1) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_sale_s1.append((0, 0, st_line))
                #elif int_line.statement_section == 'sale_s2':
                #elif int_line.statement_section == 'sale_s3':
                #elif int_line.statement_section == 'sale_s4':
        self.write({
            'sale_section1_ids' : statement_lines_sale_s1,
            'sale_section2_ids' : statement_lines_sale_s2,
            'sale_section3_ids' : statement_lines_sale_s3,
            'sale_section4_ids' : statement_lines_sale_s4,
            'purchase_section1_ids' : statement_lines_purchase_s1,
            'purchase_section2_ids' : statement_lines_purchase_s2,
            'purchase_section3_ids' : statement_lines_purchase_s3,
            'purchase_section4_ids' : statement_lines_purchase_s4,
            })
        
        return True
        
    @api.onchange('company_id')
    def change_company_id(self):
        self.vat_taxpayer = self.company_id.partner_id.vat
    
    @api.onchange('period_number')
    @api.constrains('period_type', 'period_number')
    def change_period_number(self):
        '''
        Interval Control
        '''
        if self.period_type == 'M'\
            and (self.period_number < 1 or self.period_number > 12):
            raise ValidationError(
                _('Period Not Valid! Range accepted: from 1 to 12'))
        if self.period_type == 'T'\
            and (self.period_number < 1 or self.period_number > 4):
            raise ValidationError(
                _('Period Not Valid! Range accepted: from 1 to 4'))
            

class account_intrastat_statement_sale_section1(models.Model):
    _name = 'account.intrastat.statement.sale.section1'
    _description = 'Account INTRASTAT - Statement - Sale Section 1'
    
    statement_id = fields.Many2one(
        'account.intrastat.statement', string='Statement', 
        required=True, readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Customer')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Good')
    weight_kg = fields.Float(string='Weight kg')
    additional_units = fields.Float(string='Additional Units')
    statistic_amount_euro = fields.Float(string='Statistic Amount Euro', 
                                         digits=dp.get_precision('Account'))
    delivery_code_id = fields.Many2one('stock.incoterms', 
                                    string='Delivery')
    transport_code_id = fields.Many2one('account.intrastat.transport', 
                                     string='Transport')
    country_destination_id = fields.Many2one('res.country', 
                                             string='Country Destination')
    province_origin_id = fields.Many2one('res.country.state', 
                                         string='Province Origin')
    invoice_id = fields.Many2one('account.invoice',
                                 string='Invoice', readonly=True)
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code': inv_intra_line.invoice_id.partner_id.vat or False,
            'amount_euro': inv_intra_line.amount_euro or 0,
            'transation_nature_id': inv_intra_line.transation_nature_id.id \
                or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'weight_kg': inv_intra_line.weight_kg or 0,
            'additional_units': inv_intra_line.additional_units or 0,
            'statistic_amount_euro': inv_intra_line.statistic_amount_euro or 0,
            'delivery_code_id': inv_intra_line.delivery_code_id and \
                inv_intra_line.delivery_code_id.id or False,
            'transport_code_id': inv_intra_line.transport_code_id and \
                inv_intra_line.transport_code_id.id or False,
            'country_destination_id': inv_intra_line.country_destination_id \
                and inv_intra_line.country_destination_id.id or False,
            'province_origin_id': inv_intra_line.province_origin_id \
                and inv_intra_line.province_origin_id.id or False,
        }
        
        return res
    

class account_intrastat_statement_sale_section2(models.Model):
    _name = 'account.intrastat.statement.sale.section2'
    _description = 'Account INTRASTAT - Statement - Sale Section 2'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement',
                                   required=True, readonly=True)
    progressive = fields.Integer(string='Progressive', required=True, 
                                 readonly=True)
    
    month = fields.Integer(string='Month Ref of Refund')
    quarterly = fields.Integer(string='Quarterly Ref of Refund')
    year = fields.Many2one('account.fiscalyear', string='Year Ref of Refund')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    sign_variation = fields.Selection([
        ('+', '+'),
        ('-', '-'),
        ], 'Sign Variation')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one('account.intrastat.transation.nature', 
                                        string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Good')
    statistic_amount_euro = fields.Float(string='Statistic Amount Euro', 
                                         digits=dp.get_precision('Account'))
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)


class account_intrastat_statement_sale_section3(models.Model):
    _name = 'account.intrastat.statement.sale.section3'
    _description = 'Account INTRASTAT - Statement - Sale Section 3'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True, 
                                 readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Service')
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
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)


class account_intrastat_statement_sale_section4(models.Model):
    _name = 'account.intrastat.statement.sale.section4'
    _description = 'Account INTRASTAT - Statement - Sale Section 4'
    
    statement_id = fields.Many2one(
        'account.intrastat.statement', string='Statement', 
        required=True, readonly=True)
    progressive = fields.Integer(
        string='Progressive', required=True, readonly=True)
    custom = fields.Many2one('account.intrastat.custom', 'Custom')
    year = fields.Many2one('account.fiscalyear', 
                           string='Year Ref of Variation')
    protocol = fields.Integer(string='Protocol number', size=6)
    progressive_to_modify_id =  fields.Many2one(
        'account.intrastat.statement.sale.section1', 'Progressive to Modify')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Service')
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
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)


class account_intrastat_statement_purchase_section1(models.Model):
    _name = 'account.intrastat.statement.purchase.section1'
    _description = 'Account INTRASTAT - Statement - Purchase Section 1'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Float(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Float(string='Amount Currency', 
                                   digits=dp.get_precision('Account'))
    transation_nature = fields.Many2one('account.intrastat.transation.nature',
                                        string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Good')
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
                                             string='Country Good Origin')
    province_destination_id = fields.Many2one('res.country.state', 
                                              string='Province Destination')
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)


class account_intrastat_statement_purchase_section2(models.Model):
    _name = 'account.intrastat.statement.purchase.section2'
    _description = 'Account INTRASTAT - Statement - Purchase Section 2'
    
    statement_id = fields.Many2one('account.intrastat.statement', 
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    month = fields.Integer(string='Month Ref of Refund')
    quarterly = fields.Integer(string='Quarterly Ref of Refund')
    year = fields.Many2one('account.fiscalyear', string='Year Ref of Refund')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    sign_variation = fields.Selection([
        ('+', '+'),
        ('-', '-'),
        ], 'Sign Variation')
    amount_euro = fields.Float(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Float(string='Amount Currency',
                                   digits=dp.get_precision('Account'))
    transation_nature = fields.Many2one('account.intrastat.transation.nature',
                                        string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code',
                                        string='Intrastat Code Good')
    statistic_amount_euro = fields.Float(string='Statistic Amount Euro',
                                         digits=dp.get_precision('Account'))
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)


class account_intrastat_statement_purchase_section3(models.Model):
    _name = 'account.intrastat.statement.purchase.section3'
    _description = 'Account INTRASTAT - Statement - Purchase Section 3'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Float(string='Amount Currency',
                                   digits=dp.get_precision('Account'))
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Date(string='Invoice Date')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Service')
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
    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', readonly=True)


class account_intrastat_statement_purchase_section4(models.Model):
    _name = 'account.intrastat.statement.purchase.section4'
    _description = 'Account INTRASTAT - Statement - Purchase Section 4'
    statement_id = fields.Many2one('account.intrastat.statement', 
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    custom = fields.Many2one('account.intrastat.custom', 'Custom')
    year = fields.Many2one('account.fiscalyear',
                           string='Year Ref of Variation')
    protocol = fields.Integer(string='Protocol number', size=6)
    progressive_to_modify_id = fields.Many2one(
        'account.intrastat.statement.purchase.section1',
        'Progressive to Modify')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Float(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Float(string='Amount Currency',
                                   digits=dp.get_precision('Account'))
    invoice_number = fields.Char(string='Invoice Number')
    invoice_date = fields.Char(string='Invoice Date')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Service')
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
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)
