# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi

OLD_N1_REFERENCE = "Art. 15 DPR 633/1972"
NEW_N1_REFERENCE = "Art. 29, c. 1, D.Lgs. 10/2026"


@tagged("post_install_l10n", "post_install", "-at_install")
class TestTuIvaReference(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chart = cls.env["account.chart.template"].with_company(cls.company)
        # N1 and N2.2 sale taxes of the Italian chart: the first one ships a
        # D.P.R. 633/1972 reference found in TU_IVA_REFERENCES, the second one
        # a wording only found in LEGACY_REFERENCES.
        cls.tax_n1 = chart.ref("00v")
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

    def test_reference_before_2027(self):
        """An invoice dated 2026 keeps citing the D.P.R. 633/1972."""
        invoice = self._create_invoice("2026-12-31", self.tax_n1)
        self.assertEqual(self._get_references(invoice), [OLD_N1_REFERENCE])

    def test_reference_from_2027(self):
        """An invoice dated 2027 cites the Testo Unico IVA."""
        invoice = self._create_invoice("2027-01-01", self.tax_n1)
        self.assertEqual(self._get_references(invoice), [NEW_N1_REFERENCE])

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

    def test_reference_of_unmapped_code(self):
        """The N2.2 tax of the chart is updated through its current wording."""
        invoice = self._create_invoice("2027-01-15", self.tax_n22)
        self.assertEqual(self._get_references(invoice), ["Art. 150, D.Lgs. 10/2026"])

    def test_custom_reference_preserved(self):
        """A custom wording found in neither map is left untouched."""
        invoice = self._create_invoice("2027-01-15", self._create_custom_tax())
        self.assertEqual(self._get_references(invoice), ["Custom reference"])

    def test_user_reference_from_2027(self):
        """A tax created by the user cites the reference set on it."""
        tax = self._create_custom_tax(
            l10n_it_tu_iva_law_reference="Art. 22, D.Lgs. 10/2026"
        )
        invoice = self._create_invoice("2027-01-15", tax)
        self.assertEqual(self._get_references(invoice), ["Art. 22, D.Lgs. 10/2026"])
        self.assertIn("Art. 22, D.Lgs. 10/2026", invoice.taxes_legal_notes)

    def test_user_reference_before_2027(self):
        """The reference set on the tax is not used before 2027."""
        tax = self._create_custom_tax(
            l10n_it_law_reference="Art. 15 DPR 633/1972",
            l10n_it_tu_iva_law_reference="Art. 22, D.Lgs. 10/2026",
        )
        invoice = self._create_invoice("2026-12-31", tax)
        self.assertEqual(self._get_references(invoice), ["Art. 15 DPR 633/1972"])
        self.assertNotIn("Art. 22, D.Lgs. 10/2026", invoice.taxes_legal_notes or "")

    def test_user_reference_overrides_automatic_wording(self):
        """The reference set on the tax wins over the automatic wording."""
        self.tax_n1.l10n_it_tu_iva_law_reference = "Art. 29, c. 2, D.Lgs. 10/2026"
        invoice = self._create_invoice("2027-01-15", self.tax_n1)
        self.assertEqual(
            self._get_references(invoice), ["Art. 29, c. 2, D.Lgs. 10/2026"]
        )

    def test_user_references_are_not_merged(self):
        """Taxes with the same Natura and different references stay apart."""
        tax_a = self._create_custom_tax(
            l10n_it_tu_iva_law_reference="Art. 22, D.Lgs. 10/2026"
        )
        tax_b = self._create_custom_tax(
            name="VAT 0% custom 2",
            l10n_it_tu_iva_law_reference="Art. 5, c. 3, D.Lgs. 10/2026",
        )
        invoice = self._create_invoice("2027-01-15", [tax_a, tax_b])
        self.assertCountEqual(
            self._get_references(invoice),
            ["Art. 22, D.Lgs. 10/2026", "Art. 5, c. 3, D.Lgs. 10/2026"],
        )

    def test_same_user_reference_is_merged(self):
        """Taxes citing the same reference share one e-invoice summary."""
        tax_a = self._create_custom_tax(
            l10n_it_law_reference="Custom A",
            l10n_it_tu_iva_law_reference="Art. 22, D.Lgs. 10/2026",
        )
        tax_b = self._create_custom_tax(
            name="VAT 0% custom 2",
            l10n_it_law_reference="Custom B",
            l10n_it_tu_iva_law_reference="Art. 22, D.Lgs. 10/2026",
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

    def test_user_reference_must_be_latin1(self):
        """A reference the e-invoice cannot contain is refused."""
        with self.assertRaises(ValidationError):
            self._create_custom_tax(
                l10n_it_tu_iva_law_reference="Art. 22 \u2013 D.Lgs. 10/2026"
            )
        # A reference the e-invoice can contain is accepted.
        tax = self._create_custom_tax(l10n_it_tu_iva_law_reference="Art. 22 \u00e8")
        self.assertEqual(tax.l10n_it_tu_iva_law_reference, "Art. 22 \u00e8")
