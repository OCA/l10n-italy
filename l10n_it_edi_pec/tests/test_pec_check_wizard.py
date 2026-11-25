# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TestItEdiPecCommon


@tagged("post_install_l10n", "post_install", "-at_install")
class TestPecCheckWizard(TestItEdiPecCommon):
    def setUp(self):
        super().setUp()
        self.PEC_server = self.pec_fetch_server
        self.company.l10n_it_edi_pec_email_exchange_system = "sdi03@pec.fatturapa.it"
        self.raw_mail = self._get_test_file("POSTA CERTIFICATA_ Invio File 7339338.txt")
        self.e_invoice_name = "IT02652600210_00007.xml"
        self.wizard = self.env["pec.e_invoice.check.wizard"].create(
            {
                "fetchmail_server_id": self.PEC_server.id,
                "datetime_from": "2018-12-01 00:00:00",
                "datetime_to": "2018-12-31 23:59:59",
            }
        )

    def _get_invoice_attachment(self, company=None):
        return (
            self.env["ir.attachment"]
            .sudo()
            .search(
                [
                    ("name", "=", self.e_invoice_name),
                    ("company_id", "=", (company or self.company).id),
                    ("res_model", "=", "account.move"),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ],
                limit=1,
            )
        )

    def _patch_messages(self):
        return mock.patch.object(
            type(self.PEC_server),
            "_get_pec_messages",
            return_value=[self.raw_mail],
        )

    def test_action_check_pec_e_invoices(self):
        action = self.PEC_server.action_check_pec_e_invoices()

        self.assertEqual(action["res_model"], "pec.e_invoice.check.wizard")
        self.assertEqual(
            action["context"]["default_fetchmail_server_id"], self.PEC_server.id
        )

    def test_action_check_pec_e_invoices_not_pec(self):
        self.PEC_server.is_l10n_it_edi_pec = False

        with self.assertRaises(UserError):
            self.PEC_server.action_check_pec_e_invoices()

    def test_action_check(self):
        with self._patch_messages():
            action = self.wizard.action_check()

        self.assertEqual(action["res_id"], self.wizard.id)
        self.assertEqual(len(self.wizard.line_ids), 1)
        line = self.wizard.line_ids
        self.assertEqual(line.file_name, self.e_invoice_name)
        self.assertTrue(line.to_import)
        self.assertFalse(line.is_einvoice_xml_found)

    def test_action_check_all_found_files(self):
        found = [
            {
                "message_id": "<message@pec.example.com>",
                "subject": "Subject",
                "date": "2018-12-08 11:26:18",
                "email_from": "sdi@pec.fatturapa.it",
                "file_name": "IT01234567890_00001.xml",
                "is_einvoice_xml_found": False,
            },
            {
                "message_id": "<message@pec.example.com>",
                "subject": "Subject",
                "date": "2018-12-08 11:26:18",
                "email_from": "sdi@pec.fatturapa.it",
                "file_name": "IT01234567890_00002.xml",
                "is_einvoice_xml_found": True,
            },
        ]
        with mock.patch.object(
            type(self.PEC_server),
            "check_received_e_invoices",
            return_value=found,
        ):
            self.wizard.action_check()

        self.assertEqual(len(self.wizard.line_ids), 2)
        self.assertEqual(
            self.wizard.line_ids.mapped("file_name"),
            ["IT01234567890_00001.xml", "IT01234567890_00002.xml"],
        )
        self.assertEqual(
            self.wizard.to_import_line_ids.mapped("file_name"),
            ["IT01234567890_00001.xml"],
        )
        self.assertEqual(
            self.wizard.present_line_ids.mapped("file_name"),
            ["IT01234567890_00002.xml"],
        )
        self.assertTrue(self.wizard.to_import_line_ids.to_import)
        self.assertFalse(self.wizard.present_line_ids.to_import)
        self.wizard.to_import_line_ids.to_import = False
        self.assertFalse(
            self.wizard.line_ids.filtered(
                lambda line: not line.is_einvoice_xml_found
            ).to_import
        )

    def test_action_import_selected(self):
        with self._patch_messages():
            self.wizard.action_check()
            action = self.wizard.action_import_selected()

        self.assertEqual(action["type"], "ir.actions.act_window_close")
        self.assertFalse(self.wizard.line_ids)
        self.assertTrue(self._get_invoice_attachment())

    def test_action_import_none_selected(self):
        with self._patch_messages():
            self.wizard.action_check()
        self.wizard.line_ids.to_import = False

        with self.assertRaises(UserError):
            self.wizard.action_import_selected()

    def test_action_import_selective(self):
        with self._patch_messages():
            self.wizard.action_check()
        other_line = self.env["pec.e_invoice.check.line"].create(
            {
                "wizard_id": self.wizard.id,
                "message_id": "<other@pec.example.com>",
                "file_name": "IT01234567890_00001.xml",
                "to_import": False,
            }
        )

        with self._patch_messages():
            self.wizard.action_import_selected()

        self.assertTrue(self._get_invoice_attachment())
        self.assertEqual(self.wizard.line_ids, other_line)

    def test_check_import_uses_server_company(self):
        admin = self.env.ref("base.user_admin")
        admin_env = self.env(user=admin)
        other_company = self.company_data["company"]
        admin.sudo().write({"company_ids": [(4, other_company.id)]})
        other_server = admin_env["fetchmail.server"].create(
            {
                "name": "Other PEC server",
                "server_type": "pop",
                "is_l10n_it_edi_pec": True,
                "server": "dummy",
                "port": 110,
                "user": "dummy",
                "password": "secret",
                "state": "done",
                "e_inv_notify_partner_ids": [(6, 0, [admin.partner_id.id])],
            }
        )
        other_company.write(
            {
                "l10n_it_edi_use_pec": True,
                "l10n_it_edi_pec_fetch_server_id": other_server.id,
                "l10n_it_edi_pec_email_exchange_system": "sdi03@pec.fatturapa.it",
            }
        )
        wizard = admin_env["pec.e_invoice.check.wizard"].create(
            {
                "fetchmail_server_id": other_server.id,
                "datetime_from": "2018-12-01 00:00:00",
                "datetime_to": "2018-12-31 23:59:59",
            }
        )

        with self._patch_messages():
            wizard.action_check()

        self.assertEqual(len(wizard.line_ids), 1)
        self.assertTrue(wizard.line_ids.to_import)

        with self._patch_messages():
            wizard.action_import_selected()

        attachment = self._get_invoice_attachment(company=other_company)
        self.assertTrue(attachment)

    def test_check_server_in_other_enabled_company(self):
        """A server of another enabled company can be checked."""
        main_company = self.env.company
        other_company = self.company_data["company"]
        self.env.user.sudo().write({"company_ids": [(4, other_company.id)]})
        other_server = (
            self.env["fetchmail.server"]
            .sudo()
            .create(
                {
                    "name": "Other PEC server",
                    "server_type": "pop",
                    "is_l10n_it_edi_pec": True,
                    "server": "dummy",
                    "port": 110,
                    "user": "dummy",
                    "password": "secret",
                    "state": "done",
                }
            )
        )
        other_company.write(
            {
                "l10n_it_edi_use_pec": True,
                "l10n_it_edi_pec_fetch_server_id": other_server.id,
                "l10n_it_edi_pec_email_exchange_system": "sdi03@pec.fatturapa.it",
            }
        )
        # Keep only the main company as current company
        self.env = self.env(
            context=dict(self.env.context, allowed_company_ids=[main_company.id])
        )
        wizard = self.env["pec.e_invoice.check.wizard"].create(
            {
                "fetchmail_server_id": other_server.id,
                "datetime_from": "2018-12-01 00:00:00",
                "datetime_to": "2018-12-31 23:59:59",
            }
        )

        with self._patch_messages():
            wizard.action_check()

        self.assertEqual(len(wizard.line_ids), 1)
        self.assertFalse(wizard.line_ids.is_einvoice_xml_found)

        with self._patch_messages():
            wizard.action_import_selected()

        attachment = self._get_invoice_attachment(company=other_company)
        self.assertTrue(attachment)
