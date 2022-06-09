# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools.pycompat import string_types
from odoo.tools.safe_eval import safe_eval


def get_xmlid(id_str):
    id_str = id_str.replace('.', '')
    return 'l10n_it_account_balance_report.{}'.format(id_str)


class ReportAccountBalanceReport(models.TransientModel):
    _name = 'account_balance_report'
    _inherit = 'account_financial_report_abstract'
    _inherits = {'report_trial_balance': 'trial_balance_id'}

    account_balance_report_type = fields.Selection(
        [('profit_loss', "Profit & Loss"),
         ('balance_sheet', "Balance Sheet")],
    )
    left_col_name = fields.Char()
    right_col_name = fields.Char()
    section_credit_ids = fields.One2many(
        'account_balance_report_account',
        'report_credit_id'
    )
    section_debit_ids = fields.One2many(
        'account_balance_report_account',
        'report_debit_id'
    )
    title = fields.Char()
    total_balance = fields.Float(
        digits=(16, 2)
    )
    total_credit = fields.Float(
        digits=(16, 2)
    )
    total_debit = fields.Float(
        digits=(16, 2)
    )
    trial_balance_id = fields.Many2one(
        'report_trial_balance',
        ondelete='cascade',
        required=True,
        index=True,
    )

    @api.multi
    def print_report(self, report_type=None):
        """
        This method is called from the JS widget buttons 'Print'
        and 'Export' in the HTML view.
        Prints PDF and XLSX reports.
        :param report_type: string that represents the report type
        """
        self.ensure_one()
        report_type = report_type or 'qweb-pdf'
        if report_type in ('qweb-pdf', 'xlsx'):
            res = self.do_print(report_type)
        elif report_type == 'qweb-html':
            res = self.view_report()
        elif report_type:
            raise ValidationError(
                _("No report has been defined for report type '{}'."
                  .format(report_type))
            )
        else:
            raise ValidationError(
                _("No report type has been declared for current print.")
            )
        return res

    def do_print(self, report_type):
        self.ensure_one()
        if report_type == 'qweb-pdf':
            xml_id = get_xmlid('report_account_balance_report_pdf')
        else:
            xml_id = get_xmlid('report_account_balance_report_xlsx')
        report = self.env.ref(xml_id)
        return report.report_action(self)

    @api.multi
    def view_report(self):
        """ Launches view for HTML report """
        self.ensure_one()
        [act] = self.env.ref(get_xmlid('action_account_balance_report')).read()
        ctx = act.get('context', {})
        if isinstance(ctx, string_types):
            ctx = safe_eval(ctx)
        # Call update twice to force 'active_%s' values to be overridden
        ctx.update(dict(self._context))
        ctx.update(active_id=self.id, active_ids=self.ids)
        act['context'] = ctx
        return act

    @api.multi
    def compute_data_for_report(self):
        """
        Sets data for report.
        Defines which lines go on the left (or right) section, which names
        sections should have, the report title, amounts and balances
        """
        self.ensure_one()
        rep_type = self.account_balance_report_type

        # Trial balance already has every data we may need
        section_credit_vals = []
        section_debit_vals = []
        total_credit = 0
        total_debit = 0
        cols = self.get_column_data().get(rep_type)
        if not cols:
            raise ValidationError(
                _("Unknown report type; cannot parse it into a table.")
            )
        l_sec, l_name = cols['left']['section'], cols['left']['name']
        r_sec, r_name = cols['right']['section'], cols['right']['name']
        valid_sections = [l_sec, r_sec]

        for trial_acc_line in self.trial_balance_id.account_ids:
            section = self.get_report_section(
                trial_acc_line.account_id, trial_acc_line.account_group_id
            )
            if not (section and section in valid_sections):
                continue

            sign = trial_acc_line.get_balance_sign()
            trial_acc_line.final_balance *= sign
            for trial_partner_line in trial_acc_line.partner_ids:
                trial_partner_line.final_balance *= sign

            balance_line_vals = (
                0, 0, {
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'report_partner_ids': [(
                        0, 0, {
                            'date_from': self.date_from,
                            'date_to': self.date_to,
                            'report_id': self.id,
                            'trial_balance_partner_id': pid
                        }) for pid in trial_acc_line.partner_ids.ids],
                    'trial_balance_line_id': trial_acc_line.id,
                }
            )

            if section == r_sec:
                section_credit_vals.append(balance_line_vals)
                if not trial_acc_line.account_group_id:
                    total_credit += trial_acc_line.final_balance
            elif section == l_sec:
                section_debit_vals.append(balance_line_vals)
                if not trial_acc_line.account_group_id:
                    total_debit += trial_acc_line.final_balance

        curr = self.company_id.currency_id or self.company_id._get_euro()
        digits = curr.decimal_places
        if not digits:
            digits = self.env['decimal.precision'].precision_get('Account')
        total_balance = 0
        if float_compare(total_credit, total_debit, digits) == 1:
            total_balance = total_credit - total_debit
        elif float_compare(total_credit, total_debit, digits) == -1:
            total_balance = total_debit - total_credit

        self.write({
            'left_col_name': l_name,
            'right_col_name': r_name,
            'section_credit_ids': section_credit_vals,
            'section_debit_ids': section_debit_vals,
            'title': cols['title'],
            'total_balance': total_balance,
            'total_credit': total_credit,
            'total_debit': total_debit,
        })

    def get_column_data(self):
        """
        This method is meant to be overridden if necessary.
        :returns: report data grouped by report type
        """
        return {
            'balance_sheet': {
                'left': {
                    'section': 'assets',
                    'name': _("ASSETS"),
                },
                'right': {
                    'section': 'liabilities',
                    'name': _("LIABILITIES"),
                },
                'title': _("BALANCE SHEET")
            },
            'profit_loss': {
                'left': {
                    'section': 'expenses',
                    'name': _("COSTS"),
                },
                'right': {
                    'section': 'incomes',
                    'name': _("REVENUES"),
                },
                'title': _("PROFIT & LOSS")
            },
        }

    def get_report_section(self, account=None, group=None):
        section = ''
        if not account and group and group.account_ids:
            account = group.account_ids[0]
        if account:
            section = account.account_balance_report_section
        return section

    @api.model
    def get_html(self, given_context=None):
        """ Method needed from JavaScript widget to render HTML view """
        context = dict(self.env.context)
        context.update(given_context or {})
        report = self or self.browse(context.get('active_id'))
        xml_id = get_xmlid('template_account_balance_report')

        result = {}
        if report:
            context['o'] = report
            result['html'] = self.env.ref(xml_id).render(context)
        return result


