# Copyright 2026 Marco Colombo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.test_edi_reverse_charge import TestItEdiReverseCharge


@tagged("post_install", "-at_install")
class TestL10nItEdiGenerateXml(TestItEdiReverseCharge):
    """Tests for the `action_l10n_it_edi_generate_xml` flow and the
    `action_l10n_it_edi_send` override that reuses the generated XML.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The send tests require a demo-mode proxy user so the SdI call path
        # can be exercised (mocked) without a real proxy.
        cls.proxy_user.edi_mode = "demo"

    def _create_reverse_charge_bill(self, partner=None):
        """Create and post a vendor bill with an external reverse charge tax,
        turning it into an Italian self-invoice.
        """
        partner = partner or self.french_partner
        bill = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2022-03-24",
                    "invoice_date_due": "2022-03-24",
                    "date": "2022-04-01",
                    "ref": "BILL/2022/04/0001",
                    "partner_id": partner.id,
                    "partner_bank_id": self.test_bank.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Product A",
                                "product_id": self.product_a.id,
                                "price_unit": 800.40,
                                "tax_ids": [Command.set(self.purchase_tax_22p.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        bill.action_post()
        return bill

    def _edi_attachments(self, move):
        """All FatturaPA attachments linked to a move via the binary field."""
        return (
            self.env["ir.attachment"]
            .with_company(self.company)
            .search(
                [
                    ("res_model", "=", "account.move"),
                    ("res_id", "=", move.id),
                    ("res_field", "=", "l10n_it_edi_attachment_file"),
                ]
            )
        )

    # -------------------------------------------------------------------------
    # action_l10n_it_edi_generate_xml
    # -------------------------------------------------------------------------

    def test_generate_xml_creates_attachment(self):
        """Generating the XML on a valid self-invoice creates the attachment
        without sending anything to the SdI.
        """
        bill = self._create_reverse_charge_bill()
        self.assertTrue(
            bill.l10n_it_edi_is_self_invoice,
            "precondition: the bill must be recognised as a self-invoice",
        )

        result = bill.action_l10n_it_edi_generate_xml()

        # No reload action is returned on the success path.
        self.assertFalse(result)
        # The FatturaPA attachment is created.
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertEqual(
            self._edi_attachments(bill).ids, bill.l10n_it_edi_attachment_id.ids
        )
        self.assertTrue(bill.l10n_it_edi_attachment_id.raw)
        # No SdI interaction happened.
        self.assertFalse(bill.is_move_sent)
        self.assertFalse(bill.l10n_it_edi_state)
        self.assertFalse(bill.l10n_it_edi_transaction)
        # No error banner.
        self.assertFalse(bill.l10n_it_edi_header)

    def test_generate_xml_validation_error(self):
        """A self-invoice whose partner is missing both VAT and codice fiscale
        returns a reload action and an error header without creating an
        attachment.
        """
        # Make the partner invalid: no VAT, no codice fiscale -> triggers
        # `partner_vat_codice_fiscale_missing` in _l10n_it_edi_export_data_check.
        partner = self.env["res.partner"].create(
            {
                "name": "No VAT Partner",
                "country_id": self.env.ref("base.fr").id,
                "street": "Avenue Test rue",
                "zip": "84000",
                "city": "Avignon",
                "is_company": True,
            }
        )
        bill = self._create_reverse_charge_bill(partner=partner)
        self.assertTrue(bill.l10n_it_edi_is_self_invoice)

        result = bill.action_l10n_it_edi_generate_xml()

        # A reload client action is returned to refresh the header banner.
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("type"), "ir.actions.client")
        self.assertEqual(result.get("tag"), "reload")
        # The error banner is populated.
        self.assertTrue(bill.l10n_it_edi_header)
        # No attachment was created.
        self.assertFalse(bill.l10n_it_edi_attachment_id)
        self.assertEqual(self._edi_attachments(bill), self.env["ir.attachment"])
        # Nothing was sent.
        self.assertFalse(bill.is_move_sent)
        self.assertFalse(bill.l10n_it_edi_transaction)

    def test_generate_xml_does_not_send_to_sdi(self):
        """Generating the XML alone must not start any SdI transaction."""
        bill = self._create_reverse_charge_bill()
        bill.action_l10n_it_edi_generate_xml()

        self.assertFalse(bill.l10n_it_edi_transaction)
        self.assertFalse(bill.l10n_it_edi_state)
        self.assertFalse(bill.is_move_sent)
        # Sanity: the attachment exists, proving we did create it (and only it).
        self.assertTrue(bill.l10n_it_edi_attachment_id)

    def test_generate_xml_idempotent_no_duplicate(self):
        """Calling generate twice does not create a second attachment and
        takes the "already generated" branch (chatter resurface only).
        """
        bill = self._create_reverse_charge_bill()
        bill.action_l10n_it_edi_generate_xml()
        first_attachment = bill.l10n_it_edi_attachment_id
        self.assertTrue(first_attachment)

        # Second call should reuse the existing attachment, not create a new one.
        result = bill.action_l10n_it_edi_generate_xml()
        self.assertFalse(result)
        self.assertEqual(bill.l10n_it_edi_attachment_id, first_attachment)
        self.assertEqual(len(self._edi_attachments(bill)), 1)

    # -------------------------------------------------------------------------
    # action_l10n_it_edi_send override (reuse generated XML)
    # -------------------------------------------------------------------------

    def test_send_after_generate_reuses_attachment(self):
        """Generate the XML, then send: the SdI call reuses the existing
        attachment — no duplicate `ir.attachment` is created.
        """
        bill = self._create_reverse_charge_bill()
        bill.action_l10n_it_edi_generate_xml()
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        generated_attachment = bill.l10n_it_edi_attachment_id
        self.assertEqual(len(self._edi_attachments(bill)), 1)

        success = {"id_transaction": "SDI ID 1", "signed": False, "signed_data": False}
        with patch(
            "odoo.addons.l10n_it_edi.models.account_move.AccountMove._l10n_it_edi_upload_single",
            return_value=success,
        ) as mock_upload:
            result = bill.action_l10n_it_edi_send()

        # generate_xml succeeds -> send proceeds (no reload returned).
        self.assertFalse(result)
        # The SdI upload was actually invoked exactly once.
        self.assertEqual(mock_upload.call_count, 1)
        # The move is now marked as sent and in the processing state.
        self.assertTrue(bill.is_move_sent)
        self.assertEqual(bill.l10n_it_edi_state, "processing")
        self.assertEqual(bill.l10n_it_edi_transaction, success["id_transaction"])
        # Crucially: still only ONE FatturaPA attachment, the one we generated.
        self.assertEqual(bill.l10n_it_edi_attachment_id, generated_attachment)
        self.assertEqual(len(self._edi_attachments(bill)), 1)

    def test_send_without_generate_creates_attachment(self):
        """Sending directly (no prior generate) still works: generate is run
        on the fly by the override and produces exactly one attachment.
        """
        bill = self._create_reverse_charge_bill()
        success = {"id_transaction": "SDI ID 1", "signed": False, "signed_data": False}
        with patch(
            "odoo.addons.l10n_it_edi.models.account_move.AccountMove._l10n_it_edi_upload_single",
            return_value=success,
        ) as mock_upload:
            result = bill.action_l10n_it_edi_send()

        self.assertFalse(result)
        self.assertEqual(mock_upload.call_count, 1)
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(bill)), 1)
        self.assertTrue(bill.is_move_sent)
        self.assertEqual(bill.l10n_it_edi_state, "processing")

    def test_send_validation_error_returns_reload(self):
        """When the data is invalid, send delegates to generate_xml which
        returns a reload action and does NOT call the SdI.
        """
        partner = self.env["res.partner"].create(
            {
                "name": "No VAT Partner",
                "country_id": self.env.ref("base.fr").id,
                "street": "Avenue Test rue",
                "zip": "84000",
                "city": "Avignon",
                "is_company": True,
            }
        )
        bill = self._create_reverse_charge_bill(partner=partner)
        self.assertTrue(bill.l10n_it_edi_is_self_invoice)

        success = {"id_transaction": "SDI ID 1", "signed": False, "signed_data": False}
        with patch(
            "odoo.addons.l10n_it_edi.models.account_move.AccountMove._l10n_it_edi_upload_single",
            return_value=success,
        ) as mock_upload:
            result = bill.action_l10n_it_edi_send()

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("tag"), "reload")
        # No SdI call happened, nothing was sent.
        self.assertEqual(mock_upload.call_count, 0)
        self.assertFalse(bill.is_move_sent)
        self.assertFalse(bill.l10n_it_edi_attachment_id)
        self.assertTrue(bill.l10n_it_edi_header)
