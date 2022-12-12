# Copyright 2022 Sergio Corato
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form
from odoo.tools.date_utils import relativedelta
from .delivery_note_common import StockDeliveryNoteCommon
from datetime import date, datetime, timedelta


class StockDeliveryNoteSequence(StockDeliveryNoteCommon):

    def test_complete_invoicing_sequence(self):
        sequence = self.env.ref('l10n_it_delivery_note_base.delivery_note_sequence_ddt')
        current_year = datetime.today().year
        old_year = (datetime.today() - relativedelta(years=1)).year
        for sequence_year in [current_year, old_year]:
            sequence.write({
                "use_date_range": True,
                "date_range_ids": [
                    (0, 0, {
                        'date_from': date.today().replace(
                            month=1, day=1, year=sequence_year),
                        'date_to': date.today().replace(
                            month=12, day=31, year=sequence_year),
                    })
                ],
            })
        date_range_sequence = sequence.date_range_ids.filtered(
            lambda x: x.date_from == date.today().replace(
                month=1, day=1, year=old_year)
        )
        date_range_sequence.write({'number_next_actual': 50})
        sale_order = self.create_sales_order([
            self.desk_combination_line,
        ])
        self.assertEqual(len(sale_order.order_line), 1)
        sale_order.action_confirm()
        picking = sale_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_lines), 1)

        picking.move_lines[0].quantity_done = 1
        result = picking.button_validate()
        self.assertIsNone(result)

        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                active_ids=picking.ids,
            )
        )
        wizard = dn_form.save()
        wizard.confirm()
        delivery_note = picking.delivery_note_id
        delivery_note.transport_datetime = \
            datetime.now() + timedelta(days=1, hours=3)
        delivery_note.date = date.today().replace(year=old_year)
        delivery_note.action_confirm()

        self.assertEqual(delivery_note.type_id.sequence_id, sequence)
        self.assertEqual(delivery_note.name,
                         sequence.prefix + '%%0%sd' % sequence.padding % 50)
