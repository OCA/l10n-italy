# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2011-2021 https://OmniaSolutions.website
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import base64
import logging
import os
from pathlib import Path

from odoo import api, fields, models
from odoo.tools.misc import format_date


class FatturaAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    @api.depends("ir_attachment_id.datas")
    def _compute_xml_data(self):
        for att in self:
            try:
                wiz_obj = self.env["wizard.import.fatturapa"].with_context(
                    from_attachment=att
                )
                fatt = wiz_obj.get_invoice_obj(att)
                cedentePrestatore = \
                    fatt.FatturaElettronicaHeader.CedentePrestatore
                partner_id = wiz_obj.getCedPrest(cedentePrestatore)
                att.xml_supplier_id = partner_id
                att.invoices_number = len(fatt.FatturaElettronicaBody)
                att.invoices_total = 0
                invoices_date = []
                try:
                    for invoice_body in fatt.FatturaElettronicaBody:
                        att.invoices_total += float(
                            invoice_body.DatiGenerali.
                            DatiGeneraliDocumento.ImportoTotaleDocumento
                            or 0
                        )
                        invoice_date = format_date(
                            att.with_context(lang=att.env.user.lang).env,
                            fields.Date.from_string(
                                invoice_body.DatiGenerali.
                                DatiGeneraliDocumento.Data
                            ),
                        )
                        if invoice_date not in invoices_date:
                            invoices_date.append(invoice_date)
                    att.invoices_date = " ".join(invoices_date)
                except Exception as ex:
                    logging.error(ex)
                    att.invoices_date = " "
            except Exception as ex:
                logging.error(ex)
                att.invoices_date = " "

    def create_fatturapa_from_file(self, file_path):
        file_path = str(file_path)
        file_name = os.path.basename(file_path)
        try:
            fatturapa_atts = self.search([("name", "=", file_name)])
            if fatturapa_atts:
                logging.info(
                    "Invoice xml already processed in %s"
                    % str(fatturapa_atts.mapped("name"))
                )
            else:
                with open(file_path, "rb") as f:
                    return self.create(
                        {"name": file_name,
                         "datas": base64.b64encode(f.read())}
                    )
        except Exception as ex:
            logging.error(
                "Unable to load the electronic invoice %s" % file_name)
            logging.error("File %r" % file_path)
            logging.error("%r" % ex)

    def get_xml_customer_invoice(self, pa_in_folder):
        out = self.env["fatturapa.attachment.in"]
        for xml_file in Path(pa_in_folder).rglob("*.xml"):
            logging.info("Processing FatturaPA file: %r" % xml_file)
            tmp_out = self.create_fatturapa_from_file(xml_file)
            if tmp_out:
                out += tmp_out
        return out
