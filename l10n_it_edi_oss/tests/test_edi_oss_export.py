# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo.tests import tagged

from odoo.addons.l10n_it_edi.tests.common import TestItEdi


@tagged("post_install_l10n", "post_install", "-at_install")
class TestEdiOssExport(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_oss"

        cls.french_partner = cls.env["res.partner"].create(
            {
                "name": "French Partner",
                "vat": "FR23334175221",
                "country_id": cls.env.ref("base.fr").id,
                "street": "1 Rue de la Paix",
                "city": "Paris",
                "company_id": False,
                "is_company": True,
                "invoice_edi_format": "it_edi_xml",
            }
        )

        oss_tag = cls.env.ref("l10n_eu_oss.tag_oss")
        cls.oss_tax_fr = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "OSS for EU to France: 20.0",
                    "amount": 20.0,
                    "amount_type": "percent",
                    "type_tax_use": "sale",
                    "l10n_it_exempt_reason": "N3.2",
                    "l10n_it_law_reference": "Art. 41 D.L. 331/1993",
                    "sequence": 1000,
                }
            )
        )
        cls.oss_tax_fr.invoice_repartition_line_ids.write(
            {"tag_ids": [(4, oss_tag.id)]}
        )
        cls.oss_tax_fr.refund_repartition_line_ids.write({"tag_ids": [(4, oss_tag.id)]})

    def test_oss_invoice_export(self):
        """OSS invoice exports with AliquotaIVA=0.00, Natura=N3.2,
        AltriDatiGestionali with OSS data, and Imposta=0.00."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.french_partner,
            taxes=self.oss_tax_fr,
        )
        invoice.invoice_date_due = invoice.date
        invoice.action_post()
        self._assert_export_invoice(invoice, "oss_invoice.xml")

    def test_non_oss_invoice_export(self):
        """Non-OSS invoices are not affected by this module."""
        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=self.italian_partner_a,
            taxes=self.default_tax,
        )
        invoice.invoice_date_due = invoice.date
        invoice.action_post()
        xml = invoice._l10n_it_edi_render_xml()
        tree = etree.fromstring(xml)
        oss_nodes = [n for n in tree.iter("TipoDato") if n.text == "OSS"]
        self.assertFalse(
            oss_nodes, "Non-OSS invoice should not have OSS AltriDatiGestionali"
        )
        aliquota_nodes = list(tree.iter("AliquotaIVA"))
        for node in aliquota_nodes:
            self.assertNotEqual(
                node.text,
                "0.00",
                "Non-OSS invoice should have actual tax rate",
            )
