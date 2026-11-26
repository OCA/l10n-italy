# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import xlrd

from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

N_START, N_END = "2024-01-01", "2024-12-31"
N1_START, N1_END = "2025-01-01", "2025-12-31"


@tagged("post_install", "-at_install")
class TestTrialBalanceIgnoreClosingMove(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.revenue = cls.company_data["default_account_revenue"]
        cls.expense = cls.company_data["default_account_expense"]
        cls.asset = cls.company_data["default_account_assets"]
        cls.misc_journal = cls.company_data["default_journal_misc"]
        cls.capital, cls.result = (
            cls.env["account.account"].create(
                {"code": code, "name": code, "account_type": "equity"}
            )
            for code in ("TBICM.CAP", "TBICM.RES")
        )
        cls.opening_journal, cls.closing_journal = (
            cls.env["account.journal"].create(
                {"name": code, "code": code, "type": "general"}
            )
            for code in ("TBOPN", "TBCLS")
        )
        # Start-up balances, not created by the closing procedure
        cls.start_move = cls._create_move(
            N_START, cls.asset, cls.capital, 5000, journal=cls.opening_journal
        )
        cls._create_move("2024-03-01", cls.asset, cls.revenue, 1000)
        cls._create_move("2024-04-01", cls.expense, cls.asset, 400)

    @classmethod
    def _create_move(cls, date, debit_account, credit_account, amount, **kwargs):
        journal = kwargs.pop("journal", cls.misc_journal)
        move = cls.env["account.move"].create(
            dict(
                date=date,
                journal_id=journal.id,
                line_ids=[
                    (0, 0, {"account_id": debit_account.id, "debit": amount}),
                    (0, 0, {"account_id": credit_account.id, "credit": amount}),
                ],
                **kwargs,
            )
        )
        move.action_post()
        return move

    def _close_fiscal_year(self):
        def mapping(accounts, dest=False):
            return [
                (0, 0, {"src_accounts": a.code, "dest_account_id": dest and dest.id})
                for a in accounts
            ]

        def config(code, move_type, sequence, date, **vals):
            vals.update(
                name=code,
                code=code,
                move_type=move_type,
                sequence=sequence,
                date=date,
                journal_id=self.closing_journal.id,
                closing_type_default="balance",
            )
            return (0, 0, vals)

        closing = self.env["account.fiscalyear.closing"].create(
            {
                "name": "Closing 2024",
                "date_start": N_START,
                "date_end": N_END,
                "date_opening": N1_START,
                "move_config_ids": [
                    config(
                        "PL",
                        "loss_profit",
                        1,
                        N_END,
                        mapping_ids=mapping(self.revenue | self.expense, self.result),
                    ),
                    config(
                        "BS",
                        "closing",
                        2,
                        N_END,
                        mapping_ids=mapping(self.asset | self.capital | self.result),
                    ),
                    config("OPEN", "opening", 3, N1_START, inverse="BS"),
                ],
            }
        )
        self.assertIs(closing.button_calculate(), True)
        closing.button_post()
        self.assertEqual(
            sorted(closing.move_ids.mapped("closing_type")),
            ["closing", "loss_profit", "opening"],
        )
        return closing

    def _wizard(self, date_from, date_to, **vals):
        return (
            self.env["trial.balance.report.wizard"]
            .with_context(discard_logo_check=True)
            .create(dict(date_from=date_from, date_to=date_to, **vals))
        )

    def _trial_balance(self, date_from, date_to, **vals):
        """Return {account code: (initial, debit, credit, ending)}."""
        wizard = self._wizard(date_from, date_to, **vals)
        res = self.env["report.account_financial_report.trial_balance"]
        lines = res._get_report_values(wizard.ids, wizard._prepare_report_data())[
            "trial_balance"
        ]
        return {
            line["code"]: tuple(
                round(line[k], 2)
                for k in ("initial_balance", "debit", "credit", "ending_balance")
            )
            for line in lines
        }

    def _balance_sheet(self, date_from, date_to, **vals):
        """Return (total assets, total liabilities, {line: ending balance})."""
        wizard = self._wizard(
            date_from, date_to, financial_statements_report_type="balance_sheet", **vals
        )
        data = self.env[
            "report.l10n_it_financial_statements_report.report"
        ].compute_data_for_report(wizard._prepare_report_data())
        lines = data["section_debit_ids"] + data["section_credit_ids"]
        return (
            round(data["total_debit"], 2),
            round(data["total_credit"], 2),
            {
                (line["account_id"], line["group_id"]): line["ending_balance"]
                for line in lines
            },
        )

    def _render(self, wizard, report_type):
        """Render `wizard` in `report_type` and return the text of the report."""
        action = getattr(wizard, "button_export_" + report_type)()
        self.assertIn("ignore_closing_move", action["data"])
        content, _ext = self.env["ir.actions.report"]._render(
            action["report_name"], wizard.ids, data=action["data"]
        )
        if report_type != "xlsx":
            return content.decode()
        sheet = xlrd.open_workbook(file_contents=content).sheet_by_index(0)
        return " ".join(
            str(sheet.cell_value(r, c))
            for r in range(sheet.nrows)
            for c in range(sheet.ncols)
        )

    def test_default(self):
        self.assertTrue(self._wizard(N_START, N_END).ignore_closing_move)

    def test_fiscal_year_closing(self):
        """Closing (N) and opening (N+1) moves are ignored only with the option."""
        expected_n = self._trial_balance(N_START, N_END)
        expected_n1 = self._trial_balance(N1_START, N1_END)
        # Start-up balances (closing_type none) are always included
        self.assertEqual(self.start_move.closing_type, "none")
        self.assertEqual(expected_n["TBICM.CAP"], (0, 0, 5000, -5000))

        self._close_fiscal_year()

        self.assertEqual(self._trial_balance(N_START, N_END), expected_n)
        self.assertEqual(self._trial_balance(N1_START, N1_END), expected_n1)

        standard_n = self._trial_balance(N_START, N_END, ignore_closing_move=False)
        self.assertNotEqual(standard_n, expected_n)
        self.assertEqual(standard_n[self.revenue.code][3], 0)
        self.assertEqual(standard_n["TBICM.CAP"], (0, 5000, 5000, 0))
        standard_n1 = self._trial_balance(N1_START, N1_END, ignore_closing_move=False)
        self.assertNotEqual(standard_n1, expected_n1)
        self.assertEqual(standard_n1["TBICM.RES"], (0, 0, 600, -600))
        self.assertNotIn("TBICM.RES", expected_n1)

    def test_other_closing_type(self):
        """Moves with closing type 'other' are ignored."""
        expected = self._trial_balance(N_START, N_END)
        self._create_move(N_END, self.expense, self.asset, 50, closing_type="other")

        self.assertEqual(self._trial_balance(N_START, N_END), expected)
        standard = self._trial_balance(N_START, N_END, ignore_closing_move=False)
        self.assertEqual(standard[self.expense.code], (0, 450, 0, 450))

    def test_journal_filter(self):
        """The option works together with the journal filter."""
        self._create_move(N_END, self.expense, self.asset, 50, closing_type="other")
        journal_filter = {"journal_ids": [fields.Command.set(self.misc_journal.ids)]}

        result = self._trial_balance(N_START, N_END, **journal_filter)
        self.assertNotIn("TBICM.CAP", result)
        self.assertEqual(result[self.expense.code], (0, 400, 0, 400))
        self.assertEqual(result[self.asset.code], (0, 1000, 400, 600))

    def test_balance_sheet(self):
        """Balance sheet (l10n_it_financial_statements_report) ignores closing moves."""
        expected_n = self._balance_sheet(N_START, N_END)
        expected_n1 = self._balance_sheet(N1_START, N1_END)

        self._close_fiscal_year()

        self.assertEqual(self._balance_sheet(N_START, N_END), expected_n)
        self.assertEqual(self._balance_sheet(N1_START, N1_END), expected_n1)
        self.assertNotEqual(
            self._balance_sheet(N_START, N_END, ignore_closing_move=False), expected_n
        )

    def test_render(self):
        """HTML, PDF and XLSX reports of trial balance and balance sheet."""
        self._close_fiscal_year()
        for report_vals in ({}, {"financial_statements_report_type": "balance_sheet"}):
            for report_type in ("html", "pdf", "xlsx"):
                with self.subTest(report=report_vals, report_type=report_type):
                    ignored = self._render(
                        self._wizard(N1_START, N1_END, **report_vals), report_type
                    )
                    self.assertNotIn("TBICM.RES", ignored)
                    self.assertIn("TBICM.CAP", ignored)
                    standard = self._render(
                        self._wizard(
                            N1_START,
                            N1_END,
                            ignore_closing_move=False,
                            **report_vals,
                        ),
                        report_type,
                    )
                    self.assertIn("TBICM.RES", standard)
