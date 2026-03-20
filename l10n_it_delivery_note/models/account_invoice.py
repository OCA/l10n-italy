# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import fields, models

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

    def _prepare_note_dn_value(self, sequence, delivery_note_id):
        return {
            "sequence": sequence,
            "display_type": "line_note",
            "name": self.env._("""Delivery Note "%(ddt_name)s" of %(ddt_date)s""")
            % {
                "ddt_name": delivery_note_id.name,
                "ddt_date": delivery_note_id.date.strftime(DATE_FORMAT),
            },
            "note_dn": True,
            "delivery_note_id": delivery_note_id.id,
            "quantity": 0,
        }

    def update_delivery_note_lines(self):
        context = {}

        for invoice in self.filtered(lambda i: i.delivery_note_ids):
            new_lines = []
            old_lines = invoice.invoice_line_ids.filtered(lambda line: line.note_dn)
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
                for line in invoice.invoice_line_ids:
                    sequence = line.sequence - 1
                    delivery_note_line = invoice.mapped(
                        "delivery_note_ids.line_ids"
                    ) & line.mapped("sale_line_ids.delivery_note_line_ids")
                    for delivery_note_id in delivery_note_line.filtered(
                        lambda l: l.invoice_status  # noqa: E741
                        == DOMAIN_INVOICE_STATUSES[2]
                    ).mapped("delivery_note_id"):
                        line.delivery_note_id = delivery_note_id.id
                        new_lines.append(
                            (
                                0,
                                False,
                                self._prepare_note_dn_value(sequence, delivery_note_id),
                            )
                        )

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

    def button_cancel(self):  # pylint: disable=missing-return
        super().button_cancel()
        dn_lines = (
            self.invoice_line_ids.sale_line_ids.delivery_note_line_ids
            | self.delivery_note_ids.line_ids
        )
        dn_lines.sync_invoice_status()
        dn_lines.delivery_note_id._compute_invoice_status()
        dn_lines.delivery_note_id.state = "confirm"

    def _l10n_it_edi_invoice_is_direct(self):
        """An invoice is direct if ddt are all done the same day as the invoice."""
        if self.delivery_note_ids:
            return all(
                ddt.date and ddt.date == self.invoice_date
                for ddt in self.delivery_note_ids
            )
        return super()._l10n_it_edi_invoice_is_direct()

    def _l10n_it_edi_get_values(self, pdf_values=None):
        """Extend to add dati_ddt_list for delivery notes."""
        values = super()._l10n_it_edi_get_values(pdf_values)
        values["dati_ddt_list"] = self._get_dati_ddt(values["base_lines"])
        return values

    def _get_ddt_values(self):
        # The DdT of this module replace the pickings of l10n_it_stock_ddt,
        # otherwise the same shipping would be exported twice
        if self.delivery_note_ids:
            return {}
        return super()._get_ddt_values()

    def _get_dati_ddt_invoice_lines(self, delivery_note):
        """
        Get the invoice lines shipped by `delivery_note`.

        The link goes through the sale order lines because an invoice line
        can be shipped by more than one DdT (partial deliveries),
        while `delivery_note_id` can only store one of them.
        """
        self.ensure_one()
        invoice_lines = self.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        )
        sale_lines = delivery_note.line_ids.sale_line_id
        lines = invoice_lines.filtered(
            lambda line, dn=delivery_note: line.sale_line_ids & sale_lines
            or line.delivery_note_id == dn
        )
        if not lines and len(self.delivery_note_ids) == 1:
            # Nothing to follow (e.g. DdT lines without sale order):
            # the only DdT of the invoice ships all of its lines
            return invoice_lines
        return lines

    def _get_dati_ddt(self, base_lines):
        """
        Get the data for rendering DatiDDT, one dictionary per DdT.

        :param base_lines: the lines exported as DettaglioLinee
        """
        self.ensure_one()

        # NumeroDDT and DataDDT are mandatory, so only confirmed DdT are exported
        delivery_notes = self.delivery_note_ids.filtered(
            lambda dn: dn.name and dn.date
        ).sorted(lambda dn: (dn.date, dn.id))
        if not delivery_notes:
            return []

        # RiferimentoNumeroLinea has to match the NumeroLinea of DettaglioLinee,
        # that are numbered on base_lines and not on the invoice lines
        line_numbers = defaultdict(list)
        for base_line in base_lines:
            line_numbers[base_line["record"]].append(
                base_line["it_values"]["numero_linea"]
            )

        return [
            {
                "NumeroDDT": delivery_note.name,
                "DataDDT": delivery_note.date,
                "RiferimentoNumeroLinea": sorted(
                    number
                    for line in self._get_dati_ddt_invoice_lines(delivery_note)
                    for number in line_numbers[line]
                ),
            }
            for delivery_note in delivery_notes
        ]
