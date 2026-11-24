# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import TransactionCase
from odoo.tools.safe_eval import safe_eval


class TestSendButton(TransactionCase):
    def _is_send_button_invisible(self, **values):
        arch = self.env["account.move"].get_view(view_type="form")["arch"]
        button = etree.fromstring(arch).xpath(
            "//button[@name='action_l10n_it_edi_send']"
        )[0]
        eval_context = {
            "state": "posted",
            "l10n_it_edi_is_self_invoice": True,
            "is_move_sent": False,
            "country_code": "IT",
            "l10n_it_edi_state": False,
            "l10n_it_document_type_code": False,
            **values,
        }
        return safe_eval(button.get("invisible"), eval_context)

    def test_send_button_visible(self):
        """Self-invoices can be sent to SDI,
        also when no document type is set."""
        self.assertFalse(self._is_send_button_invisible())
        for code in ("TD16", "TD17", "TD20", "TD28"):
            self.assertFalse(
                self._is_send_button_invisible(l10n_it_document_type_code=code),
                code,
            )

    def test_send_button_invisible(self):
        """Documents of type TD01, TD04 and TD24 are never sent to SDI."""
        for code in ("TD01", "TD04", "TD24"):
            self.assertTrue(
                self._is_send_button_invisible(l10n_it_document_type_code=code),
                code,
            )

    def test_send_button_standard_conditions(self):
        """Standard conditions still hide the button."""
        self.assertTrue(self._is_send_button_invisible(state="draft"))
        self.assertTrue(
            self._is_send_button_invisible(l10n_it_edi_is_self_invoice=False)
        )
