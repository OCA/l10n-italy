# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


@tagged("post_install_l10n", "post_install", "-at_install")
class TestEdiRf11Export(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Company under the RF11 regime. The 74-ter "Terzo Intermediario o
        # Soggetto Emittente" block is emitted automatically with the company's
        # own data, so the global sender partner is intentionally left empty.
        cls.company.l10n_it_tax_system = "RF11"

        # The travel agency (74-ter agent) = supplier of the self-billing bill.
        cls.agency = cls.italian_partner_a
        cls.agency.is_74ter_agent = True
        # SdI destination code of the agency (private, 7 chars).
        cls.agency.l10n_it_pa_index = "ZG4QBXW"

        # 0% purchase tax carrying the N3.6 nature (art. 74-ter non-taxable).
        # Nature comes from the tax configuration, not from code.
        cls.tax_n36 = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "N3.6 74-ter",
                    "amount": 0.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                    "l10n_it_exempt_reason": "N3.6",
                    "l10n_it_law_reference": "Art. 74-ter, DPR 633/72",
                }
            )
        )

        # Intra-EU: an explicit 22% reverse-charge purchase tax carrying nature
        # N6.9. It stays at 22% for the VAT registers (both the purchase and
        # sales registers, thanks to the -100% tax repartition line); the module
        # strips the VAT in the XML and keeps the N6.9 read from the tax.
        cls.tax_22_n69 = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "22% 74-ter intra-UE (N6.9)",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                    "l10n_it_exempt_reason": "N6.9",
                    "l10n_it_law_reference": "Art. 74-ter, DPR 633/72",
                    "invoice_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100.0, "base", []),
                        cls.RepartitionLine(100.0, "tax", []),
                        cls.RepartitionLine(-100.0, "tax", []),
                    ),
                    "refund_repartition_line_ids": cls.repartition_lines(
                        cls.RepartitionLine(100.0, "base", []),
                        cls.RepartitionLine(100.0, "tax", []),
                        cls.RepartitionLine(-100.0, "tax", []),
                    ),
                }
            )
        )

        # A plain 22% purchase tax with NO nature: used to check that the module
        # falls back to N6.9 when the tax does not carry one.
        cls.tax_22_plain = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "22% 74-ter intra-UE (no nature)",
                    "amount": 22.0,
                    "amount_type": "percent",
                    "type_tax_use": "purchase",
                }
            )
        )

    def _create_74ter_bill(self, tax=None):
        bill = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "in_invoice",
                    "invoice_date": "2024-01-01",
                    "partner_id": self.agency.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Provvigione agenzia",
                                "product_id": self.product_a.id,
                                "price_unit": 100.0,
                                "tax_ids": [Command.set((tax or self.tax_n36).ids)],
                            }
                        ),
                    ],
                }
            )
        )
        bill.action_post()
        return bill

    def test_74ter_bill_is_self_invoice(self):
        """The agency bill is forced to a self-invoice (role swap + send button)."""
        bill = self._create_74ter_bill()
        self.assertTrue(bill._l10n_it_edi_is_74ter_self_billing())
        self.assertTrue(bill.l10n_it_edi_is_self_invoice)

    def test_74ter_bill_xml(self):
        bill = self._create_74ter_bill()
        tree = etree.fromstring(bill._l10n_it_edi_render_xml())

        # RegimeFiscale RF11 (core would force RF18 for a self-invoice)
        self.assertEqual(tree.findtext(".//CedentePrestatore//RegimeFiscale"), "RF11")
        # Ordinary invoice document type
        self.assertEqual(
            tree.findtext(".//DatiGeneraliDocumento/TipoDocumento"), "TD01"
        )
        # Emitted by the Cessionario/Committente (the tour operator)
        self.assertEqual(tree.findtext(".//SoggettoEmittente"), "CC")
        # The issuer block carries the company (tour operator), emitted
        # automatically without a global sender partner.
        self.assertEqual(
            tree.findtext(
                ".//TerzoIntermediarioOSoggettoEmittente//IdFiscaleIVA/IdCodice"
            ),
            "01234560157",
        )
        # Seller (CedentePrestatore) is the agency
        self.assertEqual(
            tree.findtext(".//CedentePrestatore//IdFiscaleIVA/IdCodice"),
            "00465840031",
        )
        # CodiceDestinatario is the agency's SdI code (v16 behaviour), not the
        # company's own.
        self.assertEqual(
            tree.findtext(".//DatiTrasmissione/CodiceDestinatario"), "ZG4QBXW"
        )
        # Extra-EU / non-taxable: Natura N3.6 from the tax config, tax 0
        self.assertEqual(tree.findtext(".//DatiRiepilogo/Natura"), "N3.6")
        self.assertEqual(tree.findtext(".//DatiRiepilogo/Imposta"), "0.00")
        # ImportoTotaleDocumento omitted
        self.assertIsNone(tree.find(".//ImportoTotaleDocumento"))

    def test_74ter_bill_intra_eu_n69(self):
        """Intra-EU: an explicit 22% reverse-charge tax carrying N6.9 is kept in
        the accounting but exported without VAT and with nature N6.9."""
        bill = self._create_74ter_bill(tax=self.tax_22_n69)

        # Accounting: the reverse-charge tax books into both VAT registers, so
        # the two tax lines net to zero (the 22% stays out of the XML only).
        tax_lines = bill.line_ids.filtered("tax_line_id")
        self.assertEqual(len(tax_lines), 2)
        self.assertEqual(sum(tax_lines.mapped("balance")), 0.0)

        tree = etree.fromstring(bill._l10n_it_edi_render_xml())

        # DatiRiepilogo: VAT stripped, nature N6.9 (from the tax config)
        self.assertEqual(tree.findtext(".//DatiRiepilogo/Natura"), "N6.9")
        self.assertEqual(tree.findtext(".//DatiRiepilogo/AliquotaIVA"), "0.00")
        self.assertEqual(tree.findtext(".//DatiRiepilogo/Imposta"), "0.00")
        # DettaglioLinee: aliquota 0 and nature N6.9
        self.assertEqual(tree.findtext(".//DettaglioLinee/AliquotaIVA"), "0.00")
        self.assertEqual(tree.findtext(".//DettaglioLinee/Natura"), "N6.9")
        # No total, as for the extra-EU case
        self.assertIsNone(tree.find(".//ImportoTotaleDocumento"))

    def test_74ter_bill_intra_eu_natura_fallback(self):
        """A 22% line whose tax carries no nature falls back to N6.9."""
        bill = self._create_74ter_bill(tax=self.tax_22_plain)
        tree = etree.fromstring(bill._l10n_it_edi_render_xml())

        self.assertEqual(tree.findtext(".//DatiRiepilogo/Natura"), "N6.9")
        self.assertEqual(tree.findtext(".//DatiRiepilogo/AliquotaIVA"), "0.00")
        self.assertEqual(tree.findtext(".//DettaglioLinee/Natura"), "N6.9")

    def test_normal_invoice_unaffected(self):
        """The overrides are inert for an ordinary customer invoice."""
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": "2024-01-01",
                    "partner_id": self.agency.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "Product A",
                                "product_id": self.product_a.id,
                                "price_unit": 100.0,
                                "tax_ids": [Command.set(self.default_tax.ids)],
                            }
                        ),
                    ],
                }
            )
        )
        invoice.action_post()
        self.assertFalse(invoice._l10n_it_edi_is_74ter_self_billing())

        tree = etree.fromstring(invoice._l10n_it_edi_render_xml())
        # No global sender partner -> no issuer block, no SoggettoEmittente,
        # and the total is present as usual.
        self.assertIsNone(tree.find(".//SoggettoEmittente"))
        self.assertIsNone(tree.find(".//TerzoIntermediarioOSoggettoEmittente"))
        self.assertIsNotNone(tree.find(".//ImportoTotaleDocumento"))
