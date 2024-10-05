# Copyright 2023 Giuseppe Borruso

import base64

from freezegun import freeze_time

from odoo import fields
from odoo.tests import Form, tagged

from odoo.addons.mail.tests.common import mail_new_test_user

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestFatturaPAXMLValidation(FatturaPACommon):
    def setUp(self):
        super(TestFatturaPAXMLValidation, self).setUp()

        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )

        self.env.company.name = "YourCompany"
        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = True
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.state_id = self.env.ref("base.state_us_2").id
        self.env.company.partner_id.zip = "00100"
        self.env.company.partner_id.phone = "06543534343"
        self.env.company.email = "info@yourcompany.example.com"
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

        self.env.ref("product.decimal_product_uom").digits = 3
        self.env.ref("uom.product_uom_unit").name = "Unit(s)"
        self.stock_location = (
            self.env["stock.warehouse"]
            .search(
                [
                    ("company_id", "=", self.env.company.id),
                ],
                limit=1,
            )
            .lot_stock_id
        )

        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
                "currency_id": self.env.user.company_id.currency_id.id,
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "compute_price": "formula",
                            "base": "list_price",
                        },
                    )
                ],
            }
        )

        tax_form = Form(self.env["account.tax"])
        tax_form.name = "22%"
        tax_form.amount = 22
        self.tax22 = tax_form.save()

        product1_lot_from = Form(self.env["product.product"])
        product1_lot_from.name = "Product 1 Lot Test"
        product1_lot_from.type = "product"
        product1_lot_from.taxes_id.clear()
        product1_lot_from.taxes_id.add(self.tax22)
        product1_lot_from.tracking = "lot"
        product1_lot_from.invoice_policy = "delivery"
        product1_lot_from.company_id = self.env.company
        self.product1_lot = product1_lot_from.save()

        product2_lot_from = Form(self.env["product.product"])
        product2_lot_from.name = "Product 2 Serial Test"
        product2_lot_from.type = "product"
        product2_lot_from.taxes_id.clear()
        product2_lot_from.taxes_id.add(self.tax22)
        product2_lot_from.tracking = "serial"
        product2_lot_from.invoice_policy = "delivery"
        product2_lot_from.company_id = self.env.company
        self.product2_lot = product2_lot_from.save()

        lot1_from = Form(self.env["stock.production.lot"])
        lot1_from.name = "Lot 1"
        lot1_from.product_id = self.product1_lot
        lot1_from.company_id = self.env.company
        self.lot1 = lot1_from.save()

        lot2_from = Form(self.env["stock.production.lot"])
        lot2_from.name = "Lot 2"
        lot2_from.product_id = self.product1_lot
        lot2_from.company_id = self.env.company
        self.lot2 = lot2_from.save()

        serial1_from = Form(self.env["stock.production.lot"])
        serial1_from.name = "Serial 1"
        serial1_from.product_id = self.product2_lot
        serial1_from.company_id = self.env.company
        self.serial1 = serial1_from.save()

        self.user_stock_manager = mail_new_test_user(
            self.env,
            name="Stock Manager",
            login="stock_manager",
            groups="stock.group_stock_manager",
        )

    def qty_on_hand(self, product, location, quantity, lot):
        wiz = (
            self.env["stock.inventory"]
            .with_user(self.user_stock_manager)
            .create(
                {
                    "name": "Stock Inventory",
                    "product_ids": [(4, product.id, 0)],
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "product_uom_id": product.uom_id.id,
                                "product_qty": quantity,
                                "prod_lot_id": lot.id,
                                "location_id": location.id,
                            },
                        ),
                    ],
                }
            )
        )
        wiz.action_start()
        wiz.action_validate()

    def _create_sale_order(self):
        sale_order_form = Form(self.env["sale.order"])
        sale_order_form.partner_id = self.res_partner_fatturapa_0
        sale_order_form.partner_invoice_id = self.res_partner_fatturapa_0
        sale_order_form.partner_shipping_id = self.res_partner_fatturapa_0
        sale_order_form.pricelist_id = self.pricelist
        sale_order_form.company_id = self.env.company

        with sale_order_form.order_line.new() as line_form:
            line_form.product_id = self.product1_lot
            line_form.product_uom_qty = 4
            line_form.price_unit = 15

        with sale_order_form.order_line.new() as line_form:
            line_form.product_id = self.product2_lot
            line_form.product_uom_qty = 1
            line_form.price_unit = 10

        sale_order = sale_order_form.save()
        return sale_order

    @freeze_time("2023-10-20 00:00")
    def test_1_lot_xml_export(self):
        # update quantities with their related lots
        self.qty_on_hand(self.product1_lot, self.stock_location, 2, self.lot1)
        self.qty_on_hand(self.product1_lot, self.stock_location, 2, self.lot2)
        self.qty_on_hand(self.product2_lot, self.stock_location, 1, self.serial1)

        # confirm quotation
        sale_order = self._create_sale_order()
        sale_order.action_confirm()
        picking = fields.first(sale_order.picking_ids)
        picking.action_confirm()
        picking.action_assign()
        for sml in picking.move_lines.mapped("move_line_ids"):
            sml.qty_done = sml.product_qty
        picking._action_done()

        # create invoice
        invoice = sale_order._create_invoices()
        invoice.currency_id = self.env.company.currency_id.id
        self.assertEqual(len(invoice.invoice_line_ids), 2)
        line = invoice.invoice_line_ids.filtered(
            lambda x: x.product_id.id == self.product1_lot.id
        )

        # We must have two lots
        self.assertEqual(len(line.prod_lot_ids.ids), 2)
        self.assertIn("Lot 1", line.lots_grouped_by_quantity())
        self.assertIn("Lot 2", line.lots_grouped_by_quantity())
        invoice.action_post()

        res = self.run_wizard(invoice.id)
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00001.xml")
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(xml_content, "IT06363391001_00001.xml")
