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
            vat = self.company_id.partner_id.vat \
                and self.company_id.partner_id.vat[2:] or False
            return vat
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
            return st.number+1
        else:
            return 1
        
    @api.model
    def _get_sequence(self):
        return self.env['ir.sequence'].get('intrastat.statement.sequence')
            
    number = fields.Integer(
        string='Number', readonly=True, default=_compute_progressive)
    date = fields.Date(
        string='Submission Date', default=fields.Date.today(), required=True)
    company_id = fields.Many2one(
        'res.company', string='Company', default=_default_company, 
        required=True)
    vat_taxpayer = fields.Char(
        string='Vat taxpayer', required=True, default=_default_company_vat)
    vat_delegate = fields.Char(string='Vat delegate')
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
    custom_id = fields.Many2one(
        'account.intrastat.custom', string='Custom', required=True)
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
    
    sale_statement_sequence = fields.Integer(
        string='Statement Sequence', readonly=True, 
        default=_get_sequence)
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

    purchase_statement_sequence = fields.Integer(
        string='Statement Sequence', readonly=True, 
        default=_get_sequence)
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
    
    @api.model
    def _get_progressive_interchange(self):
        prg = 0
        domain = [('date', '=', self.date)]
        for st in self.search(domain):
            prg += 1
            if st.id == self.id:
                break
        return prg
        
    @api.model
    def _get_file_name(self):
        '''
        Format UA code + %m + %d
        '''
        # Calcolo progressivo interchange
        prg = self._get_progressive_interchange()
        file_name = ''
        date_obj = datetime.strptime(self.date, '%Y-%m-%d')
        file_name = '%s%s%s.%s%s' % (self.company_id.intrastat_ua_code,
                                '{:2s}'.format(str(date_obj.month).zfill(2)),
                                '{:2s}'.format(str(date_obj.day).zfill(2)),
                                'I', # doc intrastat
                                '{:2s}'.format(str(prg).zfill(2))
                                )
        return file_name
    
    @api.model
    def _prepare_export_head(self):
        rcd = ''
        # Codice utente abilitato (mittente)
        rcd += '{:4s}'.format(self.company_id.intrastat_ua_code)
        # Riservato a SDA
        rcd += '{:12s}'.format("")
        # Nome del flusso
        rcd += '{:12s}'.format(self._get_file_name())
        # Riservato a SDA
        rcd += '{:12s}'.format("")
        # Codice sezione doganale presso la quale si effettua l'operazione
        rcd += '{:6s}'.format(self.custom_id.code or '')
        # Riservato a SDA
        rcd += '{:4s}'.format("")
        # Codice fiscale o numero partita IVA o codice spedizioniere del 
        #     richiedente (utente autorizzato)
        rcd += '{:16s}'.format(self.vat_taxpayer)
        #Progressivo sede utente autorizzato
        prg = self._get_progressive_interchange()
        rcd += '{:3s}'.format(str(prg).zfill(3))
        # Riservato a SDA
        rcd += '{:1s}'.format("")
        # Numero di record presenti nel flusso
        tot_lines = self.sale_section1_operation_number +\
                    self.sale_section2_operation_number +\
                    self.sale_section3_operation_number +\
                    self.sale_section4_operation_number +\
                    self.purchase_section1_operation_number +\
                    self.purchase_section2_operation_number +\
                    self.purchase_section3_operation_number +\
                    self.purchase_section4_operation_number +\
                    1 # this rec
        # ... Add frontispiece sale
        if self.sale_section1_operation_number\
            or self.sale_section2_operation_number\
            or self.sale_section3_operation_number\
            or self.sale_section4_operation_number:
            tot_lines += 1
        # ... Add frontispiece purchase
        if self.purchase_section1_operation_number\
            or self.purchase_section2_operation_number\
            or self.purchase_section3_operation_number\
            or self.purchase_section4_operation_number:
            tot_lines += 1
        rcd += '{:5s}'.format(str(tot_lines).zfill(5))
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    
    @api.model
    def _prepare_export_prefix(self, type='sale'):
        '''
        Type: C=Sale A=Purchase
        '''
        prefix = '' 
        # Campo fisso: “EUROX”
        prefix += 'EUROX' 
        # Partita IVA del presentatore
        prefix += '{:11s}'.format(self.vat_taxpayer)
        # Numero progressivo dell’elenco
        if type == 'sale':
            prefix += '{:6s}'.format(\
                str(self.sale_statement_sequence).zfill(6))
        else:
            prefix += '{:6s}'.format(\
                str(self.purchase_statement_sequence).zfill(6))
        return prefix
    
    @api.model
    def _prepare_export_frontispiece(self, type):
        rcd = self._prepare_export_prefix(type)
        rcd += '{:1s}'.format("0")
        rcd += '{:5s}'.format("".zfill(5))
        # Tipo riepilogo: A = acquisti C = cessioni
        if type == 'purchase':
            rcd += '{:1s}'.format("A")
        else:
            rcd += '{:1s}'.format("C")
        # Anno
        date_start_year = datetime.strptime(self.fiscalyear_id.date_start, 
                                            '%Y-%m-%d')
        rcd += '{:2s}'.format(str(date_start_year.year)[2:])
        # Periodicità
        rcd += '{:1s}'.format(self.period_type)
        # Periodo
        rcd += '{:2s}'.format(str(self.period_number).zfill(2))
        # Partita IVA del contribuentè
        rcd += '{:11s}'.format(self.vat_taxpayer)
        # Contenuto degli elenchì
        rcd += '{:1s}'.format(self.content_type)
        # Casi particolari riferiti al soggetto obbligatò
        rcd += '{:1s}'.format(self.special_cases)
        # Partita IVA del soggetto delegato
        rcd += '{:11s}'.format(self.vat_delegate or "".zfill(11))
        # Numero e importo dettagli della sezione 1
        if type == "purchase":
            rcd += '{:5s}'.format(
                str(self.purchase_section1_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.purchase_section1_operation_amount).zfill(13))
        else:
            rcd += '{:5s}'.format(
                str(self.sale_section1_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.sale_section1_operation_amount).zfill(13))
        # Numero dettagli della sezione 2
        if type == "purchase":
            rcd += '{:5s}'.format(
                str(self.purchase_section2_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.purchase_section2_operation_amount).zfill(13))
        else:
            rcd += '{:5s}'.format(
                str(self.sale_section2_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.sale_section2_operation_amount).zfill(13))    
        # Numero dettagli della sezione 3
        if type == "purchase":
            rcd += '{:5s}'.format(
                str(self.purchase_section3_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.purchase_section3_operation_amount).zfill(13))
        else:
            rcd += '{:5s}'.format(
                str(self.sale_section3_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.sale_section3_operation_amount).zfill(13))
        # Numero dettagli della sezione 4
        if type == "purchase":
            rcd += '{:5s}'.format(
                str(self.purchase_section4_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.purchase_section4_operation_amount).zfill(13))
        else:
            rcd += '{:5s}'.format(
                str(self.sale_section4_operation_number).zfill(5))
            rcd += '{:13s}'.format(
                str(self.sale_section4_operation_amount).zfill(13))
        # ... new line
        rcd += "\r"
        rcd += "\n" 
        return rcd
        
    @api.model
    def generate_file_export(self):
        file_content = ''
        rec_head = self._prepare_export_head()
        file_content += rec_head
        # Purchase
        if self.purchase_section1_operation_number \
            or self.purchase_section2_operation_number \
            or self.purchase_section3_operation_number \
            or self.purchase_section4_operation_number:
            # frontispiece
            rec_frontispiece = self._prepare_export_frontispiece("purchase")
            file_content += rec_frontispiece
            # Section 1
            for line in self.purchase_section1_ids:
                rcd = self._prepare_export_prefix("purchase")
                rcd += '{:1s}'.format("1")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 2
            for line in self.purchase_section2_ids:
                rcd = self._prepare_export_prefix("purchase")
                rcd += '{:1s}'.format("2")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 3
            for line in self.purchase_section3_ids:
                rcd = self._prepare_export_prefix("purchase")
                rcd += '{:1s}'.format("3")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 4
            for line in self.purchase_section4_ids:
                rcd = self._prepare_export_prefix("purchase")
                rcd += '{:1s}'.format("4")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            
        # Sale
        if self.sale_section1_operation_number \
            or self.sale_section2_operation_number \
            or self.sale_section3_operation_number \
            or self.sale_section4_operation_number:
            # frontispiece
            rec_frontispiece = self._prepare_export_frontispiece("sale")
            file_content += rec_frontispiece
            # Section 1
            for line in self.sale_section1_ids:
                rcd = self._prepare_export_prefix("sale")
                rcd += '{:1s}'.format("1")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 2
            for line in self.sale_section2_ids:
                rcd = self._prepare_export_prefix("sale")
                rcd += '{:1s}'.format("2")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 3
            for line in self.sale_section3_ids:
                rcd = self._prepare_export_prefix("sale")
                rcd += '{:1s}'.format("3")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
            # Section 4
            for line in self.sale_section4_ids:
                rcd = self._prepare_export_prefix("sale")
                rcd += '{:1s}'.format("4")
                rcd += '{:5s}'.format(str(line.progressive).zfill(5))
                rcd += line._prepare_export_line()
                file_content += rcd
        
        return file_content
    
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
                # Sale - Section 2
                elif inv_intra_line.statement_section == 'sale_s2':
                    st_line = \
                        self.env['account.intrastat.statement.sale.section2']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_sale_s2):
                            st_line['progressive'] = \
                                len(statement_lines_sale_s2) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_sale_s2.append((0, 0, st_line))
                # Sale - Section 3
                elif inv_intra_line.statement_section == 'sale_s3':
                    st_line = \
                        self.env['account.intrastat.statement.sale.section3']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_sale_s3):
                            st_line['progressive'] = \
                                len(statement_lines_sale_s3) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_sale_s3.append((0, 0, st_line))
                # Sale - Section 4
                elif inv_intra_line.statement_section == 'sale_s4':
                    st_line = \
                        self.env['account.intrastat.statement.sale.section4']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_sale_s4):
                            st_line['progressive'] = \
                                len(statement_lines_sale_s4) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_sale_s4.append((0, 0, st_line))
                # Purchase - Section 1
                elif inv_intra_line.statement_section == 'purchase_s1':
                    st_line = \
                        self.env[
                            'account.intrastat.statement.purchase.section1']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_purchase_s1):
                            st_line['progressive'] = \
                                len(statement_lines_purchase_s1) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_purchase_s1.append((0, 0, st_line))
                # Purchase - Section 2
                elif inv_intra_line.statement_section == 'purchase_s2':
                    st_line = \
                        self.env[
                            'account.intrastat.statement.purchase.section2']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_purchase_s2):
                            st_line['progressive'] = \
                                len(statement_lines_purchase_s2) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_purchase_s2.append((0, 0, st_line))
                # Purchase - Section 3
                elif inv_intra_line.statement_section == 'purchase_s3':
                    st_line = \
                        self.env[
                            'account.intrastat.statement.purchase.section3']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_purchase_s3):
                            st_line['progressive'] = \
                                len(statement_lines_purchase_s3) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_purchase_s3.append((0, 0, st_line))
                # Purchase - Section 4
                elif inv_intra_line.statement_section == 'purchase_s4':
                    st_line = \
                        self.env[
                            'account.intrastat.statement.purchase.section4']\
                        ._prepare_statement_line(inv_intra_line)
                    if st_line:
                        if len(statement_lines_purchase_s4):
                            st_line['progressive'] = \
                                len(statement_lines_purchase_s4) +1
                        else:
                            st_line['progressive'] = 1 
                        statement_lines_purchase_s4.append((0, 0, st_line))
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
        self.vat_taxpayer = self.company_id.partner_id.vat \
            and self.company_id.partner_id.vat[2:] or False
    
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
        readonly=True, ondelete="cascade")
    progressive = fields.Integer(string='Progressive')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Customer')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Integer(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Good')
    weight_kg = fields.Integer(string='Weight kg')
    additional_units = fields.Integer(string='Additional Units')
    statistic_amount_euro = fields.Integer(string='Statistic Amount Euro', 
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
    @api.onchange('weight_kg')
    def change_weight_kg(self):
        self.additional_units = self.weight_kg 
        
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code': 
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'transation_nature_id': inv_intra_line.transation_nature_id.id \
                or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'weight_kg': round(inv_intra_line.weight_kg) or 0,
            'additional_units': 
                inv_intra_line.additional_units and \
                round(inv_intra_line.additional_units) or 0,
            'statistic_amount_euro': 
                round(inv_intra_line.statistic_amount_euro) or 0,
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
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice dello Stato membro dell’acquirente
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA dell’acquirente
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Codice della natura della transazione
        rcd += '{:1s}'.format(
            self.transation_nature_id and self.transation_nature_id.code or '')
        # Codice della nomenclatura combinata della merce
        rcd += '{:8s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Massa netta in chilogrammi
        rcd += '{:10s}'.format(str(self.weight_kg).zfill(10))
        # Quantità espressa nell'unità di misura supplementare
        rcd += '{:10s}'.format(str(self.additional_units).zfill(10))
        # Valore statistico in euro
        rcd += '{:13s}'.format(str(self.statistic_amount_euro).zfill(13))
        # Codice delle condizioni di consegna
        rcd += '{:1s}'.format(
            self.delivery_code_id and self.delivery_code_id.code[:1] or '')
        # Codice del modo di trasporto
        rcd += '{:1s}'.format(
            self.transport_code_id and str(self.transport_code_id.code) or '')
        # Codice del paese di destinazione
        rcd += '{:2s}'.format(
            self.country_destination_id and self.country_destination_id.code \
            or '')
        # Codice del paese di origine della merce
        rcd += '{:2s}'.format(
            self.province_origin_id and self.province_origin_id.code or '')
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    

class account_intrastat_statement_sale_section2(models.Model):
    _name = 'account.intrastat.statement.sale.section2'
    _description = 'Account INTRASTAT - Statement - Sale Section 2'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive', readonly=True)
    
    month = fields.Integer(string='Month Ref of Refund')
    quarterly = fields.Integer(string='Quarterly Ref of Refund')
    year_id = fields.Many2one('account.fiscalyear', string='Year Ref of Refund')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    sign_variation = fields.Selection([
        ('+', '+'),
        ('-', '-'),
        ], 'Sign Variation')
    amount_euro = fields.Integer(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_code_id = fields.Many2one('report.intrastat.code', 
                                        string='Intrastat Code Good')
    statistic_amount_euro = fields.Integer(string='Statistic Amount Euro', 
                                         digits=dp.get_precision('Account'))
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'transation_nature_id': inv_intra_line.transation_nature_id.id \
                or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'statistic_amount_euro': 
                round(inv_intra_line.statistic_amount_euro) or 0,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Mese di riferimento del riepilogo da rettificare
        rcd += '{:2s}'.format(str(self.month).zfill(2))
        # Trimestre di riferimento del riepilogo da rettificare
        rcd += '{:1s}'.format(str(self.quarterly).zfill(1))
        # Anno periodo di ref da modificare
        date_start_year = datetime.strptime(self.year_id.date_start, 
                                            '%Y-%m-%d')
        rcd += '{:2s}'.format(
            date_start_year and str(date_start_year.year)[2:] or '')
        # Codice dello Stato membro dell’acquirente
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA dell’acquirente
        rcd += '{:12s}'.format(self.vat_code or '')
        # Segno da attribuire alle variazioni da X(1) apportare
        rcd += '{:1s}'.format(self.sign_variation or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Codice della natura della transazione
        rcd += '{:1s}'.format(
            self.transation_nature_id and self.transation_nature_id.code or '')
        # Codice della nomenclatura combinata della merce
        rcd += '{:8s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Valore statistico in euro
        rcd += '{:13s}'.format(str(self.statistic_amount_euro).zfill(13))
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd


class account_intrastat_statement_sale_section3(models.Model):
    _name = 'account.intrastat.statement.sale.section3'
    _description = 'Account INTRASTAT - Statement - Sale Section 3'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Integer(string='Amount Euro', 
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
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'invoice_number': inv_intra_line.invoice_number or False,
            'invoice_date': inv_intra_line.invoice_date or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'supply_method': inv_intra_line.supply_method or False,
            'payment_method': inv_intra_line.payment_method or False,
            'country_payment_id': inv_intra_line.country_payment_id.id or False,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice dello Stato membro dell’acquirente
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA del fornitore
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Numero Fattura
        rcd += '{:15s}'.format(str(self.invoice_number).zfill(15))
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
            invoice_date_ddmmyy = date_obj.strftime('%d%m%y') 
        rcd += '{:2s}'.format(invoice_date_ddmmyy or '')
        # Codice del servizio
        rcd += '{:6s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Modalità di erogazione
        rcd += '{:1s}'.format(self.supply_method or '')
        # Modalità di incasso
        rcd += '{:1s}'.format(self.payment_method or '')
        # Codice del paese di pagamento
        rcd += '{:2s}'.format(self.country_payment_id and \
                              self.country_payment_id.code or '')
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd


class account_intrastat_statement_sale_section4(models.Model):
    _name = 'account.intrastat.statement.sale.section4'
    _description = 'Account INTRASTAT - Statement - Sale Section 4'
    
    statement_id = fields.Many2one(
        'account.intrastat.statement', string='Statement', 
        readonly=True, ondelete="cascade")
    progressive = fields.Integer(
        string='Progressive', readonly=True)
    custom_id = fields.Many2one('account.intrastat.custom', 'Custom')
    year_id = fields.Many2one('account.fiscalyear', 
                           string='Year Ref of Variation')
    protocol = fields.Integer(string='Protocol number', size=6)
    progressive_to_modify_id =  fields.Many2one(
        'account.intrastat.statement.sale.section1', 'Progressive to Modify')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Customer')
    amount_euro = fields.Integer(string='Amount Euro', 
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
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'invoice_number': inv_intra_line.invoice_number or False,
            'invoice_date': inv_intra_line.invoice_date or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'supply_method': inv_intra_line.supply_method or False,
            'payment_method': inv_intra_line.payment_method or False,
            'country_payment_id': inv_intra_line.country_payment_id.id or False,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice della sezione doganale in cui è stato registrata la 
        # dichiarazione da rettificare
        rcd += '{:6s}'.format(self.custom_id and self.custom_id.code or '')
        # Anno di registrazione della dichiarazione da rettificare
        date_start_year = datetime.strptime(self.year_id.date_start, 
                                            '%Y-%m-%d')
        rcd += '{:2s}'.format(
            date_start_year and str(date_start_year.year)[2:] or '')
        # Protocollo della dichiarazione da rettificare
        rcd += '{:6s}'.format(self.protocol and str(self.protocol).zfill(6) \
                or '')
        # Progressivo della sezione 3 da rettificare
        rcd += '{:5s}'.format(self.progressive_to_modify_id and 
                str(self.progressive_to_modify_id.progressive).zfill(5) \
                or '')
        # Codice dello Stato membro dell’acquirente
        rcd += '{:2s}'.format(
            self.country_partner_id.code or self.partner_id.country_id \
            and self.partner_id.country_id.code 
            or '')
        # Codice IVA dell’acquirente
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Numero Fattura
        rcd += '{:15s}'.format(str(self.invoice_number).zfill(15))
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
            invoice_date_ddmmyy = date_obj.strftime('%d%m%y') 
        rcd += '{:2s}'.format(invoice_date_ddmmyy or '')
        # Codice del servizio
        rcd += '{:6s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Modalità di erogazione
        rcd += '{:1s}'.format(self.supply_method or '')
        # Modalità di incasso
        rcd += '{:1s}'.format(self.payment_method or '')
        # Codice del paese di pagamento
        rcd += '{:2s}'.format(self.country_payment_id and \
                              self.country_payment_id.code or '')
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd

class account_intrastat_statement_purchase_section1(models.Model):
    _name = 'account.intrastat.statement.purchase.section1'
    _description = 'Account INTRASTAT - Statement - Purchase Section 1'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Integer(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Integer(string='Amount Currency', 
                                   digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_code_id = fields.Many2one(
        'report.intrastat.code', string='Intrastat Code Good')
    weight_kg = fields.Integer(string='Weight kg')
    additional_units = fields.Integer(string='Additional Units')
    statistic_amount_euro = fields.Integer(string='Statistic Amount Euro', 
                                         digits=dp.get_precision('Account'))
    delivery_code_id = fields.Many2one('stock.incoterms', 
                                    string='Delivery')
    transport_code_id = fields.Many2one('account.intrastat.transport', 
                                     string='Transport')
    country_origin_id = fields.Many2one('res.country', 
                                        string='Country Origin')
    country_good_origin_id = fields.Many2one('res.country', 
                                             string='Country Good Origin')
    province_destination_id = fields.Many2one('res.country.state', 
                                              string='Province Destination')
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)
    @api.onchange('weight_kg')
    def change_weight_kg(self):
        self.additional_units = self.weight_kg 
            
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'amount_currency': round(inv_intra_line.amount_currency) or 0,
            'transation_nature_id': inv_intra_line.transation_nature_id.id \
                or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'weight_kg': 
                inv_intra_line.weight_kg and round(inv_intra_line.weight_kg) 
                or 0,
            'additional_units': 
                inv_intra_line.additional_units and \
                round(inv_intra_line.additional_units) or 0,
            'statistic_amount_euro': 
                round(inv_intra_line.statistic_amount_euro) or 0,
            'delivery_code_id': inv_intra_line.delivery_code_id and \
                inv_intra_line.delivery_code_id.id or False,
            'transport_code_id': inv_intra_line.transport_code_id and \
                inv_intra_line.transport_code_id.id or False,
            'country_origin_id': inv_intra_line.country_origin_id and \
                inv_intra_line.country_origin_id.id or False,
            'country_good_origin_id': inv_intra_line.country_good_origin_id \
                and inv_intra_line.country_good_origin_id.id or False,
            'province_destination_id': inv_intra_line.province_destination_id \
                and inv_intra_line.province_destination_id.id or False
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice dello Stato membro del fornitore
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA del fornitore
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Ammontare delle operazioni in valuta
        rcd += '{:13s}'.format(str(self.amount_currency).zfill(13))
        # Codice della natura della transazione
        rcd += '{:1s}'.format(
            self.transation_nature_id and self.transation_nature_id.code or '')
        # Codice della nomenclatura combinata della merce
        rcd += '{:8s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Massa netta in chilogrammi
        rcd += '{:10s}'.format(str(self.weight_kg).zfill(10))
        # Quantità espressa nell'unità di misura supplementare
        rcd += '{:10s}'.format(str(self.additional_units).zfill(10))
        # Valore statistico in euro
        rcd += '{:13s}'.format(str(self.statistic_amount_euro).zfill(13))
        # Codice delle condizioni di consegna
        rcd += '{:1s}'.format(
            self.delivery_code_id and self.delivery_code_id.code[:1] or '')
        # Codice del modo di trasporto
        rcd += '{:1s}'.format(
            self.transport_code_id and str(self.transport_code_id.code) or '')
        # Codice del paese di provenienza
        rcd += '{:2s}'.format(
            self.country_origin_id and self.country_origin_id.code or '')
        # Codice del paese di origine della merce
        rcd += '{:2s}'.format(
            self.country_good_origin_id and self.country_good_origin_id.code \
            or '')
        # Codice della provincia di destinazione della merce
        rcd += '{:2s}'.format(
            self.province_destination_id and self.province_destination_id.code \
            or '')
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd

class account_intrastat_statement_purchase_section2(models.Model):
    _name = 'account.intrastat.statement.purchase.section2'
    _description = 'Account INTRASTAT - Statement - Purchase Section 2'
    
    statement_id = fields.Many2one('account.intrastat.statement', 
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive')
    month = fields.Integer(string='Month Ref of Refund')
    quarterly = fields.Integer(string='Quarterly Ref of Refund')
    year_id = fields.Many2one('account.fiscalyear', string='Year Ref of Refund')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    sign_variation = fields.Selection([
        ('+', '+'),
        ('-', '-'),
        ], 'Sign Variation')
    amount_euro = fields.Integer(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Integer(string='Amount Currency',
                                   digits=dp.get_precision('Account'))
    transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_code_id = fields.Many2one(
        'report.intrastat.code', string='Intrastat Code Good')
    statistic_amount_euro = fields.Integer(string='Statistic Amount Euro',
                                         digits=dp.get_precision('Account'))
    invoice_id = fields.Many2one('account.invoice', string='Invoice',
                                 readonly=True)
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'amount_currency': round(inv_intra_line.amount_currency) or 0,
            'transation_nature_id': inv_intra_line.transation_nature_id.id \
                or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'statistic_amount_euro': inv_intra_line.statistic_amount_euro or 0,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Mese di riferimento del riepilogo da rettificare
        rcd += '{:2s}'.format(str(self.month).zfill(2))
        # Trimestre di riferimento del riepilogo da rettificare
        rcd += '{:1s}'.format(str(self.quarterly).zfill(1))
        # Anno periodo di ref da modificare
        date_start_year = datetime.strptime(self.year_id.date_start, 
                                            '%Y-%m-%d')
        rcd += '{:2s}'.format(
            date_start_year and str(date_start_year.year)[2:] or '')
        # Codice dello Stato membro del fornitore
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA del fornitore
        rcd += '{:12s}'.format(self.vat_code or '')
        # Segno da attribuire alle variazioni da X(1) apportare
        rcd += '{:1s}'.format(self.sign_variation or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Ammontare delle operazioni in valuta
        rcd += '{:13s}'.format(str(self.amount_currency).zfill(13))
        # Codice della natura della transazione
        rcd += '{:1s}'.format(
            self.transation_nature_id and self.transation_nature_id.code or '')
        # Codice della nomenclatura combinata della merce
        rcd += '{:8s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Valore statistico in euro
        rcd += '{:13s}'.format(str(self.statistic_amount_euro).zfill(13))
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd

class account_intrastat_statement_purchase_section3(models.Model):
    _name = 'account.intrastat.statement.purchase.section3'
    _description = 'Account INTRASTAT - Statement - Purchase Section 3'
    
    statement_id = fields.Many2one('account.intrastat.statement',
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive',)
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Integer(string='Amount Euro', 
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Integer(string='Amount Currency',
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
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'amount_currency': round(inv_intra_line.amount_currency) or 0,
            'invoice_number': inv_intra_line.invoice_number or False,
            'invoice_date': inv_intra_line.invoice_date or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'supply_method': inv_intra_line.supply_method or False,
            'payment_method': inv_intra_line.payment_method or False,
            'country_payment_id': inv_intra_line.country_payment_id.id or False,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice dello Stato membro del fornitore
        rcd += '{:2s}'.format(self.country_partner_id.code or '')
        # Codice IVA del fornitore
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Ammontare delle operazioni in valuta
        rcd += '{:13s}'.format(str(self.amount_currency).zfill(13))
        # Numero Fattura
        rcd += '{:15s}'.format(str(self.invoice_number).zfill(15))
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
            invoice_date_ddmmyy = date_obj.strftime('%d%m%y') 
        rcd += '{:2s}'.format(invoice_date_ddmmyy or '')
        # Codice del servizio
        rcd += '{:6s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Modalità di erogazione
        rcd += '{:1s}'.format(self.supply_method or '')
        # Modalità di incasso
        rcd += '{:1s}'.format(self.payment_method or '')
        # Codice del paese di pagamento
        rcd += '{:2s}'.format(self.country_payment_id and \
                              self.country_payment_id.code or '')
        # ... new line
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd


class account_intrastat_statement_purchase_section4(models.Model):
    _name = 'account.intrastat.statement.purchase.section4'
    _description = 'Account INTRASTAT - Statement - Purchase Section 4'
    statement_id = fields.Many2one('account.intrastat.statement', 
                                   string='Statement',
                                   readonly=True,
                                   ondelete="cascade")
    progressive = fields.Integer(string='Progressive')
    custom_id = fields.Many2one('account.intrastat.custom', 'Custom')
    year_id = fields.Many2one('account.fiscalyear',
                           string='Year Ref of Variation')
    protocol = fields.Integer(string='Protocol number', size=6)
    progressive_to_modify_id = fields.Many2one(
        'account.intrastat.statement.purchase.section1',
        'Progressive to Modify')
    partner_id = fields.Many2one('res.partner', string='Partner')
    country_partner_id = fields.Many2one('res.country',
                                          string='Country Partner')
    vat_code = fields.Char(string='Vat Code Partner')
    amount_euro = fields.Integer(string='Amount Euro',
                               digits=dp.get_precision('Account'))
    amount_currency = fields.Integer(string='Amount Currency',
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
    
    @api.model
    def _prepare_statement_line(self, inv_intra_line):
        res = {
            'invoice_id' : inv_intra_line.invoice_id.id or False,
            'partner_id' : inv_intra_line.invoice_id.partner_id.id or False,
            'country_partner_id': inv_intra_line.country_partner_id.id or False,
            'vat_code':
                inv_intra_line.invoice_id.partner_id.vat \
                and inv_intra_line.invoice_id.partner_id.vat[2:] \
                or False,
            'amount_euro': round(inv_intra_line.amount_euro) or 0,
            'amount_currency': round(inv_intra_line.amount_currency) or 0,
            'invoice_number': inv_intra_line.invoice_number or False,
            'invoice_date': inv_intra_line.invoice_date or False,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id or False,
            'supply_method': inv_intra_line.supply_method or False,
            'payment_method': inv_intra_line.payment_method or False,
            'country_payment_id': inv_intra_line.country_payment_id.id or False,
        }
        return res
    
    @api.model
    def _prepare_export_line(self):
        rcd = ''
        # Codice della sezione doganale in cui è stato registrata la 
        # dichiarazione da rettificare
        rcd += '{:6s}'.format(self.custom_id and self.custom_id.code or '')
        # Anno di registrazione della dichiarazione da rettificare
        date_start_year = datetime.strptime(self.year_id.date_start, 
                                            '%Y-%m-%d')
        rcd += '{:2s}'.format(
            date_start_year and str(date_start_year.year)[2:] or '')
        # Protocollo della dichiarazione da rettificare
        rcd += '{:6s}'.format(self.protocol and str(self.protocol).zfill(6) \
                or '')
        # Progressivo della sezione 3 da rettificare
        rcd += '{:5s}'.format(self.progressive_to_modify_id and 
                str(self.progressive_to_modify_id.progressive).zfill(5) \
                or '')
        # Codice dello Stato membro dell’acquirente
        rcd += '{:2s}'.format(
            self.country_partner_id.code or self.partner_id.country_id \
            and self.partner_id.country_id.code 
            or '')
        # Codice IVA dell’acquirente
        rcd += '{:12s}'.format(self.vat_code or '')
        # Ammontare delle operazioni in euro
        rcd += '{:13s}'.format(str(self.amount_euro).zfill(13))
        # Ammontare delle operazioni in valuta
        rcd += '{:13s}'.format(str(self.amount_currency).zfill(13))
        # Numero Fattura
        rcd += '{:15s}'.format(str(self.invoice_number).zfill(15))
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            date_obj = datetime.strptime(invoice_date, '%Y-%m-%d')
            invoice_date_ddmmyy = date_obj.strftime('%d%m%y') 
        rcd += '{:2s}'.format(invoice_date_ddmmyy or '')
        # Codice del servizio
        rcd += '{:6s}'.format(
            self.intrastat_code_id and self.intrastat_code_id.name or '')
        # Modalità di erogazione
        rcd += '{:1s}'.format(self.supply_method or '')
        # Modalità di incasso
        rcd += '{:1s}'.format(self.payment_method or '')
        # Codice del paese di pagamento
        rcd += '{:2s}'.format(self.country_payment_id and \
                              self.country_payment_id.code or '')
        # ... new line
        rcd += "\r" 
        rcd += "\n"  
        
        return rcd