class ReportAccountBalanceReportAccount(models.TransientModel):
    _name = 'account_balance_report_account'
    _inherit = 'account_financial_report_abstract'
    _inherits = {'report_trial_balance_account': 'trial_balance_line_id'}

    date_from = fields.Date()
    date_to = fields.Date()
    report_partner_ids = fields.One2many(
        'account_balance_report_partner',
        'report_section_id',
    )
    report_credit_id = fields.Many2one(
        'account_balance_report',
        ondelete='cascade',
        index=True
    )
    report_debit_id = fields.Many2one(
        'account_balance_report',
        ondelete='cascade',
        index=True
    )
    trial_balance_line_id = fields.Many2one(
        'report_trial_balance_account',
        ondelete='cascade',
        required=True,
        index=True
    )


class ReportAccountBalanceReportPartner(models.TransientModel):
    _name = 'account_balance_report_partner'
    _inherit = 'account_financial_report_abstract'
    _inherits = {'report_trial_balance_partner': 'trial_balance_partner_id'}

    date_from = fields.Date()
    date_to = fields.Date()
    hide_line = fields.Boolean(
        compute='_compute_hide_line'
    )
    report_id = fields.Many2one(
        'account_balance_report',
    )
    report_section_id = fields.Many2one(
        'account_balance_report_account',
        ondelete='cascade',
        index=True
    )
    trial_balance_partner_id = fields.Many2one(
        'report_trial_balance_partner',
        ondelete='cascade',
        required=True,
        index=True
    )

    @api.multi
    @api.depends('final_balance',
                 'report_id.hide_account_at_0',
                 'trial_balance_partner_id.final_balance')
    def _compute_hide_line(self):
        report = self.mapped('report_section_id.report_credit_id') \
            + self.mapped('report_section_id.report_debit_id')
        if report.hide_account_at_0:
            for partner_line in self:
                p_bal = partner_line.final_balance
                digits = partner_line.currency_id.decimal_places
                partner_line.hide_line = float_is_zero(p_bal, digits)
