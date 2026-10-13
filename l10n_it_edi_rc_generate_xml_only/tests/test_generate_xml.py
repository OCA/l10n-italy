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

    # See the note above _create_customer_invoice on why the inherited
    # AccountTestInvoicingCommon._create_invoice() helper is not used.
    def _create_reverse_charge_bill(self, partner=None, post=True):
        """Create a vendor bill with an external reverse charge tax, turning it
        into an Italian self-invoice, and post it unless ``post=False`` is
        passed.
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
        if post:
            bill.action_post()
        return bill

    # The inherited AccountTestInvoicingCommon._create_invoice() is deliberately
    # not used: it creates the invoice on the default company with partner_a,
    # the default product/tax lines and no bank account, while these tests need
    # the Italian company, partner and tax plus a bank account. It would have to
    # be overridden on 5-6 inputs, the company being settable only through a
    # company_id create value (core TestItEdiReverseCharge does the same inline).
    def _create_customer_invoice(self, partner=None):
        """Create and post a regular customer invoice (sale journal) with a
        standard Italian sale tax.
        """
        partner = partner or self.italian_partner_a
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2022-03-24",
                    "invoice_date_due": "2022-03-24",
                    "date": "2022-04-01",
                    "ref": "INV/2022/04/0001",
                    "partner_id": partner.id,
                    "partner_bank_id": self.test_bank.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Product A",
                                "product_id": self.product_a.id,
                                "price_unit": 800.40,
                                "tax_ids": [Command.set(self.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        return invoice

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

    def _chatter_messages(self, move):
        """All chatter messages posted on a move."""
        return self.env["mail.message"].search(
            [
                ("model", "=", "account.move"),
                ("res_id", "=", move.id),
            ]
        )

    # -------------------------------------------------------------------------
    # action_l10n_it_edi_generate_xml (single record)
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

    def test_generate_xml_regular_customer_invoice(self):
        """Generating the XML on a regular customer invoice (sale journal)
        creates the attachment without sending anything to the SdI.
        """
        invoice = self._create_customer_invoice()
        self.assertFalse(
            invoice.l10n_it_edi_is_self_invoice,
            "precondition: a regular customer invoice is not a self-invoice",
        )

        result = invoice.action_l10n_it_edi_generate_xml()

        self.assertFalse(result)
        self.assertTrue(invoice.l10n_it_edi_attachment_id)
        self.assertEqual(
            self._edi_attachments(invoice).ids, invoice.l10n_it_edi_attachment_id.ids
        )
        self.assertTrue(invoice.l10n_it_edi_attachment_id.raw)
        self.assertFalse(invoice.is_move_sent)
        self.assertFalse(invoice.l10n_it_edi_state)
        self.assertFalse(invoice.l10n_it_edi_header)

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
    # action_l10n_it_edi_generate_xml (batch / list view)
    # -------------------------------------------------------------------------

    def test_generate_xml_batch_mixed(self):
        """Batch over a regular customer invoice and a self-invoice: both get
        attachments, a chatter message is posted per move, and since there is
        no failure and no skip the method returns falsy (no notification).
        """
        invoice = self._create_customer_invoice()
        bill = self._create_reverse_charge_bill()
        before_invoice = len(self._chatter_messages(invoice))
        before_bill = len(self._chatter_messages(bill))

        result = (invoice | bill).action_l10n_it_edi_generate_xml()

        self.assertFalse(result)
        self.assertTrue(invoice.l10n_it_edi_attachment_id)
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(invoice)), 1)
        self.assertEqual(len(self._edi_attachments(bill)), 1)
        # A chatter message is posted for each generated move.
        self.assertEqual(len(self._chatter_messages(invoice)), before_invoice + 1)
        self.assertEqual(len(self._chatter_messages(bill)), before_bill + 1)
        # Nothing was sent to the SdI.
        self.assertFalse(invoice.is_move_sent)
        self.assertFalse(bill.is_move_sent)
        self.assertFalse(invoice.l10n_it_edi_state)
        self.assertFalse(bill.l10n_it_edi_state)

    def test_generate_xml_batch_skips_existing_attachment(self):
        """Batch with one move already having an attachment: it is not
        regenerated (attachment unchanged), the other is generated, and a
        notification reports the skipped move.
        """
        bill = self._create_reverse_charge_bill()
        bill.action_l10n_it_edi_generate_xml()
        existing_attachment = bill.l10n_it_edi_attachment_id
        self.assertTrue(existing_attachment)

        invoice = self._create_customer_invoice()

        result = (bill | invoice).action_l10n_it_edi_generate_xml()

        # A notification is returned (truthy) mentioning the skipped move.
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("tag"), "display_notification")
        self.assertEqual(result["params"]["type"], "success")
        # The notification message is plain text, not HTML/Markup.
        self.assertIs(type(result["params"]["message"]), str)
        self.assertIn("already had an attachment", result["params"]["message"])
        # The already-generated move kept its original attachment (no duplicate).
        self.assertEqual(bill.l10n_it_edi_attachment_id, existing_attachment)
        self.assertEqual(len(self._edi_attachments(bill)), 1)
        # The other move was generated.
        self.assertTrue(invoice.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(invoice)), 1)

    def test_generate_xml_batch_skips_ineligible_draft(self):
        """Batch with a draft (ineligible) move: the eligible one is still
        generated, the draft is skipped, and a notification reports it.
        """
        draft = self._create_reverse_charge_bill(post=False)
        self.assertEqual(draft.state, "draft")

        bill = self._create_reverse_charge_bill()

        result = (draft | bill).action_l10n_it_edi_generate_xml()

        # A notification is returned (truthy) mentioning the skipped move.
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("tag"), "display_notification")
        self.assertEqual(result["params"]["type"], "success")
        # The notification message is plain text, not HTML/Markup.
        self.assertIs(type(result["params"]["message"]), str)
        self.assertIn("not eligible", result["params"]["message"])
        # The draft was skipped: no attachment.
        self.assertFalse(draft.l10n_it_edi_attachment_id)
        self.assertEqual(self._edi_attachments(draft), self.env["ir.attachment"])
        # The eligible move was generated.
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(bill)), 1)

    def test_generate_xml_batch_skips_edi_waiting_state(self):
        """Batch with a move in a waiting/non-recoverable EDI state (e.g.
        'being_sent') is skipped as ineligible, while the eligible move is
        still generated. Note that 'rejected' is intentionally eligible, since
        a rejected XML can be regenerated and resent.
        """
        waiting = self._create_reverse_charge_bill()
        waiting.l10n_it_edi_state = "being_sent"

        bill = self._create_reverse_charge_bill()

        result = (waiting | bill).action_l10n_it_edi_generate_xml()

        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("tag"), "display_notification")
        self.assertEqual(result["params"]["type"], "success")
        # The notification message is plain text, not HTML/Markup.
        self.assertIs(type(result["params"]["message"]), str)
        self.assertIn("not eligible", result["params"]["message"])
        # The waiting-state move was skipped: no attachment.
        self.assertFalse(waiting.l10n_it_edi_attachment_id)
        self.assertEqual(self._edi_attachments(waiting), self.env["ir.attachment"])
        # The eligible move was generated.
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(bill)), 1)

    def test_generate_xml_batch_validation_error_notification(self):
        """Batch with one move failing validation: no exception is raised, the
        valid move is still generated (transaction commits), and a warning
        notification lists the failing move.
        """
        # Invalid partner -> validation failure for the self-invoice.
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
        bad_bill = self._create_reverse_charge_bill(partner=partner)
        self.assertTrue(bad_bill.l10n_it_edi_is_self_invoice)

        good_bill = self._create_reverse_charge_bill()

        result = (bad_bill | good_bill).action_l10n_it_edi_generate_xml()

        # A warning notification is returned listing the failing move.
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get("tag"), "display_notification")
        self.assertEqual(result["params"]["type"], "warning")
        # The notification message is plain text, not HTML/Markup.
        self.assertIs(type(result["params"]["message"]), str)
        self.assertIn(bad_bill.display_name, result["params"]["message"])
        # The failing line is self-describing as "<display_name>: <reason>".
        self.assertIn(f"{bad_bill.display_name}: ", result["params"]["message"])
        # The valid move was still generated (transaction commits).
        self.assertTrue(good_bill.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(good_bill)), 1)
        # The failing move got no attachment.
        self.assertFalse(bad_bill.l10n_it_edi_attachment_id)
        self.assertEqual(self._edi_attachments(bad_bill), self.env["ir.attachment"])

    def test_generate_xml_server_action(self):
        """The list-view server action is bound to account.move and running it
        on a set of moves generates the XML for all of them.
        """
        action = self.env.ref(
            "l10n_it_edi_rc_generate_xml_only.action_l10n_it_edi_generate_xml",
            raise_if_not_found=True,
        )
        self.assertEqual(action.model_id.model, "account.move")
        self.assertEqual(action.binding_model_id.model, "account.move")
        self.assertIn("list", action.binding_view_types)
        self.assertIn("form", action.binding_view_types)

        bill = self._create_reverse_charge_bill()
        invoice = self._create_customer_invoice()

        result = action.with_context(
            active_model="account.move",
            active_ids=(bill | invoice).ids,
            active_id=bill.id,
        ).run()

        # No failures and no skips -> run() returns falsy.
        self.assertFalse(result)
        self.assertTrue(bill.l10n_it_edi_attachment_id)
        self.assertTrue(invoice.l10n_it_edi_attachment_id)
        self.assertEqual(len(self._edi_attachments(bill)), 1)
        self.assertEqual(len(self._edi_attachments(invoice)), 1)

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
