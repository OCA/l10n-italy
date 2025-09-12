# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestExport(Common):
    def test_narration(self):
        """The narration included in the invoice
        is exported to the XML in Causale nodes."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.narration = "first line\n\nsecond line"
        invoice.action_post()
        self._assert_export_invoice(invoice, "narration.xml")
