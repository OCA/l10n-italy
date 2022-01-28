# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
import datetime as dt
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class DichiarazioneIntentoYearlyLimit(models.Model):

    _name = 'dichiarazione.intento.yearly.limit'
    _description = 'Yearly limit for declarations'
    _order = 'company_id, year desc'
    _rec_name = 'year'

    company_id = fields.Many2one('res.company', string='Company')
    year = fields.Char(required=True)
    limit_amount = fields.Float(
        string='Plafond'
    )
    # TODO align terms: used_amount > issued_declarations
    used_amount = fields.Float(
        string='Issued Declarations',
        compute='_compute_used_amount'
    )
    actual_used_amount = fields.Float(
        string='Actual Used Amount',
        compute='_compute_used_amount'
    )

    @api.multi
    def _compute_used_amount(self):
        for record in self:
            date_start = datetime.strptime(
                '01-01-{}'.format(record.year), '%d-%m-%Y')
            date_end = datetime.strptime(
                '31-12-{}'.format(record.year), '%d-%m-%Y')
            dichiarazioni = self.env['dichiarazione.intento'].search([
                ('date_start', '>=', date_start),
                ('date_end', '<=', date_end),
                ('type', '=', 'in'), ])
            record.used_amount = sum([d.limit_amount for d in dichiarazioni])
            record.actual_used_amount = sum([d.used_amount for d in dichiarazioni])


