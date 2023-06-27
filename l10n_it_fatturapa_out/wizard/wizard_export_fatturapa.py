# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Simone Rubino - Agile Business Group
# Copyright 2018 Sergio Corato
# Copyright 2019 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import itertools
import logging
import random
import string

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export

from .efattura import EFatturaOut, format_numbers

_logger = logging.getLogger(__name__)


def id_generator(
    size=5, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
):
    return "".join(random.choice(chars) for dummy in range(size))


class WizardExportFatturapa(models.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export E-invoice"

    @api.model
    def _domain_ir_values(self):
        model_name = self.env.context.get("active_model", False)
        # Get all print actions for current model
        return [
            ("binding_model_id", "=", model_name),
            ("type", "=", "ir.actions.report"),
        ]

    def _get_selection(self):
        reports = self.env["ir.actions.actions"].sudo().search(self._domain_ir_values())
        ret = [(str(r.id), r.name) for r in reports]
        return ret

    report_print_menu = fields.Selection(
        selection="_get_selection",
        help="This report will be automatically included in the created XML",
    )

    def saveAttachment(self, fatturapa, number):
        attach_obj = self.env["fatturapa.attachment.out"]
        vat = attach_obj.get_file_vat()

        attach_str = fatturapa.to_xml(self.env)
        attach_vals = {
            "name": "{}_{}.xml".format(vat, number),
            "datas": base64.encodebytes(attach_str),
        }
        return attach_obj.create(attach_vals)

    def getPartnerId(self, invoice_ids):

        invoice_model = self.env["account.move"]
        partner = False

        invoices = invoice_model.browse(invoice_ids)

        for invoice in invoices:
            if not partner:
                partner = invoice.partner_id
            if invoice.partner_id != partner:
                raise UserError(
                    _("Invoices %s must belong to the same partner.")
                    % ", ".join(invoices.mapped("name"))
                )

        return partner

    @api.model
    def getPayments(self, invoice):
        """Entry point for other modules to override computation of
        DettaglioPagamento

        We use a specialized class to allow other modules change
        values w/o altering the original lines"""

        class _Payment:
            __slots__ = "date_maturity", "amount_currency", "debit"

            def __init__(self, date_maturity, amount_currency, debit):
                self.date_maturity = date_maturity
                self.amount_currency = amount_currency
                self.debit = debit

        payments = []
        for line in invoice.line_ids.filtered(
            lambda line: line.account_id.user_type_id.type in ("receivable", "payable")
        ):
            payments.append(
                _Payment(line.date_maturity, line.amount_currency, line.debit)
            )
        return payments

    @api.model
    def getImportoTotale(self, invoice):
        """Entry point for other modules to override computation of
        ImportoTotaleDocumento"""
        # this requires a better refactoring. We SHOULD be able to use
        # amount_total as is, w/o further computations.
        # At the moment, some modules store the total amount to be paid
        # by the customer, and handle the printed total in the print
        # report (there are cases in which the partner does not have to
        # paid the VAT, yet its amount has to be printed out and included
        # in the total amount of the invoice)
        return invoice.amount_total

    @api.model
    def getAllTaxes(self, invoice):
        """Generate summary data for taxes.
        Odoo does that for us, but only for nonzero taxes.
        SdI expects a summary for every tax mentioned in the invoice,
        even those with price_total == 0.
        """

        def _key(tax_id):
            return tax_id.id

        out_computed = {}
        # existing tax lines
        tax_ids = invoice.line_ids.filtered(lambda line: line.tax_line_id)
        for tax_id in tax_ids:
            tax_line_id = tax_id.tax_line_id
            aliquota = format_numbers(tax_line_id.amount)
            key = _key(tax_line_id)
            out_computed[key] = {
                "AliquotaIVA": aliquota,
                "Natura": tax_line_id.kind_id.code,
                # 'Arrotondamento':'',
                "ImponibileImporto": tax_id.tax_base_amount,
                "Imposta": tax_id.price_total,
                "EsigibilitaIVA": tax_line_id.payability,
            }
            if tax_line_id.law_reference:
                out_computed[key]["RiferimentoNormativo"] = encode_for_export(
                    tax_line_id.law_reference, 100
                )

        out = {}
        # check for missing tax lines
        for line in invoice.invoice_line_ids:
            if line.display_type in ("line_section", "line_note"):
                # notes and sections
                # we ignore line.tax_ids altogether,
                # (it is popolated with a default tax usually)
                # and use another tax in the template
                continue
            for tax_id in line.tax_ids:
                aliquota = format_numbers(tax_id.amount)
                key = _key(tax_id)
                if key in out_computed:
                    continue
                if key not in out:
                    out[key] = {
                        "AliquotaIVA": aliquota,
                        "Natura": tax_id.kind_id.code,
                        # 'Arrotondamento':'',
                        "ImponibileImporto": line.price_subtotal,
                        "Imposta": 0.0,
                        "EsigibilitaIVA": tax_id.payability,
                    }
                    if tax_id.law_reference:
                        out[key]["RiferimentoNormativo"] = encode_for_export(
                            tax_id.law_reference, 100
                        )
                else:
                    out[key]["ImponibileImporto"] += line.price_subtotal
                    out[key]["Imposta"] += 0.0
        out.update(out_computed)
        return out

    @api.model
    def getTemplateValues(self, template_values):
        """
        Entry point for other modules to override values
        (and helper functions) passed to template
        """
        return template_values

    def group_invoices_by_partner(self):
        def split_list(my_list, size):
            it = iter(my_list)
            item = list(itertools.islice(it, size))
            while item:
                yield item
                item = list(itertools.islice(it, size))

        invoice_ids = self.env.context.get("active_ids", False)
        res = {}
        for invoice in self.env["account.move"].browse(invoice_ids):
            if invoice.partner_id not in res:
                res[invoice.partner_id] = []
            res[invoice.partner_id].append(invoice.id)
        for partner_id in res.keys():
            if partner_id.max_invoice_in_xml:
                res[partner_id] = list(
                    split_list(res[partner_id], partner_id.max_invoice_in_xml)
                )
            else:
                res[partner_id] = [res[partner_id]]
        # The returned dictionary contains a plain res.partner object as key
        # because that avoid to call the .browse() during the xml generation
        # this will speedup the algorithm. As value we have a list of list
        # such as [[inv1, inv2, inv3], [inv4, inv5], ...] where every subgroup
        # represents as per customer splitting invoice block defined by
        # max_invoice_in_xml field
        return res

    def setProgressivoInvio(self, attach=False):
        # if the attachment is given than we will reuse its file_id
        if attach:
            file_id = attach.name.split("_")[1].split(".")[0]
        else:
            file_id = id_generator()
            Attachment = self.env["fatturapa.attachment.out"]
            while Attachment.file_name_exists(file_id):
                file_id = id_generator()
        return file_id

    def _get_efattura_class(self):
        return EFatturaOut

    def exportInvoiceXML(self, partner, invoice_ids, attach=False, context=None):
        EFatturaOut = self._get_efattura_class()

        progressivo_invio = self.setProgressivoInvio(attach)
        invoice_ids = self.env["account.move"].with_context(context).browse(invoice_ids)
        invoice_ids.preventive_checks()

        # generate attachments (PDF version of invoice)
        for inv in invoice_ids:
            if not attach and inv.fatturapa_attachment_out_id:
                raise UserError(
                    _("E-invoice export file still present for invoice %s.")
                    % (inv.name or "")
                )
            if not inv.fatturapa_doc_attachments and self.report_print_menu:
                self.generate_attach_report(inv)
        fatturapa = EFatturaOut(self, partner, invoice_ids, progressivo_invio)
        return fatturapa, progressivo_invio

    def exportFatturaPA(self):
        invoice_obj = self.env["account.move"]
        invoices_by_partner = self.group_invoices_by_partner()
        attachments = self.env["fatturapa.attachment.out"]
        for partner in invoices_by_partner:
            context_partner = self.env.context.copy()
            context_partner.update({"lang": partner.lang})
            for invoice_ids in invoices_by_partner[partner]:
                fatturapa, progressivo_invio = self.exportInvoiceXML(
                    partner, invoice_ids, context=context_partner
                )

                attach = self.saveAttachment(fatturapa, progressivo_invio)
                attachments |= attach

                for invoice_id in invoice_ids:
                    inv = invoice_obj.browse(invoice_id)
                    inv.write({"fatturapa_attachment_out_id": attach.id})

        action = {
            "name": "Export Electronic Invoice",
            "res_model": "fatturapa.attachment.out",
            "type": "ir.actions.act_window",
        }
        if len(attachments) == 1:
            action["view_mode"] = "form"
            action["res_id"] = attachments[0].id
        else:
            action["view_mode"] = "tree,form"
            action["domain"] = [("id", "in", attachments.ids)]
        return action

    def generate_attach_report(self, inv):
        try:
            report_id = int(self.report_print_menu)
        except ValueError:
            raise UserError(_("Print report not found"))

        report_model = self.env["ir.actions.report"].sudo().browse(report_id)
        attachment, attachment_type = report_model._render_qweb_pdf(inv.ids)
        att_id = self.env["ir.attachment"].create(
            {
                "name": "{}.pdf".format(inv.name),
                "type": "binary",
                "datas": base64.encodebytes(attachment),
                "res_model": "account.move",
                "res_id": inv.id,
                "mimetype": "application/x-pdf",
            }
        )
        inv.write(
            {
                "fatturapa_doc_attachments": [
                    (
                        0,
                        0,
                        {
                            "is_pdf_invoice_print": True,
                            "ir_attachment_id": att_id.id,
                            "description": _(
                                "Attachment generated by " "electronic invoice export"
                            ),
                        },
                    )
                ]
            }
        )
