# Copyright 2026 Nextev
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from odoo.addons.l10n_it_riba_oca.tests.riba_common import TestRibaCommon


class TestFacility(TestRibaCommon):
    def setUp(self):
        super().setUp()
        # Use the SBF config already created by TestRibaCommon
        self.config = self.riba_config_sbf
        self.config.riba_facility_amount = 10000.0
        self.slip = self.env["riba.slip"].create(
            {
                "name": "DIST/TEST/1",
                "config_id": self.config.id,
                "state": "credited",
                "date_credited": date(2026, 10, 1),
            }
        )
        self.line_a = self._line(date(2026, 10, 20), 1000.0, "credited")
        self.line_b = self._line(date(2026, 11, 30), 2000.0, "credited")
        self.line_c = self._line(
            date(2026, 9, 30), 500.0, "credited"
        )  # anomaly: overdue credited
        self.line_d = self._line(date(2026, 10, 25), 700.0, "past_due")
        self.slip.date_past_due = date(2026, 10, 10)
        # Submitted but not yet credited
        slip2 = self.env["riba.slip"].create(
            {"name": "DIST/TEST/2", "config_id": self.config.id, "state": "accepted"}
        )
        self._line(date(2026, 12, 15), 300.0, "confirmed", slip=slip2)

    def _line(self, due_date, amount, state, slip=None):
        line = self.env["riba.slip.line"].create(
            {
                "slip_id": (slip or self.slip).id,
                "partner_id": self.partner.id,
                "due_date": due_date,
                "state": state,
                "sequence": 1,
            }
        )
        self.env["riba.slip.move.line"].create(
            {"riba_line_id": line.id, "amount": amount}
        )
        return line

    def _run(self, date_from, date_to):
        wizard = self.env["riba.facility.wizard"].create(
            {
                "date_from": date_from,
                "date_to": date_to,
                "bank_ids": [(6, 0, self.company_bank.ids)],
            }
        )
        wizard.action_compute()
        return wizard

    def test_facility(self):
        wizard = self._run(date(2026, 10, 12), date(2026, 11, 11))
        summary = wizard.summary_ids
        self.assertEqual(len(summary), 1)
        # Today 12/10: A due 20/10 -> committed, B due 30/11 -> committed,
        # C due 30/09 -> anomaly (overdue credited), D past_due 10/10 -> free
        self.assertAlmostEqual(summary.used_from, 3000.0)
        # At target 11/11: A due 20/10 -> free (from 21/10), B due 30/11 -> used
        self.assertAlmostEqual(summary.used_to, 2000.0)
        self.assertAlmostEqual(summary.available_to, 8000.0)
        self.assertAlmostEqual(summary.to_credit, 300.0)
        self.assertEqual(wizard.anomaly_count, 1)
        anomaly = wizard.detail_ids.filtered("is_anomaly")
        self.assertEqual(anomaly.slip_line_id, self.line_c)

    def test_past_due_always_free(self):
        # past_due with registered date: freed at past due date
        wizard = self._run(date(2026, 10, 10), date(2026, 12, 31))
        # line_d: past_due with slip.date_past_due = 10/10 -> free from 10/10
        self.assertAlmostEqual(wizard.summary_ids.used_from, 3000.0)
        # past_due without registered date: release = start -> never committed
        self.line_d.slip_id.date_past_due = False
        wizard2 = self._run(date(2026, 10, 12), date(2026, 12, 31))
        self.assertAlmostEqual(wizard2.summary_ids.used_from, 3000.0)

    def test_boundary_due_date(self):
        # On the due date of A (20/10): still committed
        wizard = self._run(date(2026, 10, 12), date(2026, 10, 20))
        self.assertAlmostEqual(wizard.summary_ids.used_to, 3000.0)
        # The day after the due date of A (21/10): free
        wizard = self._run(date(2026, 10, 12), date(2026, 10, 21))
        self.assertAlmostEqual(wizard.summary_ids.used_to, 2000.0)

    def test_export_xlsx(self):
        wizard = self._run(date(2026, 10, 12), date(2026, 11, 11))
        action = wizard.action_export_xlsx()
        self.assertEqual(action["type"], "ir.actions.act_url")
