# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

from odoo import api, fields, models

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrder(models.Model):
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
        invoices = self.env["account.move"].browse(invoice_ids)
        for order_line in self.order_line:
            for dn_line in order_line.delivery_note_line_ids:
                if dn_line.delivery_note_id.state == DOMAIN_DELIVERY_NOTE_STATES[0]:
                    # The Delivery Note is not ready for invoicing yet,
                    # so all its lines do not have to be invoiced
                    dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[0]
                    continue

                invoiced_dn_lines = (
                    dn_line.sale_line_id.invoice_lines.delivery_note_line_id
                )
                for inv_line in invoices.invoice_line_ids:
                    if dn_line.sale_line_id in inv_line.sale_line_ids:
                        if not inv_line.delivery_note_line_id:
                            # The invoice line is usually linked
                            # upon invoice line creation
                            # (see `sale.order.line._prepare_invoice_line`).
                            # In the case of Kits, we need to create the link
                            # because the Invoiced Kit does not appear in the
                            # Delivery Note.
                            inv_line.delivery_note_line_id = dn_line
                        elif dn_line not in invoiced_dn_lines:
                            # The Delivery Note Line is not linked
                            # to any Invoice of the current Sale Order Line
                            continue

                        dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[2]
                        break
                else:
                    dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[1]

    def _generate_delivery_note_lines(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        invoices.update_delivery_note_lines()

    def _get_invoiceable_lines(self, final=False):
        order_lines = super()._get_invoiceable_lines(final=final)
        new_order_lines = self.env["sale.order.line"].browse()
        for order_line in order_lines:
            invoiceable_dn_lines = order_line._get_invoiceable_dn_lines()
            if len(invoiceable_dn_lines) > 1:
                # Add a new order line for each linked delivery note line.
                # Every new corresponding invoice line
                # will invoice the delivered quantity
                for _index in range(len(invoiceable_dn_lines) - 1):
                    new_order_lines += order_line
            new_order_lines += order_line
        return new_order_lines

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)

        self._assign_delivery_notes_invoices(invoice_ids.ids)
        self._generate_delivery_note_lines(invoice_ids.ids)

        return invoice_ids

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
