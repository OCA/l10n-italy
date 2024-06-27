from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestDn(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.partner3 = cls.env.ref("base.res_partner_3")
        cls.product1 = cls.env.ref("product.product_product_1")

    def test_related_documents(self):
        self.product1.invoice_policy = "order"
        so = (
            self.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": self.partner3.id,
                    "client_order_ref": "1234",
                    "order_line": [
                        fields.Command.create(
                            {
                                "product_id": self.product1.id,
                                "product_uom_qty": 10.0,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )
        so.action_confirm()
        so._create_invoices()
        self.assertEqual(len(so.invoice_ids), 1)
        self.assertEqual(len(so.invoice_ids.related_documents), 1)
        self.assertEqual(so.invoice_ids.related_documents.type, "order")
        self.assertEqual(
            so.invoice_ids.related_documents.name, f"{so.name} ({so.client_order_ref})"
        )
        self.assertEqual(so.invoice_ids.related_documents.date, so.date_order.date())
        self.assertEqual(so.invoice_ids.related_documents.numitem, str(so.id))
