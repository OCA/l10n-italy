#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from freezegun import freeze_time

from odoo.tests import Form, tagged

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestFatturaOutDN(FatturaPACommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # See https://github.com/OCA/l10n-italy/issues/2507
        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        cls.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )

        cls.env.company.name = "YourCompany"
        cls.env.company.vat = "IT06363391001"
        cls.env.company.fatturapa_art73 = True
        cls.env.company.partner_id.street = "Via Milano, 1"
        cls.env.company.partner_id.city = "Roma"
        cls.env.company.partner_id.state_id = cls.env.ref("base.state_us_2").id
        cls.env.company.partner_id.zip = "00100"
        cls.env.company.partner_id.phone = "06543534343"
        cls.env.company.email = "info@yourcompany.example.com"
        cls.env.company.partner_id.country_id = cls.env.ref("base.it").id
        cls.env.company.fatturapa_fiscal_position_id = cls.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id

        product_form = Form(cls.env["product.product"])
        product_form.name = "Test product"
        product_form.type = "product"
        cls.product = product_form.save()

        cls.delivery_note_outgoing_type = cls.env["stock.delivery.note.type"].search(
            [("code", "=", "outgoing"), ("company_id", "=", cls.env.company.id)]
        )
        cls.delivery_note_outgoing_type.sequence_id.prefix = "DDT/"

    def _create_so_dn_invoice(self, partner, products, date):

        # Create and confirm the sale order
        sales_order_form = Form(self.env["sale.order"])
        sales_order_form.partner_id = partner
        for product in products:
            with sales_order_form.order_line.new() as line:
                line.product_id = product
                line.product_uom_qty = 1
        sales_order = sales_order_form.save()
        sales_order.action_confirm()

        # Validate the picking
        picking = sales_order.picking_ids
        picking.move_lines[0].quantity_done = 1
        picking.button_validate()

        # Invoice the delivery note
        delivery_note = picking.delivery_note_id
        delivery_note.date = date
        delivery_note.action_confirm()
        delivery_note.action_invoice()

        invoice = sales_order.invoice_ids
        return sales_order, delivery_note, invoice

    def test_01_invoice_delivery(self):
        """
        DatiDDT is added in the Electronic Invoice
        with reference to the lines linked to a DdT.
        """
        invoice_date = "2019-08-07"
        partner = self.res_partner_fatturapa_0
        products = self.product
        with freeze_time(invoice_date):
            sales_order, delivery_note, invoice = self._create_so_dn_invoice(
                partner, products, invoice_date
            )
            # Add to the invoice a line that is not linked with the DdT
            invoice_form = Form(invoice)
            with invoice_form.invoice_line_ids.new() as line:
                line.product_id = self.product
            invoice_form.save()
            self.set_sequences(10, invoice_date)
            invoice.action_post()
            wizard = self.wizard_model.with_context({"active_ids": invoice.ids}).create(
                {}
            )
            res = wizard.exportFatturaPA()
        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_outDDT.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_outDDT.xml",
            module_name="l10n_it_fatturapa_out_dn",
        )
