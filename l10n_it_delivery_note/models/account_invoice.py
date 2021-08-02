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

            for line in invoice.invoice_line_ids:
                for sale in line.sale_line_ids:
                    delivery_note_line = (
                        invoice.delivery_note_ids.mapped("line_ids")
                        & sale.delivery_note_line_ids
                    )
                    for note_line in delivery_note_line.filtered(
                        lambda l: l.invoice_status == DOMAIN_INVOICE_STATUSES[2]
                    ):
                        line.delivery_note_id = note_line.delivery_note_id.id
                        new_lines.append(
                            (
                                0,
                                False,
                                {
                                    "sequence": line.sequence - 1,
                                    "display_type": "line_note",
                                    "name": _("""Delivery Note "{}" of {}""").format(
                                        note_line.delivery_note_id.name,
                                        note_line.delivery_note_id.date.strftime(
                                            DATE_FORMAT
                                        ),
                                    ),
                                    "note_dn": True,
                                    "delivery_note_id": note_line.delivery_note_id.id,
                                    "quantity": 0,
                                },
                            )
                        )

            invoice.write({"invoice_line_ids": new_lines})

    def group_lines_by_ddt(self):
        for invoice in self.filtered(lambda i: i.delivery_note_ids):
            invoice.invoice_line_ids.filtered(lambda r: r.display_type).unlink()
            dn_list_grouped, residual_list = invoice.grouped_lines_by_ddt()
            invoice.line_ids.unlink()
            line_number = 0
            for dn in dn_list_grouped:
                # prepare nota dn
                delivery_note_id = self.env["stock.delivery.note"].browse(dn)
                nota_dn_vals = {
                    "sequence": line_number,
                    "name": _("""Delivery Note "{}" of {}""").format(
                        delivery_note_id.name,
                        delivery_note_id.date.strftime(DATE_FORMAT),
                    ),
                    "display_type": "line_section",
                    "note_dn": True,
                    "move_id": invoice.id,
                }
                invoice.write({"invoice_line_ids": [(0, 0, nota_dn_vals)]})
                line_number += 1
                for line in dn_list_grouped[dn]:
                    invoice_line_vals = {
                        "sequence": line_number,
                        "delivery_note_id": line["delivery_note_id"],
                        "sale_line_ids": line["sale_line_ids"],
                        "product_id": line["product_id"],
                        "name": line["name"],
                        "quantity": line["quantity"],
                        "product_uom_id": line["product_uom_id"],
                        "discount": line["discount"],
                        "price_unit": line["price_unit"],
                        "account_id": line["account_id"],
                        "tax_ids": line["tax_ids"],
                        "analytic_account_id": line["analytic_account_id"],
                        "analytic_tag_ids": line["analytic_tag_ids"],
                        "move_id": invoice.id,
                    }
                    invoice.write({"invoice_line_ids": [(0, 0, invoice_line_vals)]})
                    line_number += 1
            for line in residual_list:
                invoice_line_vals = {
                    "sequence": line_number,
                    "delivery_note_id": line["delivery_note_id"],
                    "sale_line_ids": line["sale_line_ids"],
                    "product_id": line["product_id"],
                    "name": line["name"],
                    "quantity": line["quantity"],
                    "product_uom_id": line["product_uom_id"],
                    "discount": line["discount"],
                    "price_unit": line["price_unit"],
                    "account_id": line["account_id"],
                    "tax_ids": line["tax_ids"],
                    "analytic_account_id": line["analytic_account_id"],
                    "analytic_tag_ids": line["analytic_tag_ids"],
                    "move_id": invoice.id,
                }
                invoice.write({"invoice_line_ids": [(0, 0, invoice_line_vals)]})
                line_number += 1

    def grouped_lines_by_ddt(self):
        """
        Returns invoice lines from a specified invoice grouped by ddt
        """
        dn_list = []
        residual_list = []

        # do not consider Sections and Notes: they will be overwritten
        for invoice_line in self.invoice_line_ids.filtered(
            lambda l: not l.display_type
        ):
            note_line_qty = 0
            for sale_line in invoice_line.sale_line_ids:
                delivery_note_line_ids = (
                    self.delivery_note_ids.mapped("line_ids")
                    & sale_line.delivery_note_line_ids
                )
                for note_line in delivery_note_line_ids:
                    note_line_qty += note_line.product_qty
                    dn_list.append(
                        {
                            "delivery_note_id": note_line.delivery_note_id.id,
                            "sale_line_ids": [(6, 0, [sale_line.id])],
                            "product_id": invoice_line.product_id.id,
                            "name": invoice_line.name,
                            "quantity": note_line.product_qty,
                            "product_uom_id": note_line.product_uom_id.id,
                            "discount": invoice_line.discount,
                            "price_unit": invoice_line.price_unit,
                            "account_id": invoice_line.account_id.id,
                            "tax_ids": [(6, 0, invoice_line.tax_ids.ids)],
                            "analytic_account_id": invoice_line.analytic_account_id.id,
                            "analytic_tag_ids": [
                                (6, 0, invoice_line.analytic_tag_ids.ids)
                            ],
                        }
                    )
            if invoice_line.quantity != note_line_qty:
                residual_list.append(
                    {
                        "delivery_note_id": False,
                        "sale_line_ids": [(6, 0, invoice_line.sale_line_ids.ids)],
                        "product_id": invoice_line.product_id.id,
                        "name": invoice_line.name,
                        "quantity": invoice_line.quantity - note_line_qty,
                        "product_uom_id": invoice_line.product_uom_id.id,
                        "discount": invoice_line.discount,
                        "price_unit": invoice_line.price_unit,
                        "account_id": invoice_line.account_id.id,
                        "tax_ids": invoice_line.tax_ids.ids,
                        "analytic_account_id": invoice_line.analytic_account_id.id,
                        "analytic_tag_ids": [(6, 0, invoice_line.analytic_tag_ids.ids)],
                    }
                )
        # group by dn
        dn_list.sort(key=lambda x: x.get("delivery_note_id"))
        dn_list_grouped = {}
        for item in dn_list:
            dn_list_grouped.setdefault(item["delivery_note_id"], []).append(item)
        return dn_list_grouped, residual_list

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
