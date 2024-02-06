#  Copyright 2024 Roberto Fichera - Level Prime Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestFatturapaSale(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test partner"})
        self.product = self.env["product.product"].create({"name": "Test product"})

    def _create_contract(self):
        contract = (
            self.env["contract.contract"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "name": "Test Contract",
                    "contract_type": "sale",
                    "partner_id": self.partner.id,
                    "invoice_partner_id": self.partner.id,
                    "commercial_partner_id": self.partner.id,
                    "related_documents": [
                        (
                            0,
                            0,
                            {
                                "type": "order",
                                "name": "order1",
                                "code": "code1",
                                "cig": "cig1",
                                "cup": "cup1",
                            },
                        )
                    ],
                    "date_start": "2024-01-02",
                    "line_recurrence": True,
                }
            )
        )
        contract_line = (
            self.env["contract.line"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "name": self.product.name,
                    "contract_id": contract.id,
                    "product_id": self.product.id,
                    "quantity": 1,
                    "price_unit": 1.0,
                    "admin_ref": "line admin ref",
                    "related_documents": [
                        (
                            0,
                            0,
                            {
                                "type": "order",
                                "name": "line1",
                                "code": "code1",
                                "cig": "cig1",
                                "cup": "cup1",
                            },
                        )
                    ],
                }
            )
        )
        return contract_line, contract

    def test_create_invoice(self):
        """
        Generate an invoice from a contract.
        Check that related documents are passed
        from the contract (and its lines) to the invoice (and its lines).
        """
        contract_line, contract = self._create_contract()

        # Check the invoice
        invoice = contract.recurring_create_invoice()
        self.assertEqual(len(invoice), 1, "Multiple invoices for contract")
        self.assertNotEqual(
            invoice.related_documents,
            contract.related_documents,
            "Invoice and Contract documents line must be the same",
        )
        self.assertEqual(
            invoice.related_documents[0].type, contract.related_documents[0].type
        )
        self.assertEqual(
            invoice.related_documents[0].name, contract.related_documents[0].name
        )
        self.assertEqual(
            invoice.related_documents[0].code, contract.related_documents[0].code
        )
        self.assertEqual(
            invoice.related_documents[0].cig, contract.related_documents[0].cig
        )
        self.assertEqual(
            invoice.related_documents[0].cup, contract.related_documents[0].cup
        )

        invoice_line = invoice.invoice_line_ids
        self.assertEqual(
            len(invoice_line), 1, "Multiple invoice lines for contract line"
        )

        self.assertEqual(invoice_line.admin_ref, contract_line.admin_ref)
        self.assertEqual(
            invoice_line.related_documents[0].type,
            contract_line.related_documents[0].type,
        )
        self.assertEqual(
            invoice_line.related_documents[0].name,
            contract_line.related_documents[0].name,
        )
        self.assertEqual(
            invoice_line.related_documents[0].code,
            contract_line.related_documents[0].code,
        )
        self.assertEqual(
            invoice_line.related_documents[0].cig,
            contract_line.related_documents[0].cig,
        )
        self.assertEqual(
            invoice_line.related_documents[0].cup,
            contract_line.related_documents[0].cup,
        )
