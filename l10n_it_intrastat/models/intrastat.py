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

    @api.one
    def _default_company(self):
        company_id = self._context.get('company_id',
                                       self.env.user.company_id.id)
        return company_id

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

    name = fields.Char(string='Name', required=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default="_default_company")
    vat_taxpayer = fields.Char(string='Vat taxpayer', required=True)
    fiscalyear_id = fields.Many2one('account.fiscalyear',
                                    string='Year')
    period_type = fields.Selection([
        ('M', 'Month'),
        ('T', 'Quarterly'),
        ], 'Payment Type', required=True)
    period_number = fields.Char(
        string='Period',
        help="Values accepted:\
        - Month : From 1 to 12 \
        - Quarterly: From 1 to 4", required=True)
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


class account_intrastat_statement_sale_section1(models.Model):
    _name = 'account.intrastat.statement.sale.section1'
    _description = 'Account INTRASTAT - Statement - Sale Section 1'
    
    statement_id = fields.Many2one(
        'account.intrastat.statement', string='Statement', 
        required=True, readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    country_customer_id = fields.Many2one('res.country',
                                          string='Country Customer')
    vat_code = fields.Integer(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
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
    country_destination_id = fields.Many2one('res.country', 
                                             string='Country Destination')
    province_origin_id = fields.Many2one('res.country.state', 
                                         string='Province Origin')
    invoice_id = fields.Many2one('account.invoice',
                                 string='Invoice', readonly=True)


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
    country_customer_id = fields.Many2one('res.country', 
                                          string='Country Customer')
    vat_code = fields.Integer(string='Vat Code Customer')
    sign_variation = fields.Selection([
        ('+', '+'),
        ('-', '-'),
        ], 'Sign Variation')
    amount_euro = fields.Float(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    transation_nature = fields.Many2one('account.intrastat.transation.nature', 
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
    country_customer_id = fields.Many2one('res.country', 
                                          string='Country Customer')
    vat_code = fields.Integer(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
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
    country_customer_id = fields.Many2one('res.country', 
                                          string='Country Customer')
    vat_code = fields.Integer(string='Vat Code Customer')
    amount_euro = fields.Float(string='Amount Euro', 
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


class account_intrastat_statement_purchase_section1(models.Model):
    _name = 'account.intrastat.statement.purchase.section1'
    _description = 'Account INTRASTAT - Statement - Purchase Section 1'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement', required=True,
                                   readonly=True)
    progressive = fields.Integer(string='Progressive', required=True)
    country_supplier_id = fields.Many2one('res.country',
                                          string='Country Supplier')
    vat_code = fields.Integer(string='Vat Code Purchase')
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
    country_supplier_id = fields.Many2one('res.country', 
                                          string='Country Supplier')
    vat_code = fields.Integer(string='Vat Code Customer')
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
    country_supplier_id = fields.Many2one('res.country',
                                          string='Country Supplier')
    vat_code = fields.Integer(string='Vat Code Supplier')
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
    country_supplier_id = fields.Many2one('res.country',
                                          string='Country Supplier')
    vat_code = fields.Integer(string='Vat Code Supplier')
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
