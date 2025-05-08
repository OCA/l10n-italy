#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_in.tests.fatturapa_common import FatturapaCommon


class TestInvoiceRC(FatturapaCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.invoice_model = cls.env["account.move"]
        cls.invoice_line_model = cls.env["account.move.line"]
        cls.partner_model = cls.env["res.partner"]
        cls._create_account()
        cls._create_taxes()
        cls._create_journals()
        cls._create_rc_types()
        cls._create_rc_type_taxes()
        cls._create_fiscal_position()

    @classmethod
    def _create_account(cls):
        account_model = cls.env["account.account"]
        cls.account_selfinvoice = account_model.create(
            {
                "code": "295000",
                "name": "selfinvoice temporary",
                "account_type": "liability_current",
            }
        )

    @classmethod
    def _create_taxes(cls):
        tax_model = cls.env["account.tax"]
        cls.tax_22ai = tax_model.create(
            {
                "name": "Tax 22% Purchase RC ITA",
                "type_tax_use": "purchase",
                "amount": 22,
                "kind_id": cls.env.ref("l10n_it_account_tax_kind.n6_1").id,
                "sequence": 10,
            }
        )
        cls.tax_22vi = tax_model.create(
            {
                "name": "Tax 22% Sales RC ITA",
                "type_tax_use": "sale",
                "amount": 22,
                "kind_id": cls.env.ref("l10n_it_account_tax_kind.n6_1").id,
                "law_reference": "articoli 23 e 25 D.P.R. 633/1972",
                "sequence": 10,
            }
        )

    @classmethod
    def _create_journals(cls):
        journal_model = cls.env["account.journal"]
        cls.journal_selfinvoice = journal_model.create(
            {
                "name": "selfinvoice",
                "type": "sale",
                "code": "SLF",
            }
        )
        cls.journal_reconciliation = journal_model.create(
            {
                "name": "RC reconciliation",
                "type": "bank",
                "code": "SLFRC",
                "default_account_id": cls.account_selfinvoice.id,
            }
        )
        cls.journal_selfinvoice_extra = journal_model.create(
            {
                "name": "Extra Selfinvoice",
                "type": "sale",
                "code": "SLFEX",
            }
        )

    @classmethod
    def _create_rc_types(cls):
        rc_type_model = cls.env["account.rc.type"]
        cls.rc_type_ita = rc_type_model.create(
            {
                "name": "RC ITA (selfinvoice)",
                "method": "selfinvoice",
                "partner_type": "other",
                "partner_id": cls.env.ref("base.main_partner").id,
                "journal_id": cls.journal_selfinvoice.id,
                "payment_journal_id": cls.journal_reconciliation.id,
                "transitory_account_id": cls.account_selfinvoice.id,
                "e_invoice_suppliers": True,
            }
        )

    @classmethod
    def _create_rc_type_taxes(cls):
        rc_type_tax_model = cls.env["account.rc.type.tax"]
        cls.rc_type_tax_ita = rc_type_tax_model.create(
            {
                "rc_type_id": cls.rc_type_ita.id,
                "purchase_tax_id": cls.tax_22ai.id,
                "sale_tax_id": cls.tax_22vi.id,
            }
        )

    @classmethod
    def _create_fiscal_position(cls):
        model_fiscal_position = cls.env["account.fiscal.position"]
        cls.fiscal_position_rc_ita = model_fiscal_position.create(
            {"name": "RC ITA", "rc_type_id": cls.rc_type_ita.id}
        )

    def test_00_xml_import(self):
        res = self.run_wizard(
            "test0", "IT01234567890_FPR04.xml", module_name="l10n_it_fatturapa_in_rc"
        )
        # Trigger pending computations
        # as if they were done during the attachment import,
        # in the UX this happens right before going back to the client.
        # Otherwise account.move.line.rc field is computed on demand
        # and its check on the context fails.
        self.env(
            context=dict(
                active_model="fatturapa.attachment.in",
            ),
        ).flush_all()

        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[0].name, "LA DESCRIZIONE")
        self.assertEqual(invoice.invoice_line_ids[1].name, "BANCALI")
        self.assertFalse(invoice.invoice_line_ids[0].rc)
        self.assertTrue(invoice.invoice_line_ids[1].rc)
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids.name, "22% e-bill")
        self.assertEqual(
            invoice.invoice_line_ids[1].tax_ids.name,
            "Tax 22% Purchase RC ITA",
        )
        self.assertEqual(invoice.amount_total, 30.5)
        self.assertEqual(invoice.get_tax_amount_added_for_rc(), 4.4)
        self.assertEqual(invoice.amount_tax, 5.5)
        self.assertEqual(invoice.e_invoice_amount_tax, 1.1)
        invoice.action_post()
        self.assertAlmostEqual(invoice.rc_self_invoice_id.amount_total, 24.4)
        self.assertEqual(invoice.rc_self_invoice_id.amount_tax, 4.4)
        self.assertEqual(invoice.rc_self_invoice_id.amount_untaxed, 20)
        self.assertEqual(
            invoice.rc_self_invoice_id.invoice_line_ids.tax_ids.name,
            "Tax 22% Sales RC ITA",
        )

        partner = invoice.partner_id
        partner.e_invoice_detail_level = "0"
        res = self.run_wizard(
            "test1", "IT01234567890_FPR04.xml", module_name="l10n_it_fatturapa_in_rc"
        )
        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertTrue(len(invoice.invoice_line_ids) == 0)

    def test_01_xml_import(self):
        supplier = self.env["res.partner"].search([("vat", "=", "IT02780790107")])[0]
        # import lines grouped by "Tax rate"
        supplier.e_invoice_detail_level = "1"
        res = self.run_wizard(
            "test2", "IT01234567890_FPR04.xml", module_name="l10n_it_fatturapa_in_rc"
        )
        # Trigger pending computations
        # as if they were done during the attachment import,
        # in the UX this happens right before going back to the client.
        # Otherwise account.move.line.rc field is computed on demand
        # and its check on the context fails.
        self.env(
            context=dict(
                active_model="fatturapa.attachment.in",
            ),
        ).flush_all()

        invoice_id = res.get("domain")[0][2][0]
        invoice = self.invoice_model.browse(invoice_id)
        self.assertEqual(invoice.invoice_line_ids[0].name, "Riepilogo Aliquota 22.00")
        self.assertEqual(invoice.invoice_line_ids[1].name, "Riepilogo Aliquota 0.00")
        self.assertFalse(invoice.invoice_line_ids[0].rc)
        self.assertTrue(invoice.invoice_line_ids[1].rc)
        self.assertEqual(invoice.invoice_line_ids[0].tax_ids.name, "22% e-bill")
