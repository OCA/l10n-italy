# Copyright 2026 STeSI Consulting
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta

from odoo import Command, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestPlafondFixes(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.write(
            {
                "country_id": cls.env.ref("base.it").id,
                "account_fiscal_country_id": cls.env.ref("base.it").id,
            }
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "DOI Partner",
                "country_id": cls.env.ref("base.it").id,
            }
        )
        cls.product = cls.env["product.product"].create({"name": "DOI Product"})
        tax_group = cls.env["account.tax.group"].create({"name": "DOI group"})

        def tax(name, amount, use):
            return cls.env["account.tax"].create(
                {
                    "name": name,
                    "amount": amount,
                    "type_tax_use": use,
                    "tax_group_id": tax_group.id,
                    "l10n_it_exempt_reason": "N3.5" if not amount else False,
                    "l10n_it_law_reference": "Art. 8" if not amount else False,
                }
            )

        cls.sale_doi_tax = tax("0% DOI sale", 0, "sale")
        cls.sale_vat_tax = tax("22% sale", 22, "sale")
        cls.bill_doi_tax = tax("0% DOI purchase", 0, "purchase")
        cls.bill_extra_tax = tax("4% purchase", 4, "purchase")
        cls.company.write(
            {
                "l10n_it_edi_doi_tax_id": cls.sale_doi_tax.id,
                "l10n_it_edi_doi_bill_tax_id": cls.bill_doi_tax.id,
            }
        )
        cls.doi_out = cls._create_declaration("out", "1", threshold=5000)
        cls.doi_out_2 = cls._create_declaration("out", "2", threshold=5000)
        cls.doi_in = cls._create_declaration("in", "3", threshold=5000)

    @classmethod
    def _create_declaration(cls, doi_type, protocol, threshold, partner=None):
        today = fields.Date.today()
        return cls.env["l10n_it_edi_doi.declaration_of_intent"].create(
            {
                "partner_id": (partner or cls.partner).id,
                "company_id": cls.company.id,
                "state": "active",
                "type": doi_type,
                "currency_id": cls.company.currency_id.id,
                "issue_date": today,
                "start_date": today,
                "end_date": today + relativedelta(months=2),
                "threshold": threshold,
                "protocol_number_part1": protocol,
                "protocol_number_part2": protocol,
            }
        )

    def _create_invoice(self, taxes, move_type="out_invoice", price=900.0):
        return self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner.id,
                "invoice_date": fields.Date.today(),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "quantity": 1,
                            "price_unit": price,
                            "tax_ids": [Command.set(taxes.ids)],
                        }
                    )
                ],
            }
        )

    def _reverse(self, invoice):
        wizard = (
            self.env["account.move.reversal"]
            .with_context(
                active_model="account.move",
                active_ids=invoice.ids,
            )
            .create({"journal_id": invoice.journal_id.id, "reason": "test"})
        )
        return self.env["account.move"].browse(wizard.reverse_moves()["res_id"])

    def _add_link(self, invoice, declaration, amount):
        return self.env["account.move.doi"].create(
            {
                "move_id": invoice.id,
                "declaration_id": declaration.id,
                "amount": amount,
            }
        )

    # 01: sale credit note lowers the plafond
    def test_01_sale_credit_note_lowers_invoiced(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_out)
        invoice.action_post()
        self.assertEqual(self.doi_out.invoiced, 900.0)
        refund = self._reverse(invoice)
        self.assertEqual(refund.l10n_it_edi_doi_id, self.doi_out)
        self.assertEqual(refund.l10n_it_edi_doi_amount, -900.0)
        refund.action_post()
        self.assertEqual(self.doi_out.invoiced, 0.0)

    # 02: a fully taxed invoice does not consume the plafond
    def test_02_vat_invoice_does_not_consume_plafond(self):
        invoice = self._create_invoice(self.sale_vat_tax)
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_out)
        self.assertEqual(invoice.l10n_it_edi_doi_amount, 0.0)
        invoice.action_post()
        self.assertEqual(self.doi_out.invoiced, 0.0)

    # 03: extra taxes on the DOI line do not inflate the amount
    def test_03_purchase_amount_uses_taxable_base(self):
        bill = self._create_invoice(
            self.bill_doi_tax | self.bill_extra_tax, "in_invoice"
        )
        self.assertEqual(bill.l10n_it_edi_doi_id, self.doi_in)
        self.assertEqual(bill.l10n_it_edi_doi_amount, 900.0)
        bill.action_post()
        self.assertEqual(self.doi_in.invoiced, 900.0)
        refund = self._reverse(bill)
        refund.action_post()
        self.assertEqual(self.doi_in.invoiced, 0.0)

    # 04 + 06: core threshold warning is back, no coverage banner without bridge rows
    def test_04_06_threshold_warning_without_coverage_banner(self):
        invoice = self._create_invoice(self.sale_doi_tax, price=6000.0)
        self.assertIn("exceeded", invoice.l10n_it_edi_doi_warning)
        self.assertNotIn("covered by declarations", invoice.l10n_it_edi_doi_warning)
        small = self._create_invoice(self.sale_doi_tax)
        self.assertFalse(small.l10n_it_edi_doi_warning)
        self._add_link(small, self.doi_out, 100.0)
        small.invalidate_recordset(["l10n_it_edi_doi_warning"])
        self.assertIn("covered by declarations", small.l10n_it_edi_doi_warning)

    # 05: draft invoices never count, bridge rows or not
    def test_05_draft_not_counted(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        invoice.name = "INV/TEST/0001"
        self._add_link(invoice, self.doi_out, 900.0)
        self.assertEqual(self.doi_out.invoiced, 0.0)
        invoice.action_post()
        self.assertEqual(self.doi_out.invoiced, 900.0)

    # 07: bridge rows are locked once the invoice is posted
    def test_07_posted_invoice_rows_locked(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        link = self._add_link(invoice, self.doi_out, 900.0)
        invoice.action_post()
        with self.assertRaises(UserError):
            link.unlink()
        with self.assertRaises(UserError):
            link.write({"amount": 1.0})
        with self.assertRaises(UserError):
            self._add_link(invoice, self.doi_out_2, 1.0)
        link.write({"sequence": 5})
        self.assertEqual(invoice.l10n_it_edi_doi_id, self.doi_out)

    # 08: read-only accountants can read the bridge rows
    def test_08_readonly_user_reads_bridge_rows(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        self._add_link(invoice, self.doi_out, 900.0)
        auditor = self.env["res.users"].create(
            {
                "name": "Auditor",
                "login": "doi_auditor",
                "groups_id": [
                    Command.set(
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("account.group_account_readonly").id,
                        ]
                    )
                ],
            }
        )
        data = invoice.with_user(auditor).web_read(
            {
                "l10n_it_edi_doi_ids": {"fields": {"amount": {}}},
            }
        )
        self.assertEqual(data[0]["l10n_it_edi_doi_ids"][0]["amount"], 900.0)

    # 09: a duplicate follows core (no bridge lines), a credit note mirrors them
    def test_09_copy_and_reversal(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        self._add_link(invoice, self.doi_out, 500.0)
        self._add_link(invoice, self.doi_out_2, 400.0)
        copy = invoice.copy()
        self.assertFalse(copy.l10n_it_edi_doi_ids)
        self.assertEqual(copy.l10n_it_edi_doi_id, self.doi_out)
        invoice.action_post()
        refund = self._reverse(invoice)
        self.assertRecordValues(
            refund.l10n_it_edi_doi_ids,
            [
                {"declaration_id": self.doi_out.id, "amount": 500.0},
                {"declaration_id": self.doi_out_2.id, "amount": 400.0},
            ],
        )

    # 10: a zero amount is rejected
    def test_10_zero_amount_rejected(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        with self.assertRaises(ValidationError):
            self._add_link(invoice, self.doi_out, 0.0)

    # 11: every order in a multi-record check gets validated
    def test_11_purchase_constraint_checks_all_orders(self):
        # purchase.order.create runs one record at a time, so the constraint
        # is exercised directly on a two-record set: the first order has no
        # declaration, the second one holds a declaration that turned invalid.
        other = self.env["res.partner"].create({"name": "No DOI Partner"})
        line = {
            "product_id": self.product.id,
            "product_qty": 1,
            "price_unit": 100.0,
            "taxes_id": [Command.set(self.bill_doi_tax.ids)],
        }
        orders = self.env["purchase.order"].create(
            [
                {"partner_id": other.id, "order_line": [Command.create(line)]},
                {"partner_id": self.partner.id, "order_line": [Command.create(line)]},
            ]
        )
        self.assertFalse(orders[0].l10n_it_edi_doi_id)
        self.assertEqual(orders[1].l10n_it_edi_doi_id, self.doi_in)
        self.doi_in.partner_id = other
        with self.assertRaises(ValidationError):
            orders._check_l10n_it_edi_doi_id()

    # 12: cancelled orders show no warning
    def test_12_cancelled_order_no_warning(self):
        order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_qty": 1,
                            "price_unit": 9000.0,
                            "taxes_id": [Command.set(self.bill_doi_tax.ids)],
                        }
                    )
                ],
            }
        )
        self.assertEqual(order.l10n_it_edi_doi_id, self.doi_in)
        self.assertIn("exceeded", order.l10n_it_edi_doi_warning)
        order.button_cancel()
        self.assertFalse(order.l10n_it_edi_doi_warning)

    # migrated rows with amount 0 do not hide the invoice and stay editable
    def test_13_migrated_zero_amount_row(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        invoice.action_post()
        self.assertEqual(self.doi_out.invoiced, 900.0)
        self.env.cr.execute(
            """
            INSERT INTO account_move_doi
                (move_id, declaration_id, amount, sequence, currency_id, company_id)
            VALUES (%s, %s, 0, 10, %s, %s)
            """,
            (
                invoice.id,
                self.doi_out.id,
                invoice.currency_id.id,
                invoice.company_id.id,
            ),
        )
        self.env.invalidate_all()
        self.doi_out._compute_invoiced()
        self.assertEqual(self.doi_out.invoiced, 900.0)
        row = invoice.l10n_it_edi_doi_ids
        row.amount = 900.0
        self.assertEqual(self.doi_out.invoiced, 900.0)
        with self.assertRaises(UserError):
            row.unlink()

    # credit notes keep the rows even when the declaration was terminated since
    def test_14_credit_note_on_terminated_declaration(self):
        invoice = self._create_invoice(self.sale_doi_tax)
        self._add_link(invoice, self.doi_out, 500.0)
        self._add_link(invoice, self.doi_out_2, 400.0)
        invoice.action_post()
        self.assertEqual(self.doi_out.invoiced, 500.0)
        self.doi_out.action_terminate()
        refund = self._reverse(invoice)
        self.assertEqual(refund.l10n_it_edi_doi_id, self.doi_out)
        self.assertEqual(len(refund.l10n_it_edi_doi_ids), 2)
        refund.action_post()
        self.assertEqual(self.doi_out.invoiced, 0.0)
        self.assertEqual(self.doi_out_2.invoiced, 0.0)
