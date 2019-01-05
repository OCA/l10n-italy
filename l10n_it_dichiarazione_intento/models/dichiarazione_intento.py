# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.exceptions import UserError, ValidationError


class DichiarazioneIntentoYearlyLimit(models.Model):

    _name = 'dichiarazione.intento.yearly.limit'
    _description = 'Yearly limit for dichiarazioni'
    _order = 'company_id, year desc'
    _rec_name = 'year'

    company_id = fields.Many2one('res.company', string='Company')
    year = fields.Char(required=True)
    limit_amount = fields.Float()
    used_amount = fields.Float(compute='_compute_used_amount')

    @api.multi
    def _compute_used_amount(self):
        for record in self:
            dichiarazioni = self.env['dichiarazione.intento'].search([
                ('date_start', '>=', '%s-01-01' % record.year),
                ('date_end', '<=', '%s-12-31' % record.year),
                ('type', '=', 'out'), ])
            record.used_amount = sum([d.limit_amount for d in dichiarazioni])


class DichiarazioneIntento(models.Model):

    _name = 'dichiarazione.intento'
    _description = 'Dichiarazione Intento'
    _order = 'date_start desc,date_end desc'
    _rec_name = 'display_name'

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    display_name = fields.Char(
        compute='_compute_clean_display_name', store=True)
    number = fields.Char(copy=False)
    date = fields.Date(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    type = fields.Selection([('in', 'Suppliers'), ('out', 'Customers')],
                            required=True, default='in')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True)
    partner_document_number = fields.Char(
        required=True, string='Document Number',
        help='Number of partner\'s document')
    partner_document_date = fields.Date(
        required=True, string='Document Date',
        help='Date of partner\'s document')
    taxes_ids = fields.Many2many('account.tax', string='Taxes',
                                 required=True)
    used_amount = fields.Monetary(compute='_compute_amounts', store=True)
    limit_amount = fields.Monetary(required=True)
    available_amount = fields.Monetary(compute='_compute_amounts', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=_default_currency,)
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position', required=True,
        domain=[('valid_for_dichiarazione_intento', '=', True)])
    state = fields.Selection(
        [('valid', 'Valid'), ('close', 'Close')],
        compute='_compute_state', store=True)
    line_ids = fields.One2many('dichiarazione.intento.line',
                               'dichiarazione_id', string='Lines')

    @api.model
    def create(self, values):
        # ----- Check if yearly platfond is enough
        #       to create an in dichiarazione
        if values.get('type', False) == 'in':
            year = datetime.strptime(
                values['date_start'], '%Y-%m-%d').strftime('%Y')
            platfond = self.env.user.company_id.\
                dichiarazione_yearly_limit_ids.filtered(
                    lambda r: r.year == year)
            if not platfond:
                raise UserError(
                    _('Define a yearly platfond for out documents'))
            dichiarazioni = self.search([
                ('date_start', '>=', '%s-01-01' % year),
                ('date_end', '<=', '%s-12-31' % year),
                ('type', '=', 'in'),
                ])
            actual_limit_total = sum([d.limit_amount for d in dichiarazioni]) \
                + values['limit_amount']
            if actual_limit_total > platfond.limit_amount:
                raise UserError(
                    _('Total of documents exceed yearly limit'))
        # ----- Assign a number to dichiarazione
        if values and not values.get('number', ''):
            values['number'] = self.env['ir.sequence'].next_by_code(
                'dichiarazione.intento')
        return super(DichiarazioneIntento, self).create(values)

    @api.multi
    def unlink(self):
        for record in self:
            if record.line_ids:
                raise UserError(
                    _('Impossible to delete a document with linked invoices'))
        return super(DichiarazioneIntento, self).unlink()

    @api.constrains('fiscal_position_id', 'taxes_ids')
    @api.multi
    def _check_taxes_for_dichiarazione_intento(self):
        for dichiarazione in self:
            if dichiarazione.taxes_ids and \
                    dichiarazione.fiscal_position_id and \
                    dichiarazione.fiscal_position_id.tax_ids:
                taxes = [t.tax_dest_id.id
                         for t in dichiarazione.fiscal_position_id.tax_ids]
                for tax in dichiarazione.taxes_ids:
                    if tax.id not in taxes:
                        raise ValidationError(_(
                            'All taxes in dichiarazione intento must be used '
                            'in fiscal position taxes'))

    @api.constrains('limit_amount', 'used_amount', 'line_ids',
                    'line_ids.amount')
    @api.multi
    def _check_available_amount(self):
        for dichiarazione in self:
            if dichiarazione.available_amount < 0:
                raise UserError(_(
                    'Limit passed for dichiarazione %s.\n'
                    'Excess value: %s%s' % (
                        dichiarazione.number,
                        abs(dichiarazione.available_amount),
                        dichiarazione.currency_id.symbol, )))

    @api.multi
    @api.depends('number', 'partner_document_number')
    def _compute_clean_display_name(self):
        for record in self:
            display_name = record.number
            if record.partner_document_number:
                display_name = '%s (%s)' % (
                    display_name, record.partner_document_number)
            record.display_name = display_name

    @api.multi
    @api.depends('line_ids', 'line_ids.amount')
    def _compute_amounts(self):
        for record in self:
            amount = sum(line.amount for line in record.line_ids)
            # ----- Force value to 0
            if amount < 0.0:
                amount = 0.0
            record.used_amount = amount
            record.available_amount = record.limit_amount - record.used_amount

    @api.multi
    @api.depends('used_amount', 'limit_amount', 'date_end')
    def _compute_state(self):
        for record in self:
            # ----- If used amount is bigger than limit, close document
            if record.limit_amount and \
                    record.used_amount >= record.limit_amount:
                state = 'close'
            # ----- If date is passed, close document
            elif record.date_end and \
                    record.date_end < datetime.today().strftime(DATE_FORMAT):
                state = 'close'
            else:
                state = 'valid'
            record.state = state

    def get_valid(self, type=None, partner_id=False, date=False):
        if not partner_id or not type or not date:
            return False
        # ----- return valid documents for partner
        domain = [('partner_id', '=', partner_id), ('type', '=', type),
                  ('date_start', '<=', date), ('date_end', '>=', date)]
        ignore_state = self.env.context.get('ignore_state', False)
        if not ignore_state:
            domain.append(('state', '!=', 'close'), )
        records = self.search(domain, order='state desc, date desc')
        return records


class DichiarazioneIntentoLine(models.Model):

    _name = 'dichiarazione.intento.line'

    dichiarazione_id = fields.Many2one('dichiarazione.intento',
                                       string='Dichiarazione')
    taxes_ids = fields.Many2many('account.tax', string='Taxes')
    move_line_ids = fields.Many2many('account.move.line', string='Move Lines',
                                     ondelete='cascade')
    amount = fields.Monetary()
    base_amount = fields.Monetary(string='Base Amount')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    currency_id = fields.Many2one('res.currency', string='Currency')
