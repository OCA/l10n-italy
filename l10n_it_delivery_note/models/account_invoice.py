# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models

from .stock_delivery_note import DATE_FORMAT, DOMAIN_INVOICE_STATUSES


class AccountInvoice(models.Model):
    _inherit = "account.move"

    delivery_note_ids = fields.Many2many(
        "stock.delivery.note",
        "stock_delivery_note_account_invoice_rel",
        "invoice_id",
        "delivery_note_id",
        string="Delivery Notes",
        copy=False,
    )

    delivery_note_count = fields.Integer(compute="_compute_delivery_note_count")

    def _compute_delivery_note_count(self):
        for invoice in self:
            invoice.delivery_note_count = len(invoice.delivery_note_ids)

    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped("delivery_note_ids")
        action = self.env.ref(
            "l10n_it_delivery_note.stock_delivery_note_action"
        ).read()[0]
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

    def goto_invoice(self, **kwargs):
        self.ensure_one()

        if self.move_type.startswith("out"):
            view_id = self.env.ref("account.view_move_form").id

        else:
            view_id = False

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.id,
            "views": [(view_id, "form")],
            "view_mode": "form",
            "target": "current",
            **kwargs,
        }

    def _prepare_note_dn_value(self, sequence, delivery_note_id):
        return {
            "sequence": sequence,
            "display_type": "line_note",
            "name": _("""Delivery Note "{}" of {}""").format(
                delivery_note_id.name,
                delivery_note_id.date.strftime(DATE_FORMAT),
            ),
            "note_dn": True,
            "delivery_note_id": delivery_note_id.id,
            "quantity": 0,
        }

    def update_delivery_note_lines(self):
        context = {}

        for invoice in self.filtered(lambda i: i.delivery_note_ids):
            new_lines = []
            old_lines = invoice.invoice_line_ids.filtered(lambda l: l.note_dn)
            old_lines.unlink()

            #
            # TODO: Come bisogna comportarsi nel caso in
            #        cui il DdT non sia un DdT "valido"?
            #       Al momento, potrebbe essere possibile avere
            #       sia sei DdT senza numero (non ancora confermati)
            #       così come è possibile avere dei DdT senza, necessariamente,
            #       data di trasporto (non è un campo obbligatorio).
            #

            #
            # THIS ALLOWS TO CHANGE TRANSLATION LANGUAGE FOR EVERY INVOICE!
            #
            #   See: odoo/tools/translate.py -> 'def _get_lang(self, frame):'
            #
            context["lang"] = invoice.partner_id.lang

            if len(invoice.delivery_note_ids) == 1:
                sequence = invoice.invoice_line_ids[0].sequence - 1
                new_lines.append(
                    (
                        0,
                        False,
                        self._prepare_note_dn_value(
                            sequence, invoice.delivery_note_ids[0]
                        ),
                    )
                )
            else:
                sequence = 1
                done_invoice_lines = self.env["account.move.line"]
                for dn in invoice.mapped(
                    "invoice_line_ids.sale_line_ids.delivery_note_line_ids."
                    "delivery_note_id"
                ).sorted(key="name"):
                    dn_invoice_lines = invoice.invoice_line_ids.filtered(
                        lambda x: x not in done_invoice_lines
                        and dn
                        in x.mapped(
                            "sale_line_ids.delivery_note_line_ids.delivery_note_id"
                        )
                        # fixme test invoice from 2 sale lines
                    )
                    done_invoice_lines |= dn_invoice_lines
                    for note_line in dn.line_ids.filtered(
                        lambda l: l.invoice_status == DOMAIN_INVOICE_STATUSES[2]
                    ):
                        for invoice_line in dn_invoice_lines:
                            if (
                                note_line
                                in invoice_line.sale_line_ids.delivery_note_line_ids
                            ):
                                invoice_line.delivery_note_id = (
                                    note_line.delivery_note_id.id
                                )
                    new_lines.append(
                        (
                            0,
                            False,
                            self._prepare_note_dn_value(sequence, dn),
                        )
                    )
                    for invoice_line in dn_invoice_lines:
                        sequence += 1
                        invoice_line.sequence = sequence

            invoice.write({"line_ids": new_lines})

    def unlink(self):
        # Ripristino il valore delle delivery note
        # per poterle rifatturare
        inv_lines = self.mapped("invoice_line_ids")
        all_dnls = inv_lines.mapped("sale_line_ids").mapped("delivery_note_line_ids")
        inv_dnls = self.mapped("delivery_note_ids").mapped("line_ids")
        dnls_to_unlink = all_dnls & inv_dnls
        res = super().unlink()
        dnls_to_unlink.sync_invoice_status()
        dnls_to_unlink.mapped("delivery_note_id")._compute_invoice_status()
        for dn in dnls_to_unlink.mapped("delivery_note_id"):
            dn.state = "confirm"
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    delivery_note_id = fields.Many2one(
        "stock.delivery.note", string="Delivery Note", readonly=True, copy=False
    )
    note_dn = fields.Boolean(string="Note DN")
