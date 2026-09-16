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
            "l10n_it_edi_is_self_invoice": False,
            "l10n_it_edi_is_td29": False,
            "is_move_sent": False,
            "country_code": "IT",
            "l10n_it_edi_state": False,
            "l10n_it_document_type_code": False,
            **values,
        }
        return safe_eval(button.get("invisible"), eval_context)

    def test_send_button_td29(self):
        """TD29 documents can be sent to SDI, unless their document type
        is TD01, TD04 or TD24."""
        self.assertTrue(self._is_send_button_invisible())
        self.assertFalse(self._is_send_button_invisible(l10n_it_edi_is_td29=True))
        self.assertFalse(
            self._is_send_button_invisible(l10n_it_edi_is_self_invoice=True)
        )
        for code in ("TD01", "TD04", "TD24"):
            self.assertTrue(
                self._is_send_button_invisible(
                    l10n_it_edi_is_td29=True, l10n_it_document_type_code=code
                ),
                code,
            )