class DichiarazioneIntento(models.Model):

    _name = 'dichiarazione.intento'
    _description = 'Declaration of intent'
    _order = 'date_start desc,date_end desc'

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    number = fields.Char(copy=False)
    date = fields.Date(required=True)
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    type = fields.Selection(
        [('in', 'Issued from company'), ('out', 'Received from customers')],
        required=True, default='in')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True)
    telematic_protocol = fields.Char(required=True)
    partner_document_number = fields.Char(
        string='Document Number',
        help='Number of partner\'s document')
    partner_document_date = fields.Date(
        string='Document Date',
        help='Date of partner\'s document')
    taxes_ids = fields.Many2many('account.tax', string='Taxes',
                                 required=True)
    used_amount = fields.Monetary(compute='_compute_amounts', store=True)
    limit_amount = fields.Monetary(required=True)
    available_amount = fields.Monetary(compute='_compute_amounts', store=True)
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.user.company_id,
    )
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=_default_currency,)
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position', string='Fiscal Position', required=True,
        domain=[('valid_for_dichiarazione_intento', '=', True)])
    state = fields.Selection(
        [('valid', 'Valid'), ('expired', 'Expired'), ('close', 'Close')],
        compute='_compute_state', store=True)
    force_close = fields.Boolean()
    line_ids = fields.One2many('dichiarazione.intento.line',
                               'dichiarazione_id', string='Lines')

    @api.model
    def create(self, values):
        # ----- Check if yearly plafond is enough
        #       to create an in declaration
        # Declaration issued by company are "IN"
        if values.get('type', False) == 'in':
            if isinstance(values['date_start'], dt.date):
                year = str(values['date_start'].year)
            else:
                year = datetime.strptime(
                    values['date_start'], '%Y-%m-%d').strftime('%Y')
            plafond = self.env.user.company_id.\
                dichiarazione_yearly_limit_ids.filtered(
                    lambda r: r.year == year)
            if not plafond:
                raise UserError(_(
                    'Define a yearly plafond for in documents in your company '
                    'settings'
                ))
            date_start = datetime.strptime(
                '01-01-{}'.format(year), '%d-%m-%Y')
            date_end = datetime.strptime(
                '31-12-{}'.format(year), '%d-%m-%Y')
            dichiarazioni = self.search([
                ('date_start', '>=', date_start),
                ('date_end', '<=', date_end),
                ('type', '=', 'in'),
                ])
            actual_limit_total = sum([d.limit_amount for d in dichiarazioni]) \
                + values['limit_amount']
            if actual_limit_total > plafond.limit_amount < plafond.actual_used_amount:
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
                            'All taxes in declaration of intent must be used '
                            'in fiscal position taxes'))

    @api.constrains('limit_amount', 'used_amount', 'line_ids')
    @api.multi
    def _check_available_amount(self):
        for dichiarazione in self:
            if dichiarazione.available_amount < 0:
                raise UserError(_(
                    'Limit passed for declaration %s.\n'
                    'Excess value: %s%s' % (
                        dichiarazione.number,
                        abs(dichiarazione.available_amount),
                        dichiarazione.currency_id.symbol, )))

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            complete_name = record.number
            if record.partner_document_number:
                complete_name = '%s (%s)' % (
                    complete_name, record.partner_document_number)
            res.append((record.id, complete_name), )
        return res

    @api.multi
    @api.depends('line_ids', 'line_ids.amount', 'limit_amount')
    def _compute_amounts(self):
        for record in self:
            amount = sum(line.amount for line in record.line_ids)
            # ----- Force value to 0
            if amount < 0.0:
                amount = 0.0
            record.used_amount = amount
            record.available_amount = record.limit_amount - record.used_amount

    @api.multi
    @api.depends('used_amount', 'limit_amount', 'date_end', 'force_close')
    def _compute_state(self):
        for record in self:
            # ----- If state is forced to be close, close document
            if record.force_close:
                state = 'close'
            # ----- If used amount is bigger than limit, close document
            elif record.limit_amount and \
                    record.used_amount >= record.limit_amount:
                state = 'close'
            # ----- If date is passed, close document
            elif record.date_end and \
                    record.date_end < datetime.today().date():
                state = 'expired'
            else:
                state = 'valid'
            record.state = state

    @api.onchange("fiscal_position_id", "type")
    def onchange_fiscal_position_id(self):
        taxes = self.env['account.tax']
        for tax_mapping in self.fiscal_position_id.tax_ids:
            if tax_mapping.tax_dest_id:
                if (
                    (
                        self.type == 'in' and
                        tax_mapping.tax_dest_id.type_tax_use == 'purchase'
                    )
                    or
                    (
                        self.type == 'out' and
                        tax_mapping.tax_dest_id.type_tax_use == 'sale'
                    )
                ):
                    taxes |= tax_mapping.tax_dest_id
        if taxes:
            self.taxes_ids = [(6, 0, taxes.ids)]

    @api.multi
    def change_force_close(self):
        for record in self:
            record.force_close = not record.force_close

    def get_valid(self, type_d=None, partner_id=False, date=False):
        if not partner_id or not type_d or not date:
            return False
        ignore_state = self.env.context.get('ignore_state', False)
        all_for_partner = self.get_all_for_partner(type_d, partner_id, ignore_state)
        # # ----- return valid documents for partner
        records = all_for_partner.filtered(
            lambda d: d.date_start <= date <= d.date_end
        )
        return records

    def get_all_for_partner(self, type_d=None, partner_id=False,
                            ignore_state=False):
        if not partner_id or not type_d:
            return False
        # ----- return all documents for partner
        domain = [('partner_id', '=', partner_id),
                  ('type', '=', type_d)]
        if not ignore_state:
            domain.append(('state', '!=', 'close'), )
        records = self.search(domain, order='state desc, date')
        return records


class DichiarazioneIntentoLine(models.Model):

    _name = 'dichiarazione.intento.line'
    _description = 'Details of declaration of intent'

    dichiarazione_id = fields.Many2one('dichiarazione.intento',
                                       string='Declaration')
    taxes_ids = fields.Many2many('account.tax', string='Taxes')
    move_line_ids = fields.Many2many('account.move.line', string='Move Lines',
                                     ondelete='cascade')
    amount = fields.Monetary()
    base_amount = fields.Monetary(string='Base Amount')
    invoice_id = fields.Many2one('account.invoice', string='Invoice')
    date_invoice = fields.Date(
        related='invoice_id.date_invoice',
        string='Date Invoice'
    )
    company_id = fields.Many2one(
        "res.company", string="Company", related="dichiarazione_id.company_id",
        store=True,
    )
    currency_id = fields.Many2one('res.currency', string='Currency')
