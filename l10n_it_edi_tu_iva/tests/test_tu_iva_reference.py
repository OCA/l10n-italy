# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import Command
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi
from odoo.addons.l10n_it_edi_tu_iva.hooks import post_init_hook

OLD_N1_REFERENCE = "Art. 15 DPR 633/1972"
NEW_N1_REFERENCE = "Art. 29, c. 1, D.Lgs. 10/2026"
OLD_N7_REFERENCE = "Fuori dall'Unione Europea"
NEW_N7_REFERENCE = "Art. 150, D.Lgs. 10/2026"


@tagged("post_install_l10n", "post_install", "-at_install")
class TestTuIvaReference(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chart = cls.env["account.chart.template"].with_company(cls.company)
        # Sale taxes of the Italian chart: N1 ships a D.P.R. 633/1972
        # reference found in TU_IVA_REFERENCES, N7 and N2.2 ship the same
        # wording, which LEGACY_REFERENCES maps only for N7.
        cls.tax_n1 = chart.ref("00v")
        cls.tax_n7 = chart.ref("00ex7")
        cls.tax_n22 = chart.ref("00ex")

    def _create_invoice(self, invoice_date, taxes, **values):
        """Invoice with one line per tax, as the SdI requires."""
        taxes = taxes if isinstance(taxes, list | tuple) else [taxes]
        move = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "invoice_date": invoice_date,
                    "invoice_date_due": invoice_date,
                    "partner_id": self.italian_partner_a.id,
                    "invoice_line_ids": [
                        Command.create(
                            {
                                "name": "line",
                                "quantity": 1.0,
                                "price_unit": 100.0,
                                "tax_ids": [Command.set(tax.ids)],
                            }
                        )
                        for tax in taxes
                    ],
                    **values,
                }
            )
        )
        move.action_post()
        return move

    def _create_custom_tax(self, **values):
        """Tax created by the user, with a wording of its own."""
        return (
            self.env["account.tax"]
            .with_company(self.company)
            .create(
                {
                    "name": "VAT 0% custom",
                    "amount": 0.0,
                    "amount_type": "percent",
                    "type_tax_use": "sale",
                    "l10n_it_exempt_reason": "N2.2",
                    "l10n_it_law_reference": "Custom reference",
                    **values,
                }
            )
        )

    def _get_summaries(self, move):
        """Return the DatiRiepilogo nodes of the generated e-invoice."""
        tree = self._remove_all_namespaces(
            etree.fromstring(move._l10n_it_edi_render_xml())
        )
        return tree.findall(".//DatiRiepilogo")

    def _get_references(self, move):
        """Return the RiferimentoNormativo values of the generated e-invoice."""
        tree = self._remove_all_namespaces(
            etree.fromstring(move._l10n_it_edi_render_xml())
        )
        return [node.text for node in tree.iter("RiferimentoNormativo")]

    def test_chart_load_updates_the_law_reference(self):
        """The references of the Italian chart move to the Testo Unico IVA."""
        self.assertEqual(self.tax_n1.l10n_it_law_reference, NEW_N1_REFERENCE)
        self.assertEqual(self.tax_n1.l10n_it_law_reference_until_2026, OLD_N1_REFERENCE)
        self.assertEqual(self.tax_n7.l10n_it_law_reference, NEW_N7_REFERENCE)
        self.assertEqual(self.tax_n7.l10n_it_law_reference_until_2026, OLD_N7_REFERENCE)
        # N2.2 keeps its wording: its article depends on the operation.
        self.assertEqual(self.tax_n22.l10n_it_law_reference, OLD_N7_REFERENCE)
        self.assertFalse(self.tax_n22.l10n_it_law_reference_until_2026)

    def test_reference_before_2027(self):
        """A document dated 2026 cites the reference used before 2027."""
        invoice = self._create_invoice("2026-12-31", self.tax_n1)
        self.assertEqual(self._get_references(invoice), [OLD_N1_REFERENCE])
        self.assertIn(OLD_N1_REFERENCE, invoice.taxes_legal_notes)
        self.assertNotIn(NEW_N1_REFERENCE, invoice.taxes_legal_notes)

    def test_reference_from_2027(self):
        """An invoice dated 2027 cites the Testo Unico IVA."""
        invoice = self._create_invoice("2027-01-01", self.tax_n1)
        self.assertEqual(self._get_references(invoice), [NEW_N1_REFERENCE])
        self.assertIn(NEW_N1_REFERENCE, invoice.taxes_legal_notes)
        self.assertNotIn(OLD_N1_REFERENCE, invoice.taxes_legal_notes)

    def test_credit_note_follows_corrected_invoice(self):
        """A 2027 credit note for a 2026 invoice keeps the old wording."""
        invoice = self._create_invoice("2026-12-31", self.tax_n1)
        credit_note = self._create_invoice(
            "2027-02-01",
            self.tax_n1,
            move_type="out_refund",
            reversed_entry_id=invoice.id,
        )
        self.assertEqual(self._get_references(credit_note), [OLD_N1_REFERENCE])
        self.assertIn(OLD_N1_REFERENCE, credit_note.taxes_legal_notes)
        self.assertNotIn(NEW_N1_REFERENCE, credit_note.taxes_legal_notes)

    def test_fiscal_position_note(self):
        """The note of the fiscal position cites the decree of the date."""
        fiscal_position = (
            self.env["account.chart.template"].with_company(self.company).ref("intra")
        )
        invoice = self._create_invoice(
            "2026-12-31", self.tax_n1, fiscal_position_id=fiscal_position.id
        )
        self.assertIn("Article 17, Paragraph 2", invoice.l10n_it_tu_iva_note)
        invoice = self._create_invoice(
            "2027-01-15", self.tax_n1, fiscal_position_id=fiscal_position.id
        )
        self.assertIn("Article 64, Paragraph 2", invoice.l10n_it_tu_iva_note)
        self.assertNotIn("Article 17, Paragraph 2", invoice.l10n_it_tu_iva_note)

    def test_reference_of_n7_code(self):
        """The wording of the N7 tax is updated to the Testo Unico IVA."""
        invoice = self._create_invoice("2027-01-15", self.tax_n7)
        self.assertEqual(self._get_references(invoice), [NEW_N7_REFERENCE])
        invoice = self._create_invoice("2026-12-31", self.tax_n7)
        self.assertEqual(self._get_references(invoice), [OLD_N7_REFERENCE])

    def test_reference_of_unmapped_code(self):
        """The N2.2 tax keeps its wording: the user chooses the article."""
        invoice = self._create_invoice("2027-01-15", self.tax_n22)
        self.assertEqual(self._get_references(invoice), [OLD_N7_REFERENCE])

    def test_user_reference_from_2027(self):
        """The reference of a tax created by the user is used as it is."""
        tax = self._create_custom_tax(
            l10n_it_law_reference="Art. 22, D.Lgs. 10/2026",
            l10n_it_law_reference_until_2026="Custom reference",
        )
        invoice = self._create_invoice("2027-01-15", tax)
        self.assertEqual(self._get_references(invoice), ["Art. 22, D.Lgs. 10/2026"])
        invoice = self._create_invoice("2026-12-31", tax)
        self.assertEqual(self._get_references(invoice), ["Custom reference"])

    def test_user_reference_kept(self):
        """A wording the module does not know is never changed."""
        tax = self._create_custom_tax()
        invoice = self._create_invoice("2027-01-15", tax)
        self.assertEqual(self._get_references(invoice), ["Custom reference"])
        # Without a reference of its own for the previous years, the document
        # dated before 2027 cites the same wording, as the e-invoice does.
        invoice = self._create_invoice("2026-12-31", tax)
        self.assertEqual(self._get_references(invoice), ["Custom reference"])
        self.assertIn("Custom reference", invoice.taxes_legal_notes)

    def test_update_law_references(self):
        """The update keeps the previous reference and is idempotent."""
        tax = self._create_custom_tax(
            l10n_it_exempt_reason="N1",
            l10n_it_law_reference=OLD_N1_REFERENCE,
        )
        self.env["account.tax"]._l10n_it_tu_iva_update_law_references()
        self.assertEqual(tax.l10n_it_law_reference, NEW_N1_REFERENCE)
        self.assertEqual(tax.l10n_it_law_reference_until_2026, OLD_N1_REFERENCE)
        self.env["account.tax"]._l10n_it_tu_iva_update_law_references()
        self.assertEqual(tax.l10n_it_law_reference, NEW_N1_REFERENCE)
        self.assertEqual(tax.l10n_it_law_reference_until_2026, OLD_N1_REFERENCE)

    def test_post_init_hook(self):
        """The installation updates the taxes already in the database."""
        tax = self._create_custom_tax(
            l10n_it_exempt_reason="N1",
            l10n_it_law_reference=OLD_N1_REFERENCE,
        )
        post_init_hook(self.env)
        self.assertEqual(tax.l10n_it_law_reference, NEW_N1_REFERENCE)
        self.assertEqual(tax.l10n_it_law_reference_until_2026, OLD_N1_REFERENCE)

    def test_archived_tax_is_updated(self):
        """An archived tax is updated too: it can be restored from 2027."""
        tax = self._create_custom_tax(
            l10n_it_exempt_reason="N1",
            l10n_it_law_reference=OLD_N1_REFERENCE,
        )
        tax.active = False
        self.env["account.tax"]._l10n_it_tu_iva_update_law_references()
        self.assertEqual(tax.l10n_it_law_reference, NEW_N1_REFERENCE)
        self.assertEqual(tax.l10n_it_law_reference_until_2026, OLD_N1_REFERENCE)

    def test_user_references_are_not_merged(self):
        """Taxes with the same Natura and different references stay apart."""
        tax_a = self._create_custom_tax(l10n_it_law_reference="Art. 22, D.Lgs. 10/2026")
        tax_b = self._create_custom_tax(
            name="VAT 0% custom 2",
            l10n_it_law_reference="Art. 5, c. 3, D.Lgs. 10/2026",
        )
        invoice = self._create_invoice("2027-01-15", [tax_a, tax_b])
        self.assertCountEqual(
            self._get_references(invoice),
            ["Art. 22, D.Lgs. 10/2026", "Art. 5, c. 3, D.Lgs. 10/2026"],
        )

    def test_same_user_reference_is_merged(self):
        """Taxes citing the same reference share one e-invoice summary."""
        tax_a = self._create_custom_tax(
            l10n_it_law_reference="Art. 22, D.Lgs. 10/2026",
            l10n_it_law_reference_until_2026="Custom A",
        )
        tax_b = self._create_custom_tax(
            name="VAT 0% custom 2",
            l10n_it_law_reference="Art. 22, D.Lgs. 10/2026",
            l10n_it_law_reference_until_2026="Custom B",
        )
        # Before 2027 each tax keeps its own reference, so two summaries.
        invoice = self._create_invoice("2026-12-31", [tax_a, tax_b])
        self.assertEqual(len(self._get_summaries(invoice)), 2)
        # From 2027 the two taxes cite the same reference: one summary.
        invoice = self._create_invoice("2027-01-15", [tax_a, tax_b])
        summaries = self._get_summaries(invoice)
        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].findtext("ImponibileImporto"), "200.00")
        self.assertEqual(
            summaries[0].findtext("RiferimentoNormativo"),
            "Art. 22, D.Lgs. 10/2026",
        )
