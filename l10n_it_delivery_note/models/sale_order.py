# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
from itertools import groupby

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError
from odoo.fields import Command

from odoo.addons.sale.models.sale_order import SaleOrder

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrderExtended(models.Model):
    _inherit = "sale.order"

    delivery_note_ids = fields.Many2many(
        "stock.delivery.note", compute="_compute_delivery_notes"
    )
    delivery_note_count = fields.Integer(compute="_compute_delivery_notes")

    default_transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
    )
    default_goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance",
        string="Appearance of goods",
    )
    default_transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason",
        string="Reason of transport",
    )
    default_transport_method_id = fields.Many2one(
        "stock.picking.transport.method",
        string="Method of transport",
    )

    @api.onchange("partner_id")
    def onchange_partner_id_shipping_info(self):
        if self.partner_id:
            values = {
                "default_transport_condition_id": (
                    self.partner_id.default_transport_condition_id
                ),
                "default_goods_appearance_id": (
                    self.partner_id.default_goods_appearance_id
                ),
                "default_transport_reason_id": (
                    self.partner_id.default_transport_reason_id
                ),
                "default_transport_method_id": (
                    self.partner_id.default_transport_method_id
                ),
            }

        else:
            values = {
                "default_transport_condition_id": False,
                "default_goods_appearance_id": False,
                "default_transport_reason_id": False,
                "default_transport_method_id": False,
            }

        self.update(values)

    def _compute_delivery_notes(self):
        for order in self:
            delivery_notes = order.order_line.mapped(
                "delivery_note_line_ids.delivery_note_id"
            )

            order.delivery_note_ids = delivery_notes
            order.delivery_note_count = len(delivery_notes)

    def _assign_delivery_notes_invoices(self, invoice_ids):
        order_lines = self.mapped("order_line").filtered(
            lambda order_line: order_line.is_invoiced
            and order_line.delivery_note_line_ids
        )

        delivery_note_lines = order_lines.mapped("delivery_note_line_ids").filtered(
            lambda dn_line: dn_line.is_invoiceable
        )
        delivery_notes = delivery_note_lines.mapped("delivery_note_id")

        ready_delivery_notes = delivery_notes.filtered(
            lambda n: n.state != DOMAIN_DELIVERY_NOTE_STATES[0]
        )

        draft_delivery_notes = delivery_notes - ready_delivery_notes
        draft_delivery_note_lines = (
            draft_delivery_notes.mapped("line_ids") & delivery_note_lines
        )

        ready_delivery_note_lines = delivery_note_lines - draft_delivery_note_lines

        #
        # TODO: È necessario gestire il caso di fatturazione splittata
        #        di una stessa riga d'ordine associata ad una sola
        #        picking (e di conseguenza, ad un solo DdT)?
        #       Può essere, invece, un caso "borderline"
        #        da lasciar gestire all'operatore?
        #       Personalmente, non lo gestirei e delegherei
        #        all'operatore questa responsabilità...
        #

        draft_delivery_note_lines.write(
            {"invoice_status": DOMAIN_INVOICE_STATUSES[0], "sale_line_id": None}
        )

        ready_delivery_note_lines.write({"invoice_status": DOMAIN_INVOICE_STATUSES[2]})
        for ready_delivery_note in ready_delivery_notes:
            ready_invoice_ids = [
                invoice_id
                for invoice_id in ready_delivery_note.sale_ids.mapped("invoice_ids").ids
                if invoice_id in invoice_ids
            ]
            ready_delivery_note.write(
                {"invoice_ids": [(4, invoice_id) for invoice_id in ready_invoice_ids]}
            )

        ready_delivery_notes._compute_invoice_status()

    def _generate_delivery_note_lines(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        invoices.update_delivery_note_lines()

    def _create_invoices(self, grouped=False, final=False, date=None):  # noqa: C901
        if not self.env.company.invoice_lines_grouped_by_dn:
            if not self.env["account.move"].check_access_rights("create", False):
                try:
                    self.check_access_rights("write")
                    self.check_access_rule("write")
                except AccessError:
                    return self.env["account.move"]

            # 1) Create invoices.
            invoice_vals_list = []
            # Incremental sequencing to keep the lines order on the invoice.
            invoice_item_sequence = 0
            for order in self:
                order = order.with_company(order.company_id).with_context(
                    lang=order.partner_invoice_id.lang
                )

                invoice_vals = order._prepare_invoice()
                invoiceable_lines = order._get_invoiceable_lines(final)

                if not any(not line.display_type for line in invoiceable_lines):
                    continue

                invoice_line_vals = []
                down_payment_section_added = False
                for line in invoiceable_lines:
                    if not down_payment_section_added and line.is_downpayment:
                        # Create a dedicated section for the down payments
                        # (put at the end of the invoiceable_lines)
                        invoice_line_vals.append(
                            Command.create(
                                order._prepare_down_payment_section_line(
                                    sequence=invoice_item_sequence
                                )
                            ),
                        )
                        down_payment_section_added = True
                        invoice_item_sequence += 1
                    invoice_line_vals.append(
                        Command.create(
                            line._prepare_invoice_line(sequence=invoice_item_sequence)
                        ),
                    )
                    invoice_item_sequence += 1

                invoice_vals["invoice_line_ids"] += invoice_line_vals
                invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list and self._context.get(
                "raise_if_nothing_to_invoice", True
            ):
                raise UserError(self._nothing_to_invoice_error_message())

            # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
            if not grouped:
                new_invoice_vals_list = []
                invoice_grouping_keys = self._get_invoice_grouping_keys()
                invoice_vals_list = sorted(
                    invoice_vals_list,
                    key=lambda x: [
                        x.get(grouping_key) for grouping_key in invoice_grouping_keys
                    ],
                )
                for _grouping_keys, invoices in groupby(
                    invoice_vals_list,
                    key=lambda x: [
                        x.get(grouping_key) for grouping_key in invoice_grouping_keys
                    ],
                ):
                    origins = set()
                    payment_refs = set()
                    refs = set()
                    ref_invoice_vals = None
                    for invoice_vals in invoices:
                        if not ref_invoice_vals:
                            ref_invoice_vals = invoice_vals
                        else:
                            ref_invoice_vals["invoice_line_ids"] += invoice_vals[
                                "invoice_line_ids"
                            ]
                        origins.add(invoice_vals["invoice_origin"])
                        payment_refs.add(invoice_vals["payment_reference"])
                        refs.add(invoice_vals["ref"])
                    ref_invoice_vals.update(
                        {
                            "ref": ", ".join(refs)[:2000],
                            "invoice_origin": ", ".join(origins),
                            "payment_reference": len(payment_refs) == 1
                            and payment_refs.pop()
                            or False,
                        }
                    )
                    new_invoice_vals_list.append(ref_invoice_vals)
                invoice_vals_list = new_invoice_vals_list

            # 3) Create invoices.

            # As part of the invoice creation, we make sure the sequence of
            # multiple SO do not interfere in a single invoice. Example:
            # SO 1:
            # - Section A (sequence: 10)
            # - Product A (sequence: 11)
            # SO 2:
            # - Section B (sequence: 10)
            # - Product B (sequence: 11)
            #
            # If SO 1 & 2 are grouped in the same invoice, the result will be:
            # - Section A (sequence: 10)
            # - Section B (sequence: 10)
            # - Product A (sequence: 11)
            # - Product B (sequence: 11)
            #
            # Resequencing should be safe, however we resequence only if there
            # are less invoices than orders, meaning a grouping might have been done.
            # This could also mean that only a part of the selected SO are
            # invoiceable, but resequencing in this case shouldn't be an issue.
            if len(invoice_vals_list) < len(self):
                SaleOrderLine = self.env["sale.order.line"]
                for invoice in invoice_vals_list:
                    sequence = 1
                    for line in invoice["invoice_line_ids"]:
                        line[2]["sequence"] = SaleOrderLine._get_invoice_line_sequence(
                            new=sequence, old=line[2]["sequence"]
                        )
                        sequence += 1

            # Manage the creation of invoices in sudo because a salesperson must
            # be able to generate an invoice from a sale order without "billing"
            # access rights. However, he should not be able to create an invoice
            # from scratch.
            moves = (
                self.env["account.move"]
                .sudo()
                .with_context(default_move_type="out_invoice")
                .create(invoice_vals_list)
            )

            # 4) Some moves might actually be refunds: convert them if the
            # total amount is negative We do this after the moves have been
            # created since we need taxes, etc. to know if the total is actually
            # negative or not
            if final:
                moves.sudo().filtered(
                    lambda m: m.amount_total < 0
                ).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view(
                    "mail.message_origin_link",
                    values={
                        "self": move,
                        "origin": move.line_ids.sale_line_ids.order_id,
                    },
                    subtype_id=self.env["ir.model.data"]._xmlid_to_res_id(
                        "mail.mt_note"
                    ),
                )
            self._assign_delivery_notes_invoices(moves.ids)
            self._generate_delivery_note_lines(moves.ids)
            return moves
        else:
            if not self.env["account.move"].check_access_rights("create", False):
                try:
                    self.check_access_rights("write")
                    self.check_access_rule("write")
                except AccessError:
                    return self.env["account.move"]

            # 1) Create invoices.
            invoice_vals_list = []
            invoice_item_sequence = (
                # Incremental sequencing to keep the lines order on the invoice.
                10
            )
            for order in self:
                order = order.with_company(order.company_id).with_context(
                    lang=order.partner_invoice_id.lang
                )

                invoice_vals = order._prepare_invoice()
                invoiceable_lines = order._get_invoiceable_lines(final)

                # if not any(not line.display_type for line in invoiceable_lines):
                #     continue

                invoice_line_vals = []
                down_payment_section_added = False
                for line in invoiceable_lines.mapped("delivery_note_line_ids"):
                    if (
                        not down_payment_section_added
                        and line.sale_line_id.is_downpayment
                    ):
                        # Create a dedicated section for the down payments
                        # (put at the end of the invoiceable_lines)
                        invoice_line_vals.append(
                            Command.create(
                                order._prepare_down_payment_section_line(
                                    sequence=invoice_item_sequence
                                )
                            ),
                        )
                        down_payment_section_added = True
                        invoice_item_sequence += 10
                    invoice_line_vals.append(
                        Command.create(
                            line._prepare_ddt_invoice_line(
                                sequence=invoice_item_sequence
                            )
                        ),
                    )
                    invoice_item_sequence += 10

                invoice_vals["invoice_line_ids"] += invoice_line_vals
                invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list and self._context.get(
                "raise_if_nothing_to_invoice", True
            ):
                raise UserError(self._nothing_to_invoice_error_message())

            # 2) Manage 'grouped' parameter: group by (partner_id, currency_id).
            if not grouped:
                new_invoice_vals_list = []
                invoice_grouping_keys = self._get_invoice_grouping_keys()
                invoice_vals_list = sorted(
                    invoice_vals_list,
                    key=lambda x: [
                        x.get(grouping_key) for grouping_key in invoice_grouping_keys
                    ],
                )
                for _grouping_keys, invoices in groupby(
                    invoice_vals_list,
                    key=lambda x: [
                        x.get(grouping_key) for grouping_key in invoice_grouping_keys
                    ],
                ):
                    origins = set()
                    payment_refs = set()
                    refs = set()
                    ref_invoice_vals = None
                    for invoice_vals in invoices:
                        if not ref_invoice_vals:
                            ref_invoice_vals = invoice_vals
                        else:
                            ref_invoice_vals["invoice_line_ids"] += invoice_vals[
                                "invoice_line_ids"
                            ]
                        origins.add(invoice_vals["invoice_origin"])
                        payment_refs.add(invoice_vals["payment_reference"])
                        refs.add(invoice_vals["ref"])
                    ref_invoice_vals.update(
                        {
                            "ref": ", ".join(refs)[:2000],
                            "invoice_origin": ", ".join(origins),
                            "payment_reference": len(payment_refs) == 1
                            and payment_refs.pop()
                            or False,
                        }
                    )
                    new_invoice_vals_list.append(ref_invoice_vals)
                invoice_vals_list = new_invoice_vals_list
            if len(invoice_vals_list) < len(self):
                SaleOrderLine = self.env["sale.order.line"]
                for invoice in invoice_vals_list:
                    sequence = 1
                    for line in invoice["invoice_line_ids"]:
                        line[2]["sequence"] = SaleOrderLine._get_invoice_line_sequence(
                            new=sequence, old=line[2]["sequence"]
                        )
                        sequence += 1

            moves = (
                self.env["account.move"]
                .sudo()
                .with_context(default_move_type="out_invoice")
                .create(invoice_vals_list)
            )
            if final:
                moves.sudo().filtered(
                    lambda m: m.amount_total < 0
                ).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view(
                    "mail.message_origin_link",
                    values={
                        "self": move,
                        "origin": move.line_ids.sale_line_ids.order_id,
                    },
                    subtype_id=self.env["ir.model.data"]._xmlid_to_res_id(
                        "mail.mt_note"
                    ),
                )
            # return moves
            self._assign_delivery_notes_invoices(moves.ids)
            self._generate_delivery_note_lines(moves.ids)
            return moves

    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped("delivery_note_ids")
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_delivery_note.stock_delivery_note_action"
        )
        action.update(kwargs)

        if len(delivery_notes) > 1:
            action["domain"] = [("id", "in", delivery_notes.ids)]

        elif len(delivery_notes) == 1:
            action["views"] = [
                (
                    self.env.ref(
                        "l10n_it_delivery_note.stock_delivery_note_form_view"
                    ).id,
                    "form",
                )
            ]
            action["res_id"] = delivery_notes.id

        else:
            action = {"type": "ir.actions.act_window_close"}

        return action


SaleOrder._create_invoices = SaleOrderExtended._create_invoices
