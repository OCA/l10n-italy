# Copyright 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
# Copyright 2017 Diego Bruselli <d.bruselli@creativiquadrati.it>
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tests import Form, tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestBillOfEntry(AccountTestInvoicingCommon):
    def _create_invoice(
        self, partner, customs_doc_type, journal, products_list, notes_sections_list
    ):
        invoice = self.init_invoice(
            "in_invoice",
            partner=partner,
            journal=journal,
        )
        invoice_form = Form(invoice)
        if customs_doc_type:
            invoice_form.customs_doc_type = customs_doc_type
        for product, qty, price in products_list:
            with invoice_form.invoice_line_ids.new() as line:
                line.name = product.name
                line.product_id = product
                line.price_unit = price
                line.quantity = qty
        for name, display_type in notes_sections_list:
            with invoice_form.invoice_line_ids.new() as line:
                line.name = name
                line.display_type = display_type

        invoice = invoice_form.save()
        return invoice

    def setUp(self):
        super().setUp()

        self.account_model = self.env["account.account"]
        self.tax_model = self.env["account.tax"]
        self.tax_group_model = self.env["account.tax.group"]
        self.journal_model = self.env["account.journal"]
        self.invoice_model = self.env["account.move"]
        self.inv_line_model = self.env["account.move.line"]
        self.move_line_model = self.env["account.move.line"]
        self.fp_model = self.env["account.fiscal.position"]
        self.pp_model = self.env["product.product"]
        self.partner_model = self.env["res.partner"]

        self.data_it_company = self.setup_other_company(
            name="IT Company",
            vat="IT01234560157",
            phone="0266766700",
            email="test@test.it",
            street="1234 Test Street",
            zip="12345",
            city="Prova",
            l10n_it_codice_fiscale="01234560157",
            l10n_it_tax_system="RF01",
        )
        self.it_company = self.data_it_company["company"]
        self.env.user.company_ids |= self.it_company
        self.env.user.company_id = self.it_company
        # Now that current user can access the company,
        # log the user *only* in this company so that
        # searching, reading and other operations behave as expected
        self.env.user.company_ids = self.it_company

        # Default accounts for invoice line account_id
        self.account_revenue = self.account_model.search(
            [("account_type", "=", "income")], limit=1
        )
        # Default purchase journal
        self.journal = self.journal_model.search([("type", "=", "purchase")], limit=1)
        # Extra EU purchase journal for differentiate
        # extra EU purchase invoices from ordinary ones
        self.extra_journal = self.journal_model.search([("code", "=", "NOUE")], limit=1)
        # Bill of entry storno journal
        self.bill_of_entry_journal = self.journal_model.create(
            {
                "name": "bill_of_entry_journal",
                "type": "general",
                "code": "BOE",
            }
        )
        self.it_company.bill_of_entry_journal_id = self.bill_of_entry_journal.id

        self.tax_group_iva_22 = self.tax_group_model.create(
            {
                "name": "IVA 22%",
                "preceding_subtotal": "Imponibile",
            }
        )

        # Extra EU fiscal position tax correspondence
        self.tax22 = self.tax_model.create(
            {
                "name": "22%",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "tax_group_id": self.tax_group_iva_22.id,
            }
        )
        self.fiscpos_extra = self.fp_model.create(
            {
                "name": "Extra EU",
            }
        )

        # Delivery Expense account
        self.account_delivery_expense = self.account_model.create(
            {
                "code": "420101",
                "name": "Delivery Expenses",
                "account_type": "expense",
                "reconcile": True,
            }
        )

        # Extra EU purchase journal
        self.journal_extra = self.journal_model.search([("code", "=", "NOUE")], limit=1)

        # Products
        self.product1 = self.pp_model.create(
            {
                "name": "Office Chair",
                "standard_price": 55.0,
                "list_price": 70.0,
                "type": "consu",
                "default_code": "FURN_7777",
            }
        )
        self.product1.write(
            {
                "supplier_taxes_id": [Command.set(self.tax22.ids)],
            }
        )
        self.tax_22extraUE = self.tax_model.create(
            {
                "name": "Iva al 22% ExtraUE (credito)",
                "amount": 22,
                "amount_type": "percent",
                "type_tax_use": "purchase",
                "tax_group_id": self.tax_group_iva_22.id,
                "sequence": 99,
            }
        )
        self.product_extra = self.pp_model.create(
            {
                "name": "ExtraEU Goods Purchase",
                "purchase_ok": True,
                "standard_price": 1.0,
                "list_price": 1.0,
                "type": "service",
            }
        )
        self.product_extra.supplier_taxes_id = [Command.set(self.tax_22extraUE.ids)]
        self.adv_customs_expense = self.pp_model.create(
            {
                "name": "Advance Customs Expense",
                "purchase_ok": True,
                "standard_price": 1.0,
                "list_price": 1.0,
                "type": "service",
            }
        )
        self.customs_expense = self.pp_model.create(
            {
                "name": "Customs Expense",
                "purchase_ok": True,
                "standard_price": 1.0,
                "list_price": 1.0,
                "type": "service",
            }
        )
        self.product_delivery = self.pp_model.create(
            {
                "name": "Customs Expense",
                "purchase_ok": True,
                "standard_price": 1.0,
                "list_price": 1.0,
                "type": "service",
            }
        )
        self.product_delivery.supplier_taxes_id = [Command.set(self.tax22.ids)]
        self.account_stamp_duties = self.account_model.create(
            {
                "code": "421400",
                "name": "Stamp Duties",
                "account_type": "expense",
                "reconcile": True,
            }
        )
        self.product_stamp = self.pp_model.create(
            {
                "name": "Customs Expense",
                "purchase_ok": True,
                "standard_price": 1.0,
                "list_price": 1.0,
                "property_account_expense_id": self.account_stamp_duties.id,
            }
        )

        # Partners
        self.customs = self.partner_model.create(
            {
                "name": "Customs",
                "is_company": True,
            }
        )
        self.supplier = self.env["res.partner"].create(
            {
                "name": "Wood Corner",
                "is_company": True,
                "street": "1839 Arbor Way",
                "city": "Turlock",
                "state_id": self.env.ref("base.state_us_5").id,
                "zip": "95380",
                "email": "wood.corner26@example.com",
                "phone": "(623)-853-7197",
                "vat": "US12345672",
            }
        )
        self.supplier.property_account_position_id = self.fiscpos_extra.id
        self.forwarder = self.env["res.partner"].create(
            {
                "name": "Azure Interior",
                "is_company": True,
                "street": "4557 De Silva St",
                "city": "Fremont",
                "state_id": self.env.ref("base.state_us_5").id,
                "zip": "94538",
                "email": "azure.Interior24@example.com",
                "phone": "(870)-931-0505",
                "vat": "US12345677",
            }
        )

        # Extra EU supplier invoice - draft state
        self.supplier_invoice = self._create_invoice(
            self.supplier,
            "supplier_invoice",
            self.journal_extra,
            [
                (self.product1, 1, 2500),
            ],
            [],
        )

        # Bill of Entry - draft state
        self.bill_of_entry = self._create_invoice(
            self.customs,
            "bill_of_entry",
            self.journal,
            [
                (self.product_extra, 1, 2500),
            ],
            [
                ("nota", "line_note"),
            ],
        )
        bill_of_entry_form = Form(self.bill_of_entry)
        bill_of_entry_form.supplier_invoice_ids.clear()
        bill_of_entry_form.supplier_invoice_ids.add(self.supplier_invoice)
        bill_of_entry_form.save()

        # Forwarder Invoice - draft state
        self.forwarder_invoice = self._create_invoice(
            self.forwarder,
            "forwarder_invoice",
            self.journal,
            [
                (self.product_delivery, 1, 300),
                (self.adv_customs_expense, 1, 550),
            ],
            [],
        )
        forwarder_invoice_form = Form(self.forwarder_invoice)
        with forwarder_invoice_form.invoice_line_ids.edit(1) as line:
            line.advance_customs_vat = True
            line.tax_ids.clear()
        forwarder_invoice_form.save()
        self.adv_customs_expense_line = (
            self.forwarder_invoice.invoice_line_ids.filtered("advance_customs_vat")
        )
        self.forwarder_invoice.update(
            {
                "forwarder_bill_of_entry_ids": [Command.link(self.bill_of_entry.id)],
            }
        )

        self.it_company.bill_of_entry_tax_id = (
            self.it_company.account_purchase_tax_id.copy()
        )
        self.it_company.bill_of_entry_partner_id = self.env["res.partner"].name_create(
            "Customs"
        )

    def test_generate_bill_of_entry_required_configurations(self):
        company = self.env.company
        missing_configurations_fields = [
            "bill_of_entry_tax_id",
            "bill_of_entry_partner_id",
        ]
        fields_dict = company.fields_get(
            allfields=missing_configurations_fields,
            attributes=["string"],
        )
        supplier_invoice = self.supplier_invoice
        for field_name in missing_configurations_fields:
            # Save and empty the configuration
            configuration_value = company[field_name]
            company[field_name] = False

            # Assert it is needed for generating the bill of entry
            with self.assertRaises(UserError) as ue:
                supplier_invoice.generate_bill_of_entry()
            exc_message = ue.exception.args[0]
            field_attributes = fields_dict.get(field_name)
            self.assertIn(field_attributes.get("string"), exc_message)

            # Restore the configuration
            company[field_name] = configuration_value

    def test_generate_bill_of_entry(self):
        bill_of_entry_action = self.supplier_invoice.generate_bill_of_entry()
        bill_of_entry_model = bill_of_entry_action.get("res_model")
        bill_of_entry_id = bill_of_entry_action.get("res_id")
        bill_of_entry = self.env[bill_of_entry_model].browse(bill_of_entry_id)
        self.assertTrue(bill_of_entry)
        self.assertEqual(bill_of_entry.state, "draft")

    def test_storno_create(self):
        # Validate bill of entry
        self.bill_of_entry.action_post()

        # Validate forwarder invoice
        self.forwarder_invoice.action_post()

        # Storno Bill of Entry account.move
        storno = self.forwarder_invoice.bill_of_entry_storno_id
        self.assertTrue(storno)
        self.assertEqual(storno.date, self.forwarder_invoice.invoice_date)

        # Advance Customs Expense account.move.line
        move_line_domain = [
            ("account_id", "=", self.adv_customs_expense_line.account_id.id),
            ("debit", "=", 0.0),
            ("credit", "=", self.adv_customs_expense_line.price_subtotal),
            ("partner_id", "=", self.adv_customs_expense_line.partner_id.id),
            ("product_id", "=", self.adv_customs_expense_line.product_id.id),
        ]
        adv_customs_expense_moveline = self.move_line_model.search(move_line_domain)
        self.assertEqual(len(adv_customs_expense_moveline), 1)

        # Customs Expense account.move.lines
        boe_payable_lines = self.bill_of_entry.line_ids.filtered(
            lambda line: line.account_type == "liability_payable"
        )
        boe_payable_line = next(iter(boe_payable_lines), boe_payable_lines)
        boe_account = boe_payable_line.account_id
        move_line_domain = [
            ("account_id", "=", boe_account.id),
            ("debit", "=", self.bill_of_entry.amount_total),
            ("credit", "=", 0.0),
            ("partner_id", "=", self.bill_of_entry.partner_id.id),
        ]
        customs_expense_moveline = self.move_line_model.search(move_line_domain)
        self.assertEqual(len(customs_expense_moveline), 1)

        # Extra EU goods purchase account.move.lines
        for boe_line in self.bill_of_entry.invoice_line_ids:
            move_line_domain = [
                ("account_id", "=", boe_line.account_id.id),
                ("debit", "=", 0.0),
                ("credit", "=", boe_line.price_subtotal),
                ("partner_id", "=", boe_line.partner_id.id),
                ("product_id", "=", boe_line.product_id.id),
            ]
            extraeu_expense_moveline = self.move_line_model.search(move_line_domain)
            self.assertEqual(len(extraeu_expense_moveline), 1)

        # Storno - BoE reconciliation (supplier debit account)
        storno_reconcile_ids = (
            storno.line_ids.filtered(lambda line: line.full_reconcile_id)
            .mapped("full_reconcile_id")
            .ids
        )
        boe_reconcile_ids = (
            self.bill_of_entry.line_ids.filtered(lambda line: line.full_reconcile_id)
            .mapped("full_reconcile_id")
            .ids
        )
        self.assertEqual(sorted(storno_reconcile_ids), sorted(boe_reconcile_ids))
