# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from collections import defaultdict

from odoo import _, api, fields, models

from .stock_delivery_note import DATE_FORMAT


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

    @api.model
    def _prepare_note_dn_label(self, delivery_note_ids):
        prefix = _("Delivery Note ")
        dn_names = _(" and ").join(
            _(
                '"%(dn_name)s" of %(dn_date)s',
                dn_name=dn.name,
                dn_date=dn.date.strftime(DATE_FORMAT),
            )
            for dn in delivery_note_ids
        )
        return prefix + dn_names

    @api.model
    def _prepare_note_dn_value(self, sequence, delivery_note_ids):
        return {
            "sequence": sequence,
            "display_type": "line_note",
            "name": self._prepare_note_dn_label(delivery_note_ids),
            "note_dn": True,
            "delivery_note_ids": [(6, 0, delivery_note_ids.ids)],
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
                # Build a dictionary {delivery.note(1, 2): account.move.line(3, 5)}
                inv_line_by_dn = defaultdict(self.env["account.move.line"].browse)
                for inv_line in invoice.invoice_line_ids:
                    inv_line.delivery_note_line_ids = inv_line.sale_line_ids.mapped(
                        "delivery_note_line_ids"
                    )
                    dn_ids = inv_line.delivery_note_line_ids.mapped("delivery_note_id")
                    inv_line_by_dn[dn_ids] |= inv_line

                for dnotes, invoce_lines in inv_line_by_dn.items():
                    new_lines.append(
                        (
                            0,
                            False,
                            self._prepare_note_dn_value(sequence, dnotes),
                        )
                    )
                    sequence += 1
                    for inv_line in invoce_lines:
                        inv_line.sequence = sequence
                        sequence += 1
            invoice.write({"line_ids": new_lines})

    def unlink(self):
        dn_lines = self._get_related_delivery_note_lines()
        res = super().unlink()
        self._set_back_delivery_note_status(dn_lines)
        return res

    def button_cancel(self):
        res = super().button_cancel()
        dn_lines = self._get_related_delivery_note_lines()
        self._set_back_delivery_note_status(dn_lines)
        return res

    def _get_related_delivery_note_lines(self):
        return self.mapped("invoice_line_ids.delivery_note_line_ids") or self.mapped(
            "delivery_note_ids.line_ids"
        )

    @api.model
    def _set_back_delivery_note_status(self, dn_lines):
        """
        Allow re-invoicing of delivery note lines after
        deleting/canceling/etc
        """
        dn_lines.sync_invoice_status()
        dn_lines.delivery_note_id._compute_invoice_status()
        dn_lines.delivery_note_id.state = "confirm"


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    delivery_note_line_ids = fields.Many2many(
        "stock.delivery.note.line",
        string="Delivery Note Line",
        readonly=True,
        copy=False,
    )
    # only populated for lines with display_type == "line_note"
    delivery_note_ids = fields.Many2many(
        "stock.delivery.note", string="Delivery Note", readonly=True, copy=False
    )
    note_dn = fields.Boolean(string="Note DN")

    # TODO: remove during migration, only kept for retrocompatibility
    delivery_note_id = fields.Many2one(
        "stock.delivery.note", compute="_compute_delivery_note_id", store=True
    )

    @api.depends(
        "display_type", "delivery_note_line_ids.delivery_note_id", "delivery_note_ids"
    )
    def _compute_delivery_note_id(self):
        for aml in self:
            if aml.display_type:
                aml.delivery_note_id = aml.delivery_note_ids[:1]
            else:
                aml.delivery_note_id = aml.delivery_note_line_ids.delivery_note_id[:1]
