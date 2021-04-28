import base64
import os
import shutil
import zipfile
from datetime import datetime

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.fields import first

from odoo.addons.l10n_it_fatturapa.bindings import fatturapa


class FatturaPAAttachmentImportZIP(models.Model):
    _name = "fatturapa.attachment.import.zip"
    _description = "E-bill ZIP import"
    _inherits = {"ir.attachment": "ir_attachment_id"}
    _inherit = ["mail.thread"]
    _order = "id desc"

    ir_attachment_id = fields.Many2one(
        "ir.attachment", "Attachment", required=True, ondelete="cascade"
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("done", "Completed"),
        ],
        string="State",
        default="draft",
        required=True,
        readonly=True,
    )
    messages = fields.Text(
        "Error Messages", readonly=True, compute="_compute_invoices_data"
    )
    xml_out_count = fields.Integer(
        string="XML Out Count", compute="_compute_invoices_data", readonly=True
    )
    xml_in_count = fields.Integer(
        string="XML In Count", compute="_compute_invoices_data", readonly=True
    )
    invoices_out_count = fields.Integer(
        string="Invoices Out Count", compute="_compute_invoices_data", readonly=True
    )
    invoices_in_count = fields.Integer(
        string="Invoices In Count", compute="_compute_invoices_data", readonly=True
    )
    attachment_out_ids = fields.One2many(
        "fatturapa.attachment.out",
        "attachment_import_zip_id",
        string="Attachments Out",
        readonly=True,
    )
    attachment_in_ids = fields.One2many(
        "fatturapa.attachment.in",
        "attachment_import_zip_id",
        string="Attachments In",
        readonly=True,
    )
    invoice_out_ids = fields.One2many(
        "account.invoice", "attachment_out_import_zip_id", string="Invoices Out"
    )
    invoice_in_ids = fields.One2many(
        "account.invoice", "attachment_in_import_zip_id", string="Invoices In"
    )

    def action_view_xml(self):
        if self.env.context.get("xml_type") == "out_xml":
            attachments = self.mapped("attachment_out_ids")
            action = self.env.ref(
                "l10n_it_fatturapa_out.action_fatturapa_attachment"
            ).read()[0]
        elif self.env.context.get("xml_type") == "in_xml":
            attachments = self.mapped("attachment_in_ids")
            action = self.env.ref("l10n_it_fatturapa_in.action_fattura_pa_in").read()[0]
        else:
            return {"type": "ir.actions.act_window_close"}
        action["context"] = "{}"
        action["domain"] = [("id", "in", attachments.ids)]
        return action

    def action_view_invoices(self):
        if self.env.context.get("invoice_type") == "out_invoice":
            invoices = self.mapped("invoice_out_ids")
            action = self.env.ref("account.action_invoice_out_refund").read()[0]
            context = {
                "default_move_type": "out_invoice",
            }
        elif self.env.context.get("invoice_type") == "in_invoice":
            invoices = self.mapped("invoice_in_ids")
            action = self.env.ref("account.action_invoice_in_refund").read()[0]
            context = {
                "default_move_type": "in_invoice",
            }
        else:
            return {"type": "ir.actions.act_window_close"}
        action["context"] = context
        action["domain"] = [("id", "in", invoices.ids)]
        return action

    def _compute_invoices_data(self):
        for import_zip in self:
            import_zip.xml_out_count = len(import_zip.attachment_out_ids)
            import_zip.xml_in_count = len(import_zip.attachment_in_ids)
            import_zip.invoices_out_count = len(import_zip.invoice_out_ids)
            import_zip.invoices_in_count = len(import_zip.invoice_in_ids)
            import_zip.messages = "{}\n{}".format(
                "\n".join(
                    [
                        i
                        for i in import_zip.invoice_out_ids.mapped("inconsistencies")
                        if i
                    ]
                ),
                "\n".join(
                    [
                        i
                        for i in import_zip.invoice_in_ids.mapped("inconsistencies")
                        if i
                    ]
                ),
            )

    def action_import(self):
        self.ensure_one()
        tmp_dir_name = "/tmp/{}_{}".format(
            self.env.cr.dbname, datetime.now().timestamp()
        )
        if os.path.isdir(tmp_dir_name):
            shutil.rmtree(tmp_dir_name)
        os.mkdir(tmp_dir_name)
        zip_data = base64.b64decode(self.datas)
        zip_file_path = "%s/e_bills_to_import.zip" % tmp_dir_name
        with open(zip_file_path, "wb") as writer:
            writer.write(zip_data)
        tmp_dir_name_xml = tmp_dir_name + "/XML"
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(tmp_dir_name_xml)
        for xml_filename in os.listdir(tmp_dir_name_xml):
            with open("{}/{}".format(tmp_dir_name_xml, xml_filename), "rb") as reader:
                content = reader.read()
            attach_vals = {
                "name": xml_filename,
                "datas": base64.encodebytes(content),
            }
            att_in = self.env["fatturapa.attachment.in"].create(attach_vals)
            if att_in.xml_supplier_id.id == self.env.user.company_id.partner_id.id:
                att_in.unlink()
                attach_vals["state"] = "validated"
                att_out = self.env["fatturapa.attachment.out"].create(attach_vals)
                att_out._import_e_invoice_out()
                att_out.attachment_import_zip_id = self.id
            else:
                in_invoice_registration_date = (
                    self.env.user.company_id.in_invoice_registration_date
                )
                # we don't have the received date
                self.env.user.company_id.in_invoice_registration_date = "inv_date"
                att_in.attachment_import_zip_id = self.id
                wizard = (
                    self.env["wizard.import.fatturapa"]
                    .with_context(
                        active_ids=[att_in.id], active_model="fatturapa.attachment.in"
                    )
                    .create({})
                )
                wizard.importFatturaPA()
                att_in.attachment_import_zip_id = self.id
                self.env.user.company_id.in_invoice_registration_date = (
                    in_invoice_registration_date
                )
        if os.path.isdir(tmp_dir_name):
            shutil.rmtree(tmp_dir_name)
        self.state = "done"


