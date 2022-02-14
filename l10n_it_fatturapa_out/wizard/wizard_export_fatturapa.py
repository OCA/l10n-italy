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

from .efattura import EFatturaOut

_logger = logging.getLogger(__name__)


def id_generator(
    size=5, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
):
    return "".join(random.choice(chars) for dummy in range(size))


class WizardExportFatturapaReportLine(models.TransientModel):
    _name = "wizard.export.fatturapa.report_line"
    _description = "Allow to select a report to be included in the e-invoice."
    _rec_name = "report_name"

    wizard_id = fields.Many2one(
        comodel_name="wizard.export.fatturapa",
    )
    report_id = fields.Many2one(
        string="Report",
        comodel_name="ir.actions.actions",
    )
    report_name = fields.Char(
        related="report_id.name",
    )
    selected = fields.Boolean(
        string="Select",
    )


class WizardExportFatturapa(models.TransientModel):
    _name = "wizard.export.fatturapa"
    _description = "Export E-invoice"

    @api.model
    def _default_report_print_ids(self):
        model_name = self.env.context.get("active_model", False)
        bindings = self.env["ir.actions.actions"].get_bindings(model_name)
        report_actions = bindings.get("report")
        default_values = [(5, 0, 0)]
        for report_action in report_actions:
            report_id = report_action.get("id")
            if report_id:
                default_values.append(
                    (
                        0,
                        0,
                        {
                            "report_id": report_id,
                        },
                    )
                )
        return default_values

    report_print_ids = fields.One2many(
        comodel_name="wizard.export.fatturapa.report_line",
        inverse_name="wizard_id",
        default=_default_report_print_ids,
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
        selected_reports = self.report_print_ids.filtered("selected")
        for inv in invoice_ids:
            if not attach and inv.fatturapa_attachment_out_id:
                raise UserError(
                    _("E-invoice export file still present for invoice %s.")
                    % (inv.name or "")
                )
            if not inv.fatturapa_doc_attachments and selected_reports:
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
        selected_reports = self.report_print_ids.filtered("selected")
        selected_reports = selected_reports.report_id.sudo()
        att_ids = self.env["ir.attachment"].browse()
        for selected_report in selected_reports:
            binding_model_id = selected_report.with_context(
                lang=None
            ).binding_model_id.id
            name = selected_report.name
            report_model = (
                self.env["ir.actions.report"]
                .with_context(lang=None)
                .search(
                    [("binding_model_id", "=", binding_model_id), ("name", "=", name)]
                )
            )
            attachment, attachment_type = report_model._render_qweb_pdf(inv.ids)
            att_ids |= self.env["ir.attachment"].create(
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
                                "Attachment generated by electronic invoice export"
                            ),
                        },
                    )
                    for att_id in att_ids
                ]
            }
        )
