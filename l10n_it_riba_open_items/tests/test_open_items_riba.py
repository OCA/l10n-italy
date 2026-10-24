# Copyright 2026 nextev.it
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tests import tagged

from odoo.addons.l10n_it_riba_oca.tests.riba_common import TestRibaCommon


@tagged("post_install", "-at_install")
class TestOpenItemsRiba(TestRibaCommon):
    def setUp(self):
        super().setUp()
        self.today = fields.Date.context_today(self.env.user)
        # Termine di pagamento RiBa 30/60: doppia scadenza
        self.pterm_double = self._create_pterm()
        self.pterm_double.riba_payment_cost = 0.0
        self.invoice = self._create_sbf_invoice()
        self.invoice.invoice_payment_term_id = self.pterm_double
        self.invoice._onchange_riba_partner_bank_id()
        self.invoice.action_post()
        self.rec_lines = self.invoice.line_ids.filtered(
            lambda line: (
                line.account_id.id == self.account_rec1_id.id and not line.reconciled
            )
        )
        self.assertEqual(len(self.rec_lines), 2, "Expected two due dates")

    def _issue_and_accept(self, rec_lines):
        wizard = self.env["riba.issue"].create(
            {"configuration_id": self.riba_config_sbf.id}
        )
        action = wizard.with_context(active_ids=rec_lines.ids).create_list()
        slip = self.env["riba.slip"].browse(action["res_id"])
        slip.date_accepted = self.today
        slip.confirm()
        return slip

    def _report_values(self, show=True):
        wizard = self.env["open.items.report.wizard"].create(
            {
                "date_at": self.today,
                "account_ids": [(6, 0, [self.account_rec1_id.id])],
                "partner_ids": [(6, 0, [self.partner.id])],
                "show_partner_details": True,
                "show_riba_uncovered": show,
            }
        )
        data = wizard._prepare_report_data()
        values = self.env[
            "report.account_financial_report.open_items"
        ]._get_report_values(wizard, data)
        return wizard, data, values

    def _report_lines(self, values):
        lines = values["Open_Items"].get(self.account_rec1_id.id, {})
        return {
            line["id"]: line for by_partner in lines.values() for line in by_partner
        }

    def test_accepted_riba_shown_with_zero_balance(self):
        self._issue_and_accept(self.rec_lines)
        self.assertTrue(all(self.rec_lines.mapped("reconciled")))

        _wizard, _data, values = self._report_values()
        lines = self._report_lines(values)
        self.assertEqual(set(lines), set(self.rec_lines.ids))
        for rec_line in self.rec_lines:
            line = lines[rec_line.id]
            self.assertEqual(line["amount_residual"], 0.0)
            self.assertAlmostEqual(line["riba_uncovered"], rec_line.debit)
            self.assertTrue(line["riba_closed"])
        totals = values["total_amount"][self.account_rec1_id.id]
        self.assertAlmostEqual(totals["residual"], 0.0)
        self.assertAlmostEqual(
            totals["riba_uncovered"], sum(self.rec_lines.mapped("debit"))
        )

    def test_option_disabled_keeps_standard_behaviour(self):
        self._issue_and_accept(self.rec_lines)
        _wizard, _data, values = self._report_values(show=False)
        self.assertFalse(self._report_lines(values))

    def test_one_due_date_issued(self):
        """Solo la prima scadenza in distinta: la seconda resta aperta."""
        first, second = self.rec_lines.sorted("date_maturity")
        self._issue_and_accept(first)
        _wizard, _data, values = self._report_values()
        lines = self._report_lines(values)
        self.assertEqual(lines[first.id]["amount_residual"], 0.0)
        self.assertAlmostEqual(lines[first.id]["riba_uncovered"], first.debit)
        self.assertAlmostEqual(lines[second.id]["amount_residual"], second.debit)
        self.assertEqual(lines[second.id]["riba_uncovered"], 0.0)
        totals = values["total_amount"][self.account_rec1_id.id]
        self.assertAlmostEqual(totals["residual"], second.debit)
        self.assertAlmostEqual(totals["riba_uncovered"], first.debit)

    def _credit(self, slip):
        credit_wizard = (
            self.env["riba.credit"]
            .with_context(
                active_model="riba.slip", active_ids=slip.ids, active_id=slip.id
            )
            .create(
                {
                    "credit_amount": sum(self.rec_lines.mapped("debit")),
                    "expense_amount": 0,
                }
            )
        )
        res = credit_wizard.create_move()
        self.env["account.move"].browse(res["res_id"]).action_post()

    def test_settled_riba_disappears(self):
        slip = self._issue_and_accept(self.rec_lines)
        self._credit(slip)
        _wizard, _data, values = self._report_values()
        self.assertEqual(len(self._report_lines(values)), 2)

        slip.line_ids.riba_line_settlement(date=self.today)
        self.assertEqual(set(slip.line_ids.mapped("state")), {"paid"})
        _wizard, _data, values = self._report_values()
        self.assertFalse(self._report_lines(values))

    def test_one_due_date_paid(self):
        """Doppia scadenza: una pagata, l'altra ancora a rischio."""
        slip = self._issue_and_accept(self.rec_lines)
        self._credit(slip)
        riba_first = slip.line_ids.sorted("due_date")[0]
        riba_first.state = "paid"

        _wizard, _data, values = self._report_values()
        lines = self._report_lines(values)
        paid_ml = riba_first.move_line_ids.move_line_id
        self.assertNotIn(paid_ml.id, lines)
        self.assertEqual(len(lines), 1)
        other = self.rec_lines - paid_ml
        self.assertAlmostEqual(lines[other.id]["riba_uncovered"], other.debit)

    def test_render_pdf_html_xlsx(self):
        self._issue_and_accept(self.rec_lines)
        wizard, data, _values = self._report_values()
        report_model = self.env["ir.actions.report"]
        html = report_model._render_qweb_html(
            "account_financial_report.action_print_report_open_items_html",
            wizard.ids,
            data,
        )[0]
        self.assertIn(b"RiBa uncovered", html)
        xlsx = report_model._render(
            "account_financial_report.action_report_open_items_xlsx",
            wizard.ids,
            data,
        )[0]
        self.assertTrue(xlsx)
