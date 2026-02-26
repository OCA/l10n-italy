# Copyright 2026 Lorenzo Battistini
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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

        cls.oss_tax_fr = (
            cls.env["account.tax"]
            .with_company(cls.company)
            .create(
                {
                    "name": "OSS for EU to France: 20.0",
                    "amount": 20.0,
                    "amount_type": "percent",
                    "type_tax_use": "sale",
                    "oss_country_id": cls.env.ref("base.fr").id,
                    "l10n_it_exempt_reason": "N3.2",
                    "l10n_it_law_reference": "Art. 41 D.L. 331/1993",
                    "sequence": 1000,
                }
            )
        )

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
