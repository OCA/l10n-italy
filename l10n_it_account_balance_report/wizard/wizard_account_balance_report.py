# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models, fields

REPORT_TYPES = ('profit_loss', 'balance_sheet')


class ReportAccountBalanceWizard(models.TransientModel):
    _inherit = 'trial.balance.report.wizard'

    account_balance_report_type = fields.Selection(
        [('profit_loss', "Profit & Loss"),
         ('balance_sheet', "Balance Sheet")],
        string="Report Type"
    )

    @api.onchange('show_partner_details')
    def onchange_show_partner_details(self):
        """ Override to avoid unwanted changes """
        if self.account_balance_report_type not in REPORT_TYPES:
            super().onchange_show_partner_details()
        else:
            if self.payable_accounts_only:
                self.payable_accounts_only = False
            if self.receivable_accounts_only:
                self.receivable_accounts_only = False

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        if self.account_balance_report_type not in REPORT_TYPES:
            return super().button_export_html()
        return self.export_account_balance('qweb-html')

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        if self.account_balance_report_type not in REPORT_TYPES:
            return super().button_export_pdf()
        return self.export_account_balance('qweb-pdf')

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        if self.account_balance_report_type not in REPORT_TYPES:
            return super().button_export_xlsx()
        return self.export_account_balance('xlsx')

    def export_account_balance(self, report_type=None):
        self.ensure_one()
        report_obj = self.env['account_balance_report']
        report_vals = self.prepare_report_vals()
        report = report_obj.create(report_vals)
        report.compute_data_for_report()
        return report.print_report(report_type)

    def prepare_report_vals(self):
        self.ensure_one()
        trial_obj = self.env['report_trial_balance']
        trial_vals = self.prepare_trial_balance_vals()
        trial_balance = trial_obj.create(trial_vals)
        trial_balance.compute_data_for_report()
        return {
            'account_balance_report_type': self.account_balance_report_type,
            'trial_balance_id': trial_balance.id,
        }

    def prepare_trial_balance_vals(self):
        self.ensure_one()
        return {
            'company_id': self.company_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'foreign_currency': self.foreign_currency,
            'filter_account_ids': [(6, 0, self.account_ids.ids)],
            'filter_partner_ids': [(6, 0, self.partner_ids.ids)],
            'filter_journal_ids': [(6, 0, self.journal_ids.ids)],
            'fy_start_date': self.fy_start_date,
            'hide_account_at_0': self.hide_account_at_0,
            'hide_parent_hierarchy_level': self.hide_parent_hierarchy_level,
            'hierarchy_on': self.hierarchy_on,
            'limit_hierarchy_level': self.limit_hierarchy_level,
            'only_posted_moves': self.target_move == 'posted',
            'show_hierarchy_level': self.show_hierarchy_level,
            'show_partner_details': self.show_partner_details,
        }
