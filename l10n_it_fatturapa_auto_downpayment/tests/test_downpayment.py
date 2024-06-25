from odoo import fields
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestDn(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.partner3 = cls.env.ref("base.res_partner_3")
        cls.product5 = cls.env.ref("product.product_product_5")
        cls.TD02 = cls.env["fiscal.document.type"].search(
            [("code", "=", "TD02")], limit=1
        )

    def test_downpayment(self):
        so = (
            self.env["sale.order"]
            .with_context(tracking_disable=True)
            .create(
                {
                    "partner_id": self.partner3.id,
                    "order_line": [
                        fields.Command.create(
                            {
                                "product_id": self.product5.id,
                                "product_uom_qty": 10.0,
                                "price_unit": 10.0,
                                "tax_id": False,
                            }
                        ),
                    ],
                }
            )
        )
        so.action_confirm()
        dp = (
            self.env["sale.advance.payment.inv"]
            .with_context(active_model="sale.order", active_ids=so.ids, active_id=so.id)
            .create(
                {
                    "advance_payment_method": "fixed",
                    "fixed_amount": 50.0,
                }
            )
        )
        dp.create_invoices()
        self.assertEqual(len(so.invoice_ids), 1)
        self.assertEqual(so.invoice_ids.fiscal_document_type_id, self.TD02)
