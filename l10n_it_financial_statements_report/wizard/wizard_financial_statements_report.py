# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

REPORT_TYPES = ("profit_loss", "balance_sheet")


class ReportFinancialStatementsWizard(models.TransientModel):
    _inherit = "trial.balance.report.wizard"

    financial_statements_report_type = fields.Selection(
        [("profit_loss", "Profit & Loss"), ("balance_sheet", "Balance Sheet")],
        string="Report Type",
    )
    hide_accounts_codes = fields.Boolean()

    @api.onchange("show_partner_details")
    def onchange_show_partner_details(self):
        """Override to avoid unwanted changes"""
        res = None
        if self.financial_statements_report_type not in REPORT_TYPES:
            res = super().onchange_show_partner_details()
        else:
            if self.payable_accounts_only:
                self.payable_accounts_only = False
            if self.receivable_accounts_only:
                self.receivable_accounts_only = False
        return res

    def prepare_report_vals(self):
        self.ensure_one()
        return {
            "financial_statements_report_type": self.financial_statements_report_type,
            "hide_accounts_codes": self.hide_accounts_codes,
            "wizard_id": self.id,
            "company_id": self.company_id.id,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "foreign_currency": self.foreign_currency,
            "account_ids": self.account_ids.ids or [],
            "partner_ids": self.partner_ids.ids or [],
            "journal_ids": self.journal_ids.ids or [],
            "fy_start_date": self.fy_start_date,
            "hide_account_at_0": self.hide_account_at_0,
            "hide_parent_hierarchy_level": self.hide_parent_hierarchy_level,
            "show_hierarchy": self.show_hierarchy,
            "limit_hierarchy_level": self.limit_hierarchy_level,
            "only_posted_moves": self.target_move == "posted",
            "show_hierarchy_level": self.show_hierarchy_level,
            "show_partner_details": self.show_partner_details,
            "unaffected_earnings_account": self.unaffected_earnings_account.id,
            "account_financial_report_lang": self.env.lang,
        }

    def _print_report(self, report_type):
        """
        This method is called from the JS widget buttons 'Print'
        and 'Export' in the HTML view.
        Prints PDF, HTML and XLSX reports.
        :param report_type: string that represents the report type
        """
        self.ensure_one()
        if self.financial_statements_report_type not in REPORT_TYPES:
            return super()._print_report(report_type)
        report_data = self.prepare_report_vals()
        return self.env[
            "report.l10n_it_financial_statements_report.report"
        ].print_report(self, report_data, report_type=report_type)
