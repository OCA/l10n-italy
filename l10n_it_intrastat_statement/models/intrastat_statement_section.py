#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class IntrastatStatementSection(models.AbstractModel):
    _name = 'account.intrastat.statement.section'
    _description = "Fields and methods common to all Intrastat sections"

    statement_id = fields.Many2one(
        comodel_name='account.intrastat.statement',
        string="Statement",
        readonly=True,
        ondelete='cascade')
    sequence = fields.Integer(
        string="Progr.")
    partner_id = fields.Many2one(
        comodel_name='res.partner')
    country_partner_id = fields.Many2one(
        comodel_name='res.country',
        string="Partner State")
    vat_code = fields.Char()
    amount_euro = fields.Integer(
        string="Amount in Euro",
        digits=dp.get_precision('Account'))
    invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string="Invoice",
        readonly=True)
    intrastat_code_id = fields.Many2one(
        comodel_name='report.intrastat.code')

    @api.multi
    def apply_partner_data(self, partner_data):
        self.ensure_one()
        if 'country_partner_id' in partner_data:
            self.country_partner_id = partner_data['country_partner_id']
        if 'vat_code' in partner_data:
            self.vat_code = partner_data['vat_code']

    @api.onchange('partner_id')
    def change_partner_id(self):
        if not self.partner_id:
            return
        intrastat_model = self.env['account.invoice.intrastat']
        partner_data = intrastat_model._get_partner_data(self.partner_id)
        self.apply_partner_data(partner_data)

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        company_id = self.env.context.get(
            'company_id', self.env.user.company_id)
        invoice_id = inv_intra_line.invoice_id
        partner_id = invoice_id.partner_id

        # Amounts
        dp_model = self.env['decimal.precision']
        amount_euro = statement_id.round_min_amount(
            inv_intra_line.amount_euro,
            statement_id.company_id or company_id,
            dp_model.precision_get('Account'))

        return {
            'invoice_id': invoice_id.id,
            'partner_id': partner_id.id,
            'country_partner_id': inv_intra_line.country_partner_id.id,
            'vat_code': partner_id.vat and partner_id.vat[2:],
            'amount_euro': amount_euro,
            'intrastat_code_id': inv_intra_line.intrastat_code_id.id,
        }

    @api.multi
    def _export_line_checks(self, section_label, section_number):
        self.ensure_one()
        if not self.vat_code:
            raise ValidationError(
                _("Missing vat code for %s on '%s - Section %s'")
                % (self.partner_id.display_name,
                   section_label,
                   section_number))
        country_id = self.country_partner_id or self.partner_id.country_id
        if country_id:
            country_id.intrastat_validate()
        else:
            raise ValidationError(_("Missing State for Partner %s")
                                  % self.partner_id.display_name)

    @api.multi
    def get_amount_euro(self):
        return sum(section.amount_euro for section in self)
