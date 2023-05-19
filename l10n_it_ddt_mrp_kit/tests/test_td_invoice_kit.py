#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, SavepointCase


class TestTDInvoiceKit (SavepointCase):

    @classmethod
    def _get_kit_bom(cls, kit_product, bom_lines_values):
        kit_bom_form = Form(cls.env['mrp.bom'])
        kit_bom_form.product_tmpl_id = kit_product.product_tmpl_id
        kit_bom_form.product_id = kit_product
        kit_bom_form.type = 'phantom'
        for bom_line_values in bom_lines_values:
            with kit_bom_form.bom_line_ids.new() as line:
                for bom_line_field, bom_line_value in bom_line_values.items():
                    setattr(line, bom_line_field, bom_line_value)
        kit_bom = kit_bom_form.save()
        return kit_bom

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': "Test Customer",
            'customer': True,
        })

        cls.component_1_product, cls.component_2_product, \
            cls.kit_product = \
            cls.env['product.product'].create([
                {
                    'name': "Test component 1",
                },
                {
                    'name': "Test component 2",
                },
                {
                    'name': "Test kit",
                },
            ])
        cls.kit_bom = cls._get_kit_bom(cls.kit_product, [
            {
                'product_id': cls.component_1_product,
                'product_qty': 1,
            },
            {
                'product_id': cls.component_2_product,
                'product_qty': 2,
            },
        ])
        cls.other_kit_bom = cls._get_kit_bom(cls.kit_product, [
            {
                'product_id': cls.component_1_product,
                'product_qty': 3,
            },
            {
                'product_id': cls.component_2_product,
                'product_qty': 4,
            },
        ])

    def _create_sale_picking_td(self, customer, kit_product):
        sale = self.env['sale.order'].create({
            'partner_id': customer.id,
            'order_line': [
                (0, 0, {
                    'display_type': "line_note",
                    'name': "Note",
                }),
                (0, 0, {
                    'product_id': kit_product.id,
                }),
            ],
            'create_ddt': True,
            'carriage_condition_id':
                self.ref('l10n_it_ddt.carriage_condition_PF'),
            'goods_description_id':
                self.ref('l10n_it_ddt.goods_description_CAR'),
            'transportation_reason_id':
                self.ref('l10n_it_ddt.transportation_reason_VEN'),
            'transportation_method_id':
                self.ref('l10n_it_ddt.transportation_method_DES'),
        })
        sale.action_confirm()

        picking = sale.picking_ids
        picking.action_assign()

        td = sale.ddt_ids
        td.action_put_in_pack()
        td.action_done()
        return sale, picking, td

    def _invoice_td(self, td):
        invoice_wiz = self.env['ddt.create.invoice'] \
            .with_context(
            active_ids=td.ids,
            active_model=td._name,
        ) \
            .create({})
        res = invoice_wiz.create_invoice()
        invoices_model = res['res_model']
        invoices_domain = res['domain']
        invoices = self.env[invoices_model].search(invoices_domain)
        return invoices

    def test_td_invoice_kit(self):
        """Create a TD from a kit Sale and invoice the TD:
        only the kit has been invoiced.
        """
        # Arrange: Create a TD from a kit Sale
        customer = self.customer
        component_1_product, component_2_product, kit_product = \
            self.component_1_product, self.component_2_product, self.kit_product

        sale, picking, td = self._create_sale_picking_td(customer, kit_product)
        # pre-condition: We have sold the kit and its components have been sent
        bom = self.env['mrp.bom']._bom_find(product=kit_product)
        self.assertEqual(bom.type, 'phantom')
        self.assertEqual(kit_product, sale.order_line.mapped('product_id'))
        self.assertEqual(
            component_1_product | component_2_product,
            picking.move_line_ids_without_package.mapped('product_id'),
        )
        self.assertEqual(
            component_1_product | component_2_product,
            td.line_ids.mapped('product_id'),
        )

        # Act: Invoice the TD
        invoices = self._invoice_td(td)

        # Assert: Only the kit has been invoiced
        self.assertEqual(
            kit_product,
            invoices.invoice_line_ids.mapped('product_id'),
        )
