# Copyright 2022 Sergio Corato
# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date, datetime, timedelta

from odoo.tests import Form
from odoo.tests.common import users
from odoo.tools.date_utils import relativedelta

from .delivery_note_common import StockDeliveryNoteCommon


class StockDeliveryNoteSequence(StockDeliveryNoteCommon):
    def test_new_company_dn_type_creation(self):
        """
        This test is for checking dn_types and sequence creation after
        creating a new company
        """
        company = self.env["res.company"].create(
            {
                "name": "New company",
            }
        )
        dn_types = self.env["stock.delivery.note.type"].search(
            [("company_id", "=", company.id)]
        )
        self.assertTrue(
            dn_types.filtered(
                lambda d: d.name == self.env._("Incoming")
                and d.sequence_id
                == self.env["ir.sequence"].search(
                    [
                        ("code", "=", f"stock.delivery.note.din.c{company.id}"),
                        ("company_id", "=", company.id),
                    ]
                )
            )
        )
        self.assertTrue(
            dn_types.filtered(
                lambda d: d.name == self.env._("Outgoing")
                and d.sequence_id
                == self.env["ir.sequence"].search(
                    [
                        ("code", "=", f"stock.delivery.note.ddt.c{company.id}"),
                        ("company_id", "=", company.id),
                    ]
                )
            )
        )
        self.assertTrue(
            dn_types.filtered(
                lambda d: d.name == self.env._("Outgoing (with prices)")
                and d.sequence_id
                == self.env["ir.sequence"].search(
                    [
                        ("code", "=", f"stock.delivery.note.ddt.c{company.id}"),
                        ("company_id", "=", company.id),
                    ]
                )
            )
        )
        self.assertTrue(
            dn_types.filtered(
                lambda d: d.name == self.env._("Internal transfer")
                and d.sequence_id
                == self.env["ir.sequence"].search(
                    [
                        ("code", "=", f"stock.delivery.note.int.c{company.id}"),
                        ("company_id", "=", company.id),
                    ]
                )
            )
        )

    def test_initial_dn_type_creation(self):
        """
        This test is for checking dn_types and sequence creation by
        l10n_it_delivery_note post_init_hook
        """
        companies = self.env["res.company"].search([])
        for company in companies:
            dn_types = self.env["stock.delivery.note.type"].search(
                [("company_id", "=", company.id)]
            )
            self.assertTrue(
                dn_types.filtered(
                    lambda d, c=company: d.name == self.env._("Incoming")
                    and d.sequence_id
                    == self.env["ir.sequence"].search(
                        [
                            ("code", "=", f"stock.delivery.note.din.c{c.id}"),
                            ("company_id", "=", c.id),
                        ]
                    )
                )
            )
            self.assertTrue(
                dn_types.filtered(
                    lambda d, c=company: d.name == self.env._("Outgoing")
                    and d.sequence_id
                    == self.env["ir.sequence"].search(
                        [
                            ("code", "=", f"stock.delivery.note.ddt.c{c.id}"),
                            ("company_id", "=", c.id),
                        ]
                    )
                )
            )
            self.assertTrue(
                dn_types.filtered(
                    lambda d, c=company: d.name == self.env._("Outgoing (with prices)")
                    and d.sequence_id
                    == self.env["ir.sequence"].search(
                        [
                            ("code", "=", f"stock.delivery.note.ddt.c{c.id}"),
                            ("company_id", "=", c.id),
                        ]
                    )
                )
            )
            self.assertTrue(
                dn_types.filtered(
                    lambda d, c=company: d.name == self.env._("Internal transfer")
                    and d.sequence_id
                    == self.env["ir.sequence"].search(
                        [
                            ("code", "=", f"stock.delivery.note.int.c{c.id}"),
                            ("company_id", "=", c.id),
                        ]
                    )
                )
            )

    @users("fm")
    def test_complete_invoicing_sequence(self):
        company_id = self.env.company.id
        sequence = self.env["ir.sequence"].search(
            [
                ("code", "=", f"stock.delivery.note.ddt.c{company_id}"),
                ("company_id", "=", company_id),
            ]
        )
        current_year = datetime.today().year
        old_year = (datetime.today() - relativedelta(years=1)).year
        for sequence_year in [current_year, old_year]:
            sequence.write(
                {
                    "use_date_range": True,
                    "date_range_ids": [
                        (
                            0,
                            0,
                            {
                                "date_from": date.today().replace(
                                    month=1, day=1, year=sequence_year
                                ),
                                "date_to": date.today().replace(
                                    month=12, day=31, year=sequence_year
                                ),
                            },
                        )
                    ],
                }
            )
        date_range_sequence = sequence.date_range_ids.filtered(
            lambda x: x.date_from == date.today().replace(month=1, day=1, year=old_year)
        )
        date_range_sequence.write({"number_next_actual": 50})
        sale_order = self.create_sales_order(
            [
                self.desk_combination_line,
            ]
        )
        self.assertEqual(len(sale_order.order_line), 1)
        sale_order.action_confirm()
        picking = sale_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_ids), 1)

        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1
        result = picking.button_validate()
        self.assertTrue(result)

        dn_form = Form(
            self.env["stock.delivery.note.create.wizard"].with_context(
                active_ids=picking.ids,
            )
        )
        wizard = dn_form.save()
        wizard.confirm()
        delivery_note = picking.delivery_note_id
        delivery_note.transport_datetime = datetime.now() + timedelta(days=1, hours=3)
        delivery_note.date = date.today().replace(year=old_year)
        delivery_note.action_confirm()

        self.assertEqual(delivery_note.type_id.sequence_id, sequence)
        self.assertEqual(
            delivery_note.name, f"{sequence.prefix}{50:0{sequence.padding}d}"
        )