class FatturaPAAttachmentIn(models.Model):
    _inherit = "fatturapa.attachment.in"

    attachment_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-bill ZIP import",
        readonly=True,
        ondelete="restrict",
    )


class FatturaPAAttachmentOut(models.Model):
    _inherit = "fatturapa.attachment.out"

    attachment_import_zip_id = fields.Many2one(
        "fatturapa.attachment.import.zip",
        "E-bill ZIP import",
        readonly=True,
        ondelete="restrict",
    )

    def getCessComm(self, CessComm):
        """
        Get cessionario committente present in the xml and
        update it if 'electronic_invoice_no_contact_update' is False.
        :param CessComm: the current cessionario committente
        :return: partner_id
        """

        wizard_import = self.env["wizard.import.fatturapa"]
        partner_model = self.env["res.partner"]
        partner_id = wizard_import.getPartnerBase(CessComm.DatiAnagrafici)
        no_contact_update = False
        if partner_id:
            no_contact_update = partner_model.browse(
                partner_id
            ).electronic_invoice_no_contact_update
        if partner_id and not no_contact_update:
            vals = {
                "street": " ".join(
                    map(
                        str,
                        filter(
                            None, (CessComm.Sede.Indirizzo, CessComm.Sede.NumeroCivico)
                        ),
                    )
                ),
                "zip": CessComm.Sede.CAP,
                "city": CessComm.Sede.Comune,
            }
            if CessComm.Sede.Provincia:
                Provincia = CessComm.Sede.Provincia
                prov_sede = wizard_import.ProvinceByCode(Provincia)
                if not prov_sede:
                    wizard_import.log_inconsistency(
                        _("Province ( %s ) not present in your system") % Provincia
                    )
                else:
                    vals["state_id"] = prov_sede[0].id
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def get_sale_journal(self, company):
        journal_model = self.env["account.journal"]
        journals = journal_model.search(
            [("type", "=", "sale"), ("company_id", "=", company.id)], limit=1
        )
        if not journals:
            raise UserError(
                _("Define a purchase journal " "for this company: '%s' (id: %d).")
                % (company.name, company.id)
            )
        return journals[0]

    def get_account_taxes(self, AliquotaIVA, Natura):
        account_tax_model = self.env["account.tax"]
        wizard_import = self.env["wizard.import.fatturapa"]
        ir_values = self.env["ir.default"]
        company_id = self.env.user.company_id.id
        taxes_ids = ir_values.get("product.product", "taxes_id", company_id=company_id)
        def_tax = False
        if taxes_ids:
            def_tax = account_tax_model.browse(taxes_ids, limit=1)
        if float(AliquotaIVA) == 0.0 and Natura:
            account_taxes = account_tax_model.search(
                [
                    ("type_tax_use", "=", "sale"),
                    ("kind_id.code", "=", Natura),
                    ("amount", "=", 0.0),
                ],
                order="sequence",
            )
            if not account_taxes:
                wizard_import.log_inconsistency(
                    _(
                        "No tax with percentage "
                        "%s and nature %s found. Please configure this tax."
                    )
                    % (AliquotaIVA, Natura)
                )
            if len(account_taxes) > 1:
                wizard_import.log_inconsistency(
                    _(
                        "Too many taxes with percentage "
                        "%s and nature %s found. Tax %s with lower priority has "
                        "been set on invoice lines."
                    )
                    % (AliquotaIVA, Natura, account_taxes[0].description)
                )
        else:
            account_taxes = account_tax_model.search(
                [
                    ("type_tax_use", "=", "sale"),
                    ("amount", "=", float(AliquotaIVA)),
                    ("price_include", "=", False),
                    ("children_tax_ids", "=", False),
                ],
                order="sequence",
            )
            if not account_taxes:
                wizard_import.log_inconsistency(
                    _(
                        "XML contains tax with percentage '%s' "
                        "but it does not exist in your system"
                    )
                    % AliquotaIVA
                )
            if len(account_taxes) > 1:
                if def_tax and def_tax.amount == (float(AliquotaIVA)):
                    account_taxes = def_tax
        return account_taxes

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_taxes = self.get_account_taxes(line.AliquotaIVA, line.Natura)
        if account_taxes:
            retLine["invoice_line_tax_ids"] = [(6, 0, [account_taxes[0].id])]
        return retLine

    def _prepareInvoiceLine(self, debit_account_id, line):
        wizard_import = self.env["wizard.import.fatturapa"]
        retLine = self._prepare_generic_line_data(line)
        retLine.update(
            {
                "name": line.Descrizione,
                "sequence": int(line.NumeroLinea),
                "account_id": debit_account_id,
                "price_unit": float(line.PrezzoUnitario),
            }
        )
        if line.Quantita is None:
            retLine["quantity"] = 1.0
        else:
            retLine["quantity"] = float(line.Quantita)
        if (
            float(line.PrezzoUnitario)
            and line.Quantita
            and float(line.Quantita)
            and line.ScontoMaggiorazione  # Quantita not required
        ):
            retLine["discount"] = wizard_import._computeDiscount(line)
        if line.RiferimentoAmministrazione:
            retLine["admin_ref"] = line.RiferimentoAmministrazione
        return retLine

    def get_line_product(self, line, partner):
        product = self.env["product.product"].browse()

        product_model = self.env["product.product"]
        found_products = product_model.browse()
        if len(line.CodiceArticolo or []) == 1:
            prod_code = line.CodiceArticolo[0].CodiceValore
            found_products = product_model.search(
                [
                    ("default_code", "=", prod_code),
                ]
            )
        if not found_products:
            prod_name = line.Descrizione
            found_products = product_model.search(
                [
                    ("default_code", "=", prod_name),
                ]
            )

        if found_products:
            products = found_products.mapped("product_id")
            if len(products) == 1:
                product = first(products)
            else:
                templates = products.mapped("product_tmpl_id")
                if len(templates) == 1:
                    product = templates.product_variant_id

        if not product and partner.e_invoice_default_product_id:
            product = partner.e_invoice_default_product_id
        return product

    def adjust_accounting_data(self, product, line_vals):
        wizard_import = self.env["wizard.import.fatturapa"]
        if product.product_tmpl_id.property_account_income_id:
            line_vals[
                "account_id"
            ] = product.product_tmpl_id.property_account_income_id.id
        elif product.product_tmpl_id.categ_id.property_account_income_categ_id:
            line_vals[
                "account_id"
            ] = product.product_tmpl_id.categ_id.property_account_income_categ_id.id
        account = self.env["account.account"].browse(line_vals["account_id"])

        new_tax = None
        if len(product.product_tmpl_id.taxes_id) == 1:
            new_tax = product.product_tmpl_id.taxes_id[0]
        elif len(account.tax_ids) == 1:
            new_tax = account.tax_ids[0]
        line_tax_id = line_vals.get("invoice_line_tax_ids")\
            and line_vals["invoice_line_tax_ids"][0][2][0]
        line_tax = self.env["account.tax"].browse(line_tax_id)
        if new_tax and line_tax and new_tax != line_tax:
            if new_tax._get_tax_amount() != line_tax._get_tax_amount():
                wizard_import.log_inconsistency(
                    _(
                        "XML contains tax %s. Product %s has tax %s. Using "
                        "the XML one"
                    )
                    % (line_tax.name, product.name, new_tax.name)
                )
            else:
                # If product has the same amount of the one in XML,
                # I use it. Typical case: 22% det 50%
                line_vals["invoice_line_tax_ids"] = [(6, 0, [new_tax.id])]

    def _set_invoice_lines(
        self, product, invoice_line_data, invoice_lines, invoice_line_model
    ):
        if product:
            invoice_line_data["product_id"] = product.id
            self.adjust_accounting_data(product, invoice_line_data)

        invoice_line_id = invoice_line_model.create(
            invoice_line_data).id
        invoice_lines.append(invoice_line_id)

    def set_invoice_line_ids(self, FatturaBody, debit_account_id, partner, wt_founds,
                             invoice_data):
        invoice_lines = []
        invoice_line_model = self.env["account.invoice.line"]
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            invoice_line_data = self._prepareInvoiceLine(debit_account_id, line)

            product = self.get_line_product(line, partner)
            self._set_invoice_lines(
                product, invoice_line_data, invoice_lines, invoice_line_model
            )
        invoice_data['invoice_line_ids'] = [(6, 0, invoice_lines)]

    def set_payments_data(self, FatturaBody, invoice, partner_id):
        wizard_import = self.env["wizard.import.fatturapa"]
        invoice_id = invoice.id
        PaymentsData = FatturaBody.DatiPagamento
        partner = self.env["res.partner"].browse(partner_id)
        if not partner.property_payment_term_id:
            due_dates = wizard_import._get_last_due_date(FatturaBody.DatiPagamento)
            if due_dates:
                self.env["account.invoice"].browse(
                    invoice_id
                ).date_due = due_dates[0]
        if PaymentsData:
            PaymentDataModel = self.env["fatturapa.payment.data"]
            PaymentTermsModel = self.env["fatturapa.payment_term"]
            for PaymentLine in PaymentsData:
                cond = PaymentLine.CondizioniPagamento or False
                if not cond:
                    raise UserError(_("Payment method code not found in document."))
                terms = PaymentTermsModel.search([("code", "=", cond)])
                if not terms:
                    raise UserError(_("Payment method code %s is incorrect.") % cond)
                else:
                    term_id = terms[0].id
                PayDataId = PaymentDataModel.create(
                    {"payment_terms": term_id, "invoice_id": invoice_id}
                ).id
                wizard_import._createPaymentsLine(
                    PayDataId, PaymentLine, partner_id, invoice
                )

    def set_attachments_data(self, FatturaBody, invoice):
        invoice_id = invoice.id
        AttachmentsData = FatturaBody.Allegati
        if AttachmentsData:
            AttachModel = self.env["fatturapa.attachments"]
            for attach in AttachmentsData:
                if not attach.NomeAttachment:
                    name = _("Attachment without name")
                else:
                    name = attach.NomeAttachment
                content = attach.Attachment.encode()
                _attach_dict = {
                    "name": name,
                    "datas": content,
                    "description": attach.DescrizioneAttachment or "",
                    "compression": attach.AlgoritmoCompressione or "",
                    "format": attach.FormatoAttachment or "",
                    "invoice_id": invoice_id,
                }
                AttachModel.create(_attach_dict)

    def invoiceCreate(self, fatt, fatturapa_attachment, FatturaBody, partner_id):
        partner_model = self.env["res.partner"]
        invoice_model = self.env["account.invoice"]
        currency_model = self.env["res.currency"]
        ftpa_doctype_model = self.env["fiscal.document.type"]
        wizard_import = self.env["wizard.import.fatturapa"]
        rel_docs_model = self.env["fatturapa.related_document_type"]

        company = self.env.user.company_id
        partner = partner_model.browse(partner_id)

        currency = currency_model.search(
            [("name", "=", FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa)]
        )
        if not currency:
            raise UserError(
                _(
                    "No currency found with code %s."
                    % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
                )
            )
        sale_journal = self.get_sale_journal(company)
        debit_account_id = sale_journal.default_debit_account_id.id
        comment = ""
        docType_id = False
        invtype = "out_invoice"
        docType = FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        if docType:
            docType_record = ftpa_doctype_model.search([("code", "=", docType)])
            if docType_record:
                docType_id = docType_record[0].id
            else:
                raise UserError(_("Document type %s not handled.") % docType)
            if docType == "TD04":
                invtype = "out_refund"

        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for caus in causLst:
                comment += caus + "\n"

        e_invoice_date = fields.Date.from_string(
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data)

        invoice_data = {
            "date_invoice": e_invoice_date,
            "name": FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero,
            "fiscal_document_type_id": docType_id,
            "sender": fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            "type": invtype,
            "partner_id": partner_id,
            "currency_id": currency[0].id,
            "journal_id": sale_journal.id,
            "fiscal_position_id": partner.property_account_position_id.id or False,
            "payment_term_id": partner.property_supplier_payment_term_id.id,
            "company_id": company.id,
            "fatturapa_attachment_out_id": fatturapa_attachment.id,
            "comment": comment,
        }
        wizard_import.set_art73(FatturaBody, invoice_data)

        Withholdings = FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta
        if Withholdings:
            wizard_import.log_inconsistency(
                _("Invoice %s: DatiRitenuta not handled")
                % FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero
            )

        wizard_import.set_e_invoice_lines(FatturaBody, invoice_data)
        invoice = invoice_model.create(invoice_data)
        invoice_lines = []
        wt_founds = []
        new_invoice_lines = self.set_invoice_line_ids(
            FatturaBody, debit_account_id, partner, wt_founds, invoice_data)
        if new_invoice_lines:
            invoice_lines.extend(new_invoice_lines)
        efatt_rounding = wizard_import.set_efatt_rounding(FatturaBody, invoice)
        if efatt_rounding:
            invoice_lines.extend(efatt_rounding)
        invoice.with_context(check_move_validity=False).update(
            {"invoice_line_ids": [(6, 0, invoice_lines)]}
        )
        invoice._onchange_invoice_line_wt_ids()
        invoice._onchange_payment_term_date_invoice()
        invoice.write(invoice._convert_to_write(invoice._cache))

        rel_docs_dict = {
            "order": FatturaBody.DatiGenerali.DatiOrdineAcquisto,
            "contract": FatturaBody.DatiGenerali.DatiContratto,
            "agreement": FatturaBody.DatiGenerali.DatiConvenzione,
            "reception": FatturaBody.DatiGenerali.DatiRicezione,
            "invoice": FatturaBody.DatiGenerali.DatiFattureCollegate,
        }

        for rel_doc_key, rel_doc_data in rel_docs_dict.items():
            if not rel_doc_data:
                continue
            for rel_doc in rel_doc_data:
                doc_datas = wizard_import._prepareRelDocsLine(
                    invoice.id, rel_doc, rel_doc_key
                )
                for doc_data in doc_datas:
                    # Note for v12: must take advantage of batch creation
                    rel_docs_model.create(doc_data)

        wizard_import.set_activity_progress(FatturaBody, invoice.id)
        wizard_import.set_ddt_data(FatturaBody, invoice.id)
        wizard_import.set_delivery_data(FatturaBody, invoice)
        wizard_import.set_summary_data(FatturaBody, invoice.id)
        wizard_import.set_parent_invoice_data(FatturaBody, invoice)
        wizard_import.set_vehicles_data(FatturaBody, invoice)
        self.set_payments_data(FatturaBody, invoice, partner_id)
        self.set_attachments_data(FatturaBody, invoice)
        invoice.compute_taxes()
        invoice.process_negative_lines()
        return invoice

    def get_xml_string(self):
        return self.ir_attachment_id.get_xml_string()

    def get_invoice_obj(self, fatturapa_attachment):
        xml_string = fatturapa_attachment.get_xml_string()
        return fatturapa.CreateFromDocument(xml_string)

    def _import_e_invoice_out(self):
        wizard_import = self.env["wizard.import.fatturapa"]
        for fatturapa_attachment in self:
            if fatturapa_attachment.out_invoice_ids:
                raise UserError(
                    _("File %s is linked to invoices yet.") % fatturapa_attachment.name
                )
            fatt = self.get_invoice_obj(fatturapa_attachment)
            cessionarioCommittente = (
                fatt.FatturaElettronicaHeader.CessionarioCommittente
            )
            partner_id = self.getCessComm(cessionarioCommittente)
            for fattura in fatt.FatturaElettronicaBody:
                invoice_id = self.invoiceCreate(
                    fatt, fatturapa_attachment, fattura, partner_id
                )
                wizard_import.check_invoice_amount(invoice_id, fattura)
                invoice_id.set_einvoice_data(fattura)
