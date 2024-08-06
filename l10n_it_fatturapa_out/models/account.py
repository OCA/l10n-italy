# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group

import base64

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools.translate import _

fatturapa_attachment_state_mapping = {
    "ready": "ready",
    "sent": "sent",
    "validated": "delivered",
    "sender_error": "error",
    "recipient_error": "accepted",
    "accepted": "accepted",
    "rejected": "error",
}


class AccountInvoice(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_out_id = fields.Many2one(
        "fatturapa.attachment.out", "E-invoice Export File", readonly=True, copy=False
    )

    has_pdf_invoice_print = fields.Boolean(
        related="fatturapa_attachment_out_id.has_pdf_invoice_print", readonly=True
    )

    fatturapa_state = fields.Selection(
        [
            ("ready", "Ready to Send"),
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("accepted", "Accepted"),
            ("error", "Error"),
        ],
        string="E-invoice State",
        compute="_compute_fatturapa_state",
        store="true",
    )

    @api.depends("fatturapa_attachment_out_id.state")
    def _compute_fatturapa_state(self):
        for record in self:
            record.fatturapa_state = fatturapa_attachment_state_mapping.get(
                record.fatturapa_attachment_out_id.state
            )

    def preventive_checks(self):
        for invoice in self:
            if not invoice.is_sale_document():
                raise UserError(
                    _("Impossible to generate XML: not a customer invoice: %s")
                    % invoice.name
                )

            if (
                invoice.invoice_payment_term_id
                and invoice.invoice_payment_term_id.fatturapa_pt_id.code is False
            ):
                raise UserError(
                    _(
                        "Invoice %(name)s fiscal payment term must be"
                        " set for the selected payment term %(term)s"
                    )
                    % {
                        "name": invoice.name,
                        "term": invoice.invoice_payment_term_id.name,
                    },
                )

            if (
                invoice.invoice_payment_term_id
                and invoice.invoice_payment_term_id.fatturapa_pm_id.code is False
            ):
                raise UserError(
                    _(
                        "Invoice %(name)s fiscal payment method must be"
                        " set for the selected payment term %(term)s"
                    )
                    % {
                        "name": invoice.name,
                        "term": invoice.invoice_payment_term_id.name,
                    },
                )

            if not all(
                aml.tax_ids for aml in invoice.invoice_line_ids if aml.product_id
            ):
                raise UserError(
                    _("Invoice %s contains product lines w/o taxes") % invoice.name
                )
            company_id = invoice.company_id
            if company_id.vat != company_id.partner_id.vat:
                raise UserError(
                    _("Invoice %s: company and company partner must have same vat")
                    % invoice.name
                )
        return

    @api.model
    def check_tag(self, new_xml, original_xml, tags, precision=None):
        """
        This function check if tag in new xml generated after function write()
        is the same of original xml

        :param new_xml: new xml generated after function write()
        :param original_xml: original xml linked to invoice
        :param tags: tags of xml to check
        :param precision: precision to apply on text tag for check
        :return: True if tags is the same else
        """
        for tag in tags:
            new_tag_text = new_xml.find(tag) is not None and new_xml.find(tag).text
            original_tag_text = (
                original_xml.find(tag) is not None and original_xml.find(tag).text
            )
            if precision:
                new_tag_text = "{text:.{precision}f}".format(
                    text=float(new_tag_text), precision=precision
                )
                original_tag_text = "{text:.{precision}f}".format(
                    text=float(original_tag_text), precision=precision
                )
            if (new_tag_text or "").strip() != (original_tag_text or "").strip():
                raise UserError(
                    _("%(tag)s isn't equal to tag in file e-invoice already created!")
                    % {"tag": tag[2:]}
                )

    def check_CessionarioCommittente(self, new_xml, original_xml):
        list_tag = [
            ".//CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdPaese",
            ".//CessionarioCommittente/DatiAnagrafici/IdFiscaleIVA/IdCodice",
        ]
        self.check_tag(new_xml, original_xml, list_tag)

    def check_DatiGeneraliDocumento(self, new_xml, original_xml):
        price_precision = self.env["decimal.precision"].precision_get(
            "Product Price for XML e-invoices"
        )

        list_tag = [
            ".//DatiGeneraliDocumento/Data",
            ".//DatiGeneraliDocumento/TipoDocumento",
            ".//DatiGeneraliDocumento/Divisa",
            ".//DatiGeneraliDocumento/Numero",
        ]
        self.check_tag(new_xml, original_xml, list_tag)
        list_tag = [
            ".//DatiGeneraliDocumento/ImportoTotaleDocumento",
        ]
        self.check_tag(new_xml, original_xml, list_tag, price_precision)

        if len(new_xml.findall(".//DatiGeneraliDocumento/DatiRitenuta")) != len(
            original_xml.findall(".//DatiGeneraliDocumento/DatiRitenuta")
        ):
            raise UserError(
                _(
                    "DatiGeneraliDocumento/DatiRitenuta "
                    "isn't equal to tag in file e-invoice already created!"
                )
            )
        for lr, new_line_ritenuta in enumerate(
            new_xml.findall(".//DatiGeneraliDocumento/DatiRitenuta")
        ):
            original_line_ritenuta = original_xml.findall(
                ".//DatiGeneraliDocumento/DatiRitenuta"
            )[lr]
            list_tag_DatiRitenuta = [
                ".//TipoRitenuta",
                ".//CausalePagamento",
            ]
            self.check_tag(
                new_line_ritenuta, original_line_ritenuta, list_tag_DatiRitenuta
            )
            list_tag_DatiRitenuta = [
                ".//ImportoRitenuta",
                ".//AliquotaRitenuta",
            ]
            self.check_tag(
                new_line_ritenuta,
                original_line_ritenuta,
                list_tag_DatiRitenuta,
                price_precision,
            )

    def check_DatiBeniServizi(self, new_xml, original_xml):
        price_precision = self.env["decimal.precision"].precision_get(
            "Product Price for XML e-invoices"
        )
        uom_precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )

        if len(new_xml.findall(".//DatiBeniServizi/DettaglioLinee")) != len(
            original_xml.findall(".//DatiBeniServizi/DettaglioLinee")
        ):
            raise UserError(
                _(
                    "DatiBeniServizi/DettaglioLinee "
                    "isn't equal to tag in file e-invoice already created!"
                )
            )
        for ld, new_line_details in enumerate(
            new_xml.findall(".//DatiBeniServizi/DettaglioLinee")
        ):
            original_line_details = original_xml.findall(
                ".//DatiBeniServizi/DettaglioLinee"
            )[ld]
            list_tag_DettaglioLinee = [
                ".//NumeroLinea",
                ".//CodiceTipo",
                ".//CodiceValore",
                ".//Descrizione",
                ".//Natura",
                ".//Ritenuta",
            ]
            self.check_tag(
                new_line_details, original_line_details, list_tag_DettaglioLinee
            )
            list_tag_DettaglioLinee = [
                ".//Quantita",
            ]
            self.check_tag(
                new_line_details,
                original_line_details,
                list_tag_DettaglioLinee,
                uom_precision,
            )
            list_tag_DettaglioLinee = [
                ".//PrezzoUnitario",
                ".//AliquotaIVA",
                ".//PrezzoTotale",
            ]
            self.check_tag(
                new_line_details,
                original_line_details,
                list_tag_DettaglioLinee,
                price_precision,
            )

        if len(new_xml.findall(".//DatiBeniServizi/DatiRiepilogo")) != len(
            original_xml.findall(".//DatiBeniServizi/DatiRiepilogo")
        ):
            raise UserError(
                _(
                    "DatiBeniServizi/DatiRiepilogo "
                    "isn't equal to tag in file e-invoice already created!"
                )
            )
        for lr, new_line_riepilogo in enumerate(
            new_xml.findall(".//DatiBeniServizi/DatiRiepilogo")
        ):
            original_line_riepilogo = original_xml.findall(
                ".//DatiBeniServizi/DatiRiepilogo"
            )[lr]
            list_tag_DatiRiepilogo = [
                ".//AliquotaIVA",
                ".//ImponibileImporto",
                ".//Imposta",
            ]
            self.check_tag(
                new_line_riepilogo,
                original_line_riepilogo,
                list_tag_DatiRiepilogo,
                price_precision,
            )

    def elements_equal(self, new_xml, original_xml):
        self.check_CessionarioCommittente(new_xml, original_xml)
        self.check_DatiGeneraliDocumento(new_xml, original_xml)
        self.check_DatiBeniServizi(new_xml, original_xml)

    def check_move_confirmable(self):
        self.ensure_one()

        if not self.state == "posted" and not (
            request
            and request.params.get("method", False)
            and request.params["method"] == "action_post"
        ):
            return True
        return False

    def write(self, vals):
        is_draft = {}
        for move in self:
            is_draft[move.id] = True if move.state == "draft" else False
        res = super().write(vals)
        for move in self:
            if (
                move.is_sale_document()
                and move.fatturapa_attachment_out_id
                and is_draft[move.id]
                and not move.state == "cancel"
                and not move.env.context.get("skip_check_xml", False)
                and not (
                    request
                    and request.params.get("method", False)
                    and request.params["method"] == "button_draft"
                )
            ):
                context_partner = self.env.context.copy()
                context_partner.update({"lang": move.partner_id.lang})
                context_partner.update(skip_check_xml=True)
                fatturapa, progressivo_invio = self.env[
                    "wizard.export.fatturapa"
                ].exportInvoiceXML(move.partner_id, [move.id], context=context_partner)
                new_xml_content = fatturapa.to_xml(self.env)
                original_xml_content = base64.decodebytes(
                    move.fatturapa_attachment_out_id.datas
                )
                parser = etree.XMLParser(remove_blank_text=True)
                new_xml = etree.fromstring(new_xml_content, parser)
                original_xml = etree.fromstring(original_xml_content, parser)
                move.elements_equal(new_xml, original_xml)
                if move.check_move_confirmable():
                    move.with_context(skip_check_xml=True).action_post()
        return res

    def button_draft(self):
        for invoice in self:
            if (
                invoice.fatturapa_state != "error"
                and invoice.fatturapa_attachment_out_id
                and not self.env.user.has_group(
                    "l10n_it_fatturapa_out.group_edit_invoice_sent_sdi"
                )
            ):
                raise UserError(
                    _(
                        "Invoice %s has XML and can't be reset to draft. "
                        "Delete the XML before."
                    )
                    % invoice.name
                )
        res = super().button_draft()
        return res
