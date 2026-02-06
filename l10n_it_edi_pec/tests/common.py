# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import Command
from odoo.tests import tagged
from odoo.tools.misc import file_path

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


@tagged("post_install_l10n", "post_install", "-at_install")
class TestItEdiPecCommon(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.pec_smtp_server = cls.env["ir.mail_server"].create(
            {
                "name": "Test PEC SMTP",
                "smtp_host": "smtp.pec.example.it",
                "is_l10n_it_edi_pec": True,
                "l10n_it_edi_pec_email_from": "test@pec.example.it",
            }
        )
        cls.pec_fetch_server = cls.env["fetchmail.server"].create(
            {
                "name": "Test PEC Fetch",
                "server_type": "imap",
                "is_l10n_it_edi_pec": True,
                "server": "imap.pec.example.it",
                "port": 993,
                "user": "test@pec.example.it",
                "password": "secret",
                "state": "done",
                "e_inv_notify_partner_ids": [
                    (6, 0, [cls.env.ref("base.user_admin").partner_id.id])
                ],
            }
        )
        cls.company.write(
            {
                "l10n_it_edi_use_pec": True,
                "l10n_it_edi_pec_server_id": cls.pec_smtp_server.id,
                "l10n_it_edi_pec_fetch_server_id": cls.pec_fetch_server.id,
                "l10n_it_edi_pec_email_exchange_system": "sdi01@pec.fatturapa.it",
            }
        )

    @classmethod
    def _get_test_file(cls, filename):
        """Load a test data file."""
        path = file_path(f"l10n_it_edi_pec/tests/data/{filename}")
        with open(path, "rb") as f:
            return f.read()

    @classmethod
    def _create_and_post_invoice(cls, partner=None):
        """Create and post a test invoice."""
        invoice = (
            cls.env["account.move"]
            .with_company(cls.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2024-01-15",
                    "partner_id": (partner or cls.italian_partner_a).id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Test Service",
                                "price_unit": 1000.00,
                                "tax_ids": [Command.set(cls.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        return invoice

    @classmethod
    def _create_sent_invoice(cls, filename, partner=None):
        """Create an invoice that looks like it was sent via PEC.

        Creates the move with an attachment matching the given filename,
        and sets the state to processing (simulating a successful PEC send).
        """
        move = (
            cls.env["account.move"]
            .with_company(cls.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2024-01-15",
                    "partner_id": (partner or cls.italian_partner_a).id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Test Service",
                                "price_unit": 1000.00,
                                "tax_ids": [Command.set(cls.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        move.action_post()
        cls.env["ir.attachment"].create(
            {
                "name": filename,
                "raw": b"<xml/>",
                "type": "binary",
                "res_model": "account.move",
                "res_id": move.id,
                "res_field": "l10n_it_edi_attachment_file",
                "company_id": cls.company.id,
            }
        )
        move.write(
            {
                "l10n_it_edi_state": "processing",
                "l10n_it_edi_transaction": f"pec_{move.id}_{filename}",
            }
        )
        return move
