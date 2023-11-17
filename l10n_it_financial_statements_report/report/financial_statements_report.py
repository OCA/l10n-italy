# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


def get_xmlid(id_str):
    id_str = id_str.replace(".", "")
    return f"l10n_it_financial_statements_report.{id_str}"


class ReportFinancialStatementsReport(models.AbstractModel):
    _name = "report.l10n_it_financial_statements_report.report"
    _description = "Financial Statements QWeb Report"
    _inherit = "report.account_financial_report.abstract_report"

    def print_report(self, wizard, report_data, report_type=None):
        """
        This method is called from the JS widget buttons 'Print'
        and 'Export' in the HTML view.
        Prints PDF and XLSX reports.
        :param report_type: string that represents the report type
        """
        report_type = report_type or "qweb-pdf"
        if report_type in ("qweb-pdf", "xlsx", "qweb-html"):
            res = self.do_print(wizard, report_data, report_type)
        elif report_type:
            raise ValidationError(
                _(
                    "No report has been defined for report type '{}'.",
                    report_type,
                )
            )
        else:
            raise ValidationError(
                _("No report type has been declared for current print.")
            )
        return res

    def do_print(self, wizard, report_data, report_type):
        if report_type == "qweb-pdf":
            xml_id = get_xmlid("report_financial_statements_report_pdf")
        elif report_type == "qweb-html":
            xml_id = get_xmlid("report_financial_statements_report_html")
        else:
            xml_id = get_xmlid("report_financial_statements_report_xlsx")
        report = self.env.ref(xml_id)
        return report.report_action(wizard, data=report_data)

    def compute_data_for_report(self, wizard_data):
        """
        Sets data for report.
        Defines which lines go on the left (or right) section, which names
        sections should have, the report title, amounts and balances
        """
        rep_type = wizard_data.get("financial_statements_report_type")

        trial_balance_data = self.env[
            "report.account_financial_report.trial_balance"
        ]._get_report_values([], wizard_data)

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
        l_sec, l_name = cols["left"]["section"], cols["left"]["name"]
        r_sec, r_name = cols["right"]["section"], cols["right"]["name"]
        valid_sections = [l_sec, r_sec]

        date_from = trial_balance_data["date_from"]
        date_to = trial_balance_data["date_to"]
        show_partner_details = trial_balance_data["show_partner_details"]

        # 'trial_balance' is only filled when show_partner_details is False
        trial_balance_lines = (
            trial_balance_data["total_amount"]
            if show_partner_details
            else trial_balance_data["trial_balance"]
        )
        for trial_balance_line in trial_balance_lines:
            if show_partner_details:
                line_id = trial_balance_line
                trial_balance_line = trial_balance_lines[line_id]
                line_type = "account_type"
            else:
                line_id = trial_balance_line["id"]
                line_type = trial_balance_line["type"]

            if line_type == "account_type":
                account = self.env["account.account"].browse(line_id)
                account_group = self.env["account.group"].browse()
            elif line_type == "group_type":
                account = self.env["account.account"].browse()
                account_group = self.env["account.group"].browse(line_id)
            else:
                account = self.env["account.account"].browse()
                account_group = self.env["account.group"].browse()

            section = self.get_report_section(account, account_group)
            if not (section and section in valid_sections):
                continue

            sign = self.get_balance_sign(account, account_group)
            trial_balance_line["ending_balance"] *= sign
            if show_partner_details:
                partner_ids = list(
                    filter(lambda k: isinstance(k, int), trial_balance_line.keys())
                )
                for partner_id in partner_ids:
                    trial_balance_line[partner_id]["ending_balance"] *= sign
            else:
                partner_ids = []

            report_line_vals = trial_balance_line

            report_line_vals.update(
                {
                    "date_from": date_from,
                    "date_to": date_to,
                    "account_id": account.id,
                    "group_id": account_group.id,
                    "compute_account_ids": account_group.compute_account_ids.ids,
                    "report_partner_ids": [
                        {
                            "date_from": date_from,
                            "date_to": date_to,
                            "account_id": account.id,
                            "partner_id": pid,
                            "ending_balance": report_line_vals[pid].get(
                                "ending_balance", 0
                            ),
                        }
                        for pid in partner_ids
                    ],
                }
            )

            if section == r_sec:
                section_credit_vals.append(report_line_vals)
                if not account_group:
                    total_credit += report_line_vals["ending_balance"]
            elif section == l_sec:
                section_debit_vals.append(report_line_vals)
                if not account_group:
                    total_debit += report_line_vals["ending_balance"]

        company_id = wizard_data["company_id"]
        company = self.env["res.company"].browse(company_id)
        curr = company.currency_id
        digits = curr.decimal_places
        if not digits:
            digits = self.env["decimal.precision"].precision_get("Account")
        total_balance = 0
        if float_compare(total_credit, total_debit, digits) == 1:
            total_balance = total_credit - total_debit
        elif float_compare(total_credit, total_debit, digits) == -1:
            total_balance = total_debit - total_credit

        # Preserve generic data like accounts_data and similar
        report_data = trial_balance_data
        report_data.update(
            {
                "left_col_name": l_name,
                "right_col_name": r_name,
                "section_credit_ids": section_credit_vals,
                "section_debit_ids": section_debit_vals,
                "title": cols["title"],
                "total_balance": total_balance,
                "total_credit": total_credit,
                "total_debit": total_debit,
            }
        )
        return report_data

    def get_column_data(self):
        """
        This method is meant to be overridden if necessary.
        :returns: report data grouped by report type
        """
        return {
            "balance_sheet": {
                "left": {
                    "section": "assets",
                    "name": _("ASSETS"),
                },
                "right": {
                    "section": "liabilities",
                    "name": _("LIABILITIES"),
                },
                "title": _("BALANCE SHEET"),
            },
            "profit_loss": {
                "left": {
                    "section": "expenses",
                    "name": _("COSTS"),
                },
                "right": {
                    "section": "incomes",
                    "name": _("REVENUES"),
                },
                "title": _("PROFIT & LOSS"),
            },
        }

    def get_report_section(self, account=None, group=None):
        section = ""
        if not account and group and group.account_ids:
            account = group.account_ids[0]
        if account:
            section = account.financial_statements_report_section
        return section

    @api.model
    def get_html(self, given_context=None):
        """Method needed from JavaScript widget to render HTML view"""
        context = dict(self.env.context)
        context.update(given_context or {})
        report = self or self.browse(context.get("active_id"))
        xml_id = get_xmlid("template_financial_statements_report")

        result = {}
        if report:
            context["o"] = report
            result["html"] = self.env.ref(xml_id).render(context)
        return result

    def get_balance_sign(self, account, account_group):
        sign = 1
        if account:
            sign = account.account_balance_sign
        elif account_group:
            sign = account_group.account_balance_sign
        return sign

    @api.model
    def _get_report_values(self, docids, data=None):
        report_data = self.compute_data_for_report(data)

        wizard_id = data["wizard_id"]
        wizard_model = "trial.balance.report.wizard"
        report_data.update(
            {
                "doc_ids": [wizard_id],
                "doc_model": wizard_model,
                "docs": self.env[wizard_model].browse(wizard_id),
            }
        )
        return report_data
