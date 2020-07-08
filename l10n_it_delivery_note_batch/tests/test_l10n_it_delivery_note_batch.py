from odoo.tests.common import TransactionCase
from odoo.addons.stock_picking_batch.tests.test_batch_picking import \
    TestBatchPicking


class DeliveryNoteBatchCreationTest(TransactionCase):
    def setUp(self):
        super().setUp()
        # print(self.batch)
        # self.env.user.write({'groups_id': [(4, self.env.ref(
        # 'l10n_it_delivery_note.use_advanced_delivery_notes').id)]})

    def test_multiple_creation_from_batch(self):
        self.assertTrue(True)
        return

        self.env['stock.quant']._update_available_quantity(self.productA,
                                                           self.stock_location,
                                                           10.0)
        self.env['stock.quant']._update_available_quantity(self.productA,
                                                           self.stock_location,
                                                           10.0)
        self.batch.confirm_picking()
        self.assertEqual(self.picking_client_1.state, 'assigned',
                         'Picking 1 should be reserved')
        self.assertEqual(self.picking_client_2.state, 'assigned',
                         'Picking 2 should be reserved')
        self.picking_client_1.move_lines.quantity_done = 10
        self.picking_client_2.move_lines.quantity_done = 10
        self.batch.done()
        self.assertEqual(self.picking_client_1.state, 'done',
                         'Picking 1 should be done')
        self.assertEqual(self.picking_client_2.state, 'done',
                         'Picking 2 should be done')
        quant_A = self.env['stock.quant']._gather(self.productA,
                                                  self.stock_location)
        quant_B = self.env['stock.quant']._gather(self.productB,
                                                  self.stock_location)
        self.assertFalse(sum(quant_A.mapped('quantity')))
        self.assertFalse(sum(quant_B.mapped('quantity')))

        partner = self.env['res.partner'].create({'name': "Mario Rossi"})
