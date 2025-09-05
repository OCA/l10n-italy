# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, html2plaintext

from odoo.addons.base.models.ir_qweb_fields import Markup
from odoo.addons.l10n_it_edi.models.account_move import get_date, get_float, get_text


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    l10n_it_edi_protocol_number = fields.Char(size=64, copy=False)
    l10n_it_edi_tax_representative_id = fields.Many2one(
        "res.partner", string="Tax Representative"
    )
    l10n_it_edi_sender = fields.Selection(
        [("CC", "Assignee / Partner"), ("TZ", "Third Person")], string="Sender"
    )
    l10n_it_edi_attachment_preview_link = fields.Char(
        string="Preview link",
        compute="_compute_l10n_it_edi_attachment_preview_link",
    )
    l10n_it_edi_line_ids = fields.One2many(
        "l10n_it_edi.line",
        "invoice_id",
        string="E-Invoice Lines",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_summary_ids = fields.One2many(
        "l10n_it_edi.summary_data",
        "invoice_id",
        string="E-Invoice Summary Data",
        copy=False,
    )
    l10n_it_edi_activity_progress_ids = fields.One2many(
        "l10n_it_edi.activity_progress",
        "invoice_id",
        string="E-Invoice Activity Progress",
        copy=False,
    )
    l10n_it_edi_rounding = fields.Float(
        string="Rounding",
        readonly=True,
        help="Possible total amount rounding on the document (negative sign allowed)",
        copy=False,
    )
    l10n_edi_it_art73 = fields.Boolean(
        string="Art. 73",
        readonly=True,
        help="Indicates whether the document has been issued according to "
        "methods and terms laid down in a ministerial decree under the "
        "terms of Article 73 of Italian Presidential Decree 633/72 (this "
        "enables the seller/provider to issue in the same year several "
        "documents with same number)",
        copy=False,
    )
    l10n_it_edi_related_invoice_code = fields.Char(
        string="Related Invoice Code", copy=False
    )
    l10n_it_edi_related_invoice_date = fields.Date(
        string="Related Invoice Date", copy=False
    )
    l10n_it_edi_stabile_organizzazione_indirizzo = fields.Char(
        string="Organization Address",
        help="The fields must be entered only when the seller/provider is "
        "non-resident, with a stable organization in Italy. Address of "
        "the stable organization in Italy (street name, square, etc.)",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_stabile_organizzazione_civico = fields.Char(
        string="Organization Street Number",
        help="Street number of the address (no need to specify if already "
        "present in the address field)",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_stabile_organizzazione_cap = fields.Char(
        string="Organization ZIP", help="ZIP Code", readonly=True, copy=False
    )
    l10n_it_edi_stabile_organizzazione_comune = fields.Char(
        string="Organization Municipality",
        help="Municipality or city to which the Stable Organization refers",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_stabile_organizzazione_provincia = fields.Char(
        string="Organization Province",
        help="Acronym of the Province to which the municipality indicated "
        "in the information element 1.2.3.4 <Comune> belongs. "
        "Must be filled if the information element 1.2.3.6 <Nazione> is "
        "equal to IT",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_stabile_organizzazione_nazione = fields.Char(
        string="Organization Country",
        help="Country code according to the ISO 3166-1 alpha-2 code standard",
        readonly=True,
        copy=False,
    )
    l10n_it_edi_amount_untaxed = fields.Monetary(
        string="E-Invoice Untaxed Amount", readonly=True
    )
    l10n_it_edi_amount_tax = fields.Monetary(
        string="E-Invoice Tax Amount", readonly=True
    )
    l10n_it_edi_amount_total = fields.Monetary(
        string="E-Invoice Total Amount",
        compute="_compute_l10n_it_amount_total",
        readonly=True,
    )
    l10n_it_edi_validation_message = fields.Text(
        compute="_compute_l10n_it_edi_validation_message"
    )

    # -------------------------------------------------------------------------
    # Computes
    # -------------------------------------------------------------------------

    @api.depends("l10n_it_edi_attachment_id")
    def _compute_l10n_it_edi_attachment_preview_link(self):
        for move in self:
            if move.l10n_it_edi_attachment_id:
                move.l10n_it_edi_attachment_preview_link = (
                    move.get_base_url()
                    + f"/fatturapa/preview/{move.l10n_it_edi_attachment_id.id}"
                )
            else:
                move.l10n_it_edi_attachment_preview_link = ""

    @api.depends(
        "l10n_it_edi_amount_untaxed", "l10n_it_edi_amount_tax", "l10n_it_edi_rounding"
    )
    def _compute_l10n_it_amount_total(self):
        for move in self:
            move.l10n_it_edi_amount_total = sum(
                [
                    move.l10n_it_edi_amount_untaxed,
                    move.l10n_it_edi_amount_tax,
                    move.l10n_it_edi_rounding,
                ]
            )

    @api.depends(
        "move_type",
        "state",
        "amount_untaxed",
        "amount_tax",
        "amount_total",
        "l10n_it_edi_attachment_id",
        "l10n_it_edi_amount_untaxed",
        "l10n_it_edi_amount_tax",
        "l10n_it_edi_rounding",
    )
    def _compute_l10n_it_edi_validation_message(self):
        self.l10n_it_edi_validation_message = ""

        invoices_to_check = self.filtered(
            lambda inv: inv.is_purchase_document()
            and inv.state in ["draft", "posted"]
            and inv.l10n_it_edi_attachment_id
        )
        for invoice in invoices_to_check:
            error_messages = list()

            if error_message := invoice._l10n_it_edi_check_amount_untaxed():
                error_messages.append(error_message)

            if error_message := invoice._l10n_it_edi_check_amount_tax():
                error_messages.append(error_message)

            if error_message := invoice._l10n_it_edi_check_amount_total():
                error_messages.append(error_message)

            if not error_messages:
                continue
            invoice.l10n_it_edi_validation_message = ",\n".join(error_messages) + "."

    # -------------------------------------------------------------------------
    # Business actions
    # -------------------------------------------------------------------------

    def action_l10n_it_edi_attachment_preview(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "name": "Show preview",
            "url": self.l10n_it_edi_attachment_preview_link,
            "target": "new",
        }

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _l10n_it_edi_add_base_lines_xml_values(
        self, base_lines_aggregated_values, is_downpayment
    ):
        res = super()._l10n_it_edi_add_base_lines_xml_values(
            base_lines_aggregated_values, is_downpayment
        )
        for base_line, _aggregated_values in base_lines_aggregated_values:
            line = base_line["record"]
            base_line["it_values"].update(
                {
                    "admin_ref": line.l10n_it_edi_admin_ref or None,
                }
            )
        return res

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)

        causale_list = []
        if self.narration:
            try:
                narration_text = html2plaintext(self.narration)
            except Exception:
                narration_text = ""

            # max length of Causale is 200
            for causale in narration_text.split("\n"):
                if not causale:
                    continue
                causale_list_200 = [
                    causale[i : i + 200] for i in range(0, len(causale), 200)
                ]
                for causale200 in causale_list_200:
                    causale_list.append(causale200)

        res["causale"] = causale_list

        return res

    def _l10n_it_edi_get_extra_info(
        self, company, document_type, body_tree, incoming=True
    ):
        extra_info, message_to_log = super()._l10n_it_edi_get_extra_info(
            company, document_type, body_tree, incoming=incoming
        )

        if sender := get_text(body_tree, "//SoggettoEmittente"):
            self.l10n_it_edi_sender = sender

        if elements_stabile_organizzazione := body_tree.xpath(
            "//StabileOrganizzazione"
        ):
            element_stabile_organizzazione = elements_stabile_organizzazione[0]
            self.update(
                {
                    "l10n_it_edi_stabile_organizzazione_indirizzo": get_text(
                        element_stabile_organizzazione, ".//Indirizzo"
                    ),
                    "l10n_it_edi_stabile_organizzazione_civico": get_date(
                        element_stabile_organizzazione, ".//NumeroCivico"
                    ),
                    "l10n_it_edi_stabile_organizzazione_cap": get_date(
                        element_stabile_organizzazione, ".//CAP"
                    ),
                    "l10n_it_edi_stabile_organizzazione_comune": get_date(
                        element_stabile_organizzazione, ".//Comune"
                    ),
                    "l10n_it_edi_stabile_organizzazione_provincia": get_date(
                        element_stabile_organizzazione, ".//Provincia"
                    ),
                    "l10n_it_edi_stabile_organizzazione_nazione": get_date(
                        element_stabile_organizzazione, ".//Nazione"
                    ),
                }
            )

        if rounding := get_float(body_tree, ".//DatiGeneraliDocumento/Arrotondamento"):
            self.l10n_it_edi_rounding = rounding

        if get_text(body_tree, "//DatiGeneraliDocumento/Art73"):
            self.l10n_edi_it_art73 = True

        if elements_sal := body_tree.xpath(".//DatiGenerali/DatiSAL"):
            self.env["l10n_it_edi.activity_progress"].create(
                [
                    {
                        "activity_progress": get_text(
                            element_sal, ".//RiferimentoFase"
                        ),
                        "invoice_id": self.id,
                    }
                    for element_sal in elements_sal
                ],
            )

        for xpath, label in [
            (
                ".//DatiGenerali/DatiTrasporto",
                self.env._("Transport informations from XML file:"),
            ),
            (".//DatiVeicoli", self.env._("Vehicle informations from XML file:")),
        ]:
            if body_tree.xpath(xpath):
                message = Markup("<br/>").join(
                    (label, self._compose_info_message(body_tree, xpath))
                )
                message_to_log.append(message)

        if elements_parent_invoice := body_tree.xpath(
            ".//DatiGenerali/FatturaPrincipale"
        ):
            for element_parent_invoice in elements_parent_invoice:
                self.write(
                    {
                        "l10n_it_edi_related_invoice_code": get_text(
                            element_parent_invoice, ".//NumeroFatturaPrincipale"
                        ),
                        "l10n_it_edi_related_invoice_date": get_date(
                            element_parent_invoice, ".//DataFatturaPrincipale"
                        ),
                    }
                )

        tag_name = (
            ".//DettaglioLinee"
            if not extra_info["simplified"]
            else ".//DatiBeniServizi"
        )
        if elements_line := body_tree.xpath(tag_name):
            for element_line in elements_line:
                self.l10n_it_edi_amount_untaxed += get_float(
                    element_line, ".//PrezzoTotale"
                )

        if elements_summary := body_tree.xpath(".//DatiBeniServizi/DatiRiepilogo"):
            self.env["l10n_it_edi.summary_data"].create(
                [
                    {
                        "tax_rate": get_float(element_summary, ".//AliquotaIVA"),
                        "non_taxable_nature": get_text(element_summary, ".//Natura"),
                        "incidental_charges": get_float(
                            element_summary, ".//SpeseAccessorie"
                        ),
                        "rounding": get_float(element_summary, ".//Arrotondamento"),
                        "amount_untaxed": get_float(
                            element_summary, ".//ImponibileImporto"
                        ),
                        "amount_tax": get_float(element_summary, ".//Imposta"),
                        "payability": get_text(element_summary, ".//EsigibilitaIVA"),
                        "law_reference": get_text(
                            element_summary, ".//RiferimentoNormativo"
                        ),
                        "invoice_id": self.id,
                    }
                    for element_summary in elements_summary
                ]
            )
            for element_summary in elements_summary:
                self.l10n_it_edi_amount_tax += get_float(element_summary, ".//Imposta")

        extra_info["l10n_it_edi_ext_body_tree"] = body_tree
        return extra_info, message_to_log

    def _l10n_it_edi_update_partner(self, xml_tree, role, partner):
        vals = self._l10n_it_edi_extension_prepare_partner_values(xml_tree, role)
        partner.update(vals)
        return partner

    def _l10n_it_edi_ext_import_summary_line(self, element, extra_info=None):
        messages_to_log = []
        company = self.company_id
        percentage = get_float(element, ".//AliquotaIVA")
        extra_domain = extra_info.get(
            "type_tax_use_domain", [("type_tax_use", "=", "purchase")]
        )
        l10n_it_exempt_reason = get_text(element, ".//Natura").upper() or False
        tax = self._l10n_it_edi_search_tax_for_import(
            company,
            percentage,
            extra_domain,
            l10n_it_exempt_reason=l10n_it_exempt_reason,
        )
        if tax:
            self.invoice_line_ids += self.env["account.move.line"].create(
                {
                    "move_id": self.id,
                    "name": self.env._(
                        "Summary for tax amount %(percentage)s",
                        percentage=percentage,
                    ),
                    "price_unit": get_float(element, ".//ImponibileImporto"),
                    "tax_ids": tax.ids,
                }
            )
        else:
            messages_to_log.append(
                Markup("<br/>").join(
                    (
                        self.env._(
                            "Tax not found for summary line "
                            "with percentage %(percentage)s.",
                            percentage=percentage,
                        ),
                        self._compose_info_message(element, "."),
                    )
                )
            )

        return messages_to_log

    def _l10n_it_edi_import_line(self, element, move_line, extra_info=None):
        if extra_info is None:
            extra_info = dict()
        messages_to_log = []
        company = move_line.company_id
        import_detail_level = (
            move_line.partner_id.l10n_it_edi_import_detail_level
            or company.l10n_it_edi_import_detail_level
        )
        if import_detail_level == "min":
            move_line.unlink()
            line_description = " ".join(get_text(element, ".//Descrizione").split())
            messages_to_log.append(
                Markup("<br/>").join(
                    (
                        self.env._(
                            "Line with description %(line_description)s "
                            "has been skipped "
                            "because import detail level is minimum.",
                            line_description=line_description,
                        ),
                        self._compose_info_message(element, "."),
                    )
                )
            )
        elif (
            body_tree := extra_info.get("l10n_it_edi_ext_body_tree")
        ) is not None and import_detail_level == "tax":
            move_line.unlink()
            tax_level_imported = extra_info.get("l10n_it_edi_ext_tax_level_imported")
            if not tax_level_imported:
                for summary_line in body_tree.xpath(".//DatiBeniServizi/DatiRiepilogo"):
                    messages_to_log += self._l10n_it_edi_ext_import_summary_line(
                        summary_line, extra_info=extra_info
                    )
                extra_info["l10n_it_edi_ext_tax_level_imported"] = True
        elif import_detail_level == "max":
            # Admin. ref.
            if admin_ref := get_text(element, ".//RiferimentoAmministrazione"):
                move_line.l10n_it_edi_admin_ref = admin_ref

            vals = {
                "line_number": int(get_text(element, ".//NumeroLinea")),
                "service_type": get_text(element, ".//TipoCessionePrestazione"),
                "name": " ".join(get_text(element, ".//Descrizione").split()),
                "qty": float(get_text(element, ".//Quantita") or 0),
                "uom": get_text(element, ".//UnitaMisura"),
                "period_start_date": get_date(element, ".//DataInizioPeriodo"),
                "period_end_date": get_date(element, ".//DataFinePeriodo"),
                "unit_price": get_float(element, ".//PrezzoUnitario"),
                "total_price": get_float(element, ".//PrezzoTotale"),
                "tax_amount": get_float(element, ".//AliquotaIVA"),
                "wt_amount": get_text(element, ".//Ritenuta"),
                "tax_kind": get_text(element, ".//Natura").upper(),
                "invoice_line_id": move_line.id,
                "invoice_id": move_line.move_id.id,
            }
            einvoice_line = self.env["l10n_it_edi.line"].create(vals)

            if elements_code := element.xpath(".//CodiceArticolo"):
                self.env["l10n_it_edi.article_code"].create(
                    [
                        {
                            "name": get_text(element_code, ".//CodiceTipo"),
                            "code_val": get_text(element_code, ".//CodiceValore"),
                            "l10n_it_edi_line_id": einvoice_line.id,
                        }
                        for element_code in elements_code
                    ]
                )

            if elements_discount := element.xpath(".//ScontoMaggiorazione"):
                self.env["l10n_it_edi.discount_rise_price"].create(
                    [
                        {
                            "name": get_text(element_discount, ".//Tipo"),
                            "percentage": get_float(element_discount, ".//Percentuale"),
                            "amount": get_float(element_discount, ".//Importo"),
                            "l10n_it_edi_line_id": einvoice_line.id,
                        }
                        for element_discount in elements_discount
                    ]
                )

            if elements_other_data := element.xpath(".//AltriDatiGestionali"):
                self.env["l10n_it_edi.line_other_data"].create(
                    [
                        {
                            "name": get_text(element_other_data, ".//TipoDato"),
                            "text_ref": get_text(
                                element_other_data, ".//RiferimentoTesto"
                            ),
                            "num_ref": get_float(
                                element_other_data, ".//RiferimentoNumero"
                            ),
                            "date_ref": get_date(
                                element_other_data, ".//RiferimentoData"
                            ),
                            "l10n_it_edi_line_id": einvoice_line.id,
                        }
                        for element_other_data in elements_other_data
                    ]
                )

            messages_to_log += super()._l10n_it_edi_import_line(
                element, move_line, extra_info=extra_info
            )
        else:
            raise UserError(
                self.env._(
                    "Import detail level %(import_detail_level)s not supported.\n"
                    "Please set an import detail level in company %(company)s.",
                    import_detail_level=import_detail_level,
                    company=company.name,
                )
            )
        return messages_to_log

    def _l10n_it_edi_ext_check_amount(self, amount, edi_amount, message):
        if (
            edi_amount
            and float_compare(
                amount,
                abs(edi_amount),
                precision_rounding=self.currency_id.rounding,
            )
            != 0
        ):
            return message

    def _l10n_it_edi_check_amount_untaxed(self):
        return self._l10n_it_edi_ext_check_amount(
            self.amount_untaxed - self.l10n_it_edi_rounding,
            self.l10n_it_edi_amount_untaxed,
            self.env._(
                "Untaxed amount (%(amount_untaxed)s}) "
                "minus rounding (%(rounding)s}) "
                "does not match with "
                "e-invoice untaxed amount %(edi_amount_untaxed)s)",
                amount_untaxed=self.amount_untaxed,
                rounding=self.l10n_it_edi_rounding,
                edi_amount_untaxed=self.l10n_it_edi_amount_untaxed,
            ),
        )

    def _l10n_it_edi_check_amount_tax(self):
        return self._l10n_it_edi_ext_check_amount(
            self.amount_tax,
            self.l10n_it_edi_amount_tax,
            self.env._(
                "Taxed amount (%(tax_amount)s}) "
                "does not match with "
                "e-invoice taxed amount (%(edi_tax_amount)s)",
                tax_amount=self.amount_tax,
                edi_tax_amount=self.l10n_it_edi_amount_tax,
            ),
        )

    def _l10n_it_edi_check_amount_total(self):
        return self._l10n_it_edi_ext_check_amount(
            self.amount_total,
            self.l10n_it_edi_amount_total,
            self.env._(
                "Total amount (%(total_amount)s) "
                "does not match with "
                "e-invoice total amount (%(edi_total_amount)s)",
                total_amount=self.amount_total,
                edi_total_amount=self.l10n_it_edi_amount_total,
            ),
        )

    def _l10n_it_edi_extend_partner_info(self, partner_role, partner_info):
        if partner_role == "buyer":
            partner_info_xpath = "//CessionarioCommittente"
        elif partner_role == "seller":
            partner_info_xpath = "//CedentePrestatore"
        elif partner_role == "tax_representative":
            partner_info_xpath = "//RappresentanteFiscale"
        else:
            raise UserError(
                self.env._(
                    "Role %(role)s is not supported for partner creation/update",
                    role=partner_role,
                )
            )

        partner_info.update(
            {
                "city_xpath": f"{partner_info_xpath}//Comune",
                "codice_fiscale_xpath": f"{partner_info_xpath}//CodiceFiscale",
                "country_code_xpath": f"{partner_info_xpath}//IdPaese",
                "email_xpath": f"{partner_info_xpath}//Email",
                "eori_code_xpath": f"{partner_info_xpath}//CodEORI",
                "first_name_xpath": f"{partner_info_xpath}//Nome",
                "last_name_xpath": f"{partner_info_xpath}//Cognome",
                "name_xpath": f"{partner_info_xpath}//Denominazione",
                "phone_xpath": f"{partner_info_xpath}//Telefono",
                "register_code_xpath": f"{partner_info_xpath}//NumeroIscrizioneAlbo",
                "register_regdate_xpath": f"{partner_info_xpath}//DataIscrizioneAlbo",
                "register_state_xpath": f"{partner_info_xpath}//ProvinciaAlbo",
                "register_xpath": f"{partner_info_xpath}//AlboProfessionale",
                "state_xpath": f"{partner_info_xpath}//Provincia",
                "street_number_xpath": f"{partner_info_xpath}//NumeroCivico",
                "street_xpath": f"{partner_info_xpath}//Indirizzo",
                "vat_xpath": f"{partner_info_xpath}//IdCodice",
                "zip_xpath": f"{partner_info_xpath}//CAP",
            }
        )

    @api.model
    def _l10n_it_buyer_seller_info(self):
        buyer_seller_info = super()._l10n_it_buyer_seller_info()
        for role, partner_info in buyer_seller_info.items():
            self._l10n_it_edi_extend_partner_info(role, partner_info)
        return buyer_seller_info

    def _l10n_it_edi_extension_get_partner_info_by_role(self, tree, role):
        if role in ("buyer", "seller"):
            buyer_seller_info = self._l10n_it_buyer_seller_info()
            partner_info = buyer_seller_info[role]
        else:
            partner_info = dict()
            self._l10n_it_edi_extend_partner_info(role, partner_info)
        return partner_info

    def _l10n_it_edi_extension_prepare_partner_values(self, tree, role):
        if partner_info := self._l10n_it_edi_extension_get_partner_info_by_role(
            tree, role
        ):
            vals = dict()
            for field_name, partner_info_xpath in [
                ("city", "city_xpath"),
                ("email", "email_xpath"),
                ("l10n_edi_it_eori_code", "eori_code_xpath"),
                ("l10n_edi_it_register_code", "register_code_xpath"),
                ("l10n_edi_it_register", "register_xpath"),
                ("l10n_edi_it_register_regdate", "register_regdate_xpath"),
                ("l10n_it_codice_fiscale", "codice_fiscale_xpath"),
                ("phone", "phone_xpath"),
                ("vat", "vat_xpath"),
                ("zip", "zip_xpath"),
            ]:
                if value := get_text(tree, partner_info[partner_info_xpath]):
                    vals[field_name] = value

            country_code = get_text(tree, partner_info["country_code_xpath"])
            if country := self.env["res.country"].search(
                [
                    ("code", "=", country_code),
                ],
                limit=1,
            ):
                vals["country_id"] = country.id

                if province := get_text(tree, partner_info["state_xpath"]):
                    if found_province := self.env["res.country.state"].search(
                        [
                            ("code", "=", province),
                            ("country_id", "=", country.id),
                        ],
                        limit=1,
                    ):
                        vals["state_id"] = found_province.id
                    else:
                        message = self.env._(
                            "Province (%(province)s) not present in your system",
                            province=province,
                        )
                        self.sudo().message_post(body=message)

                if register_province := get_text(
                    tree, partner_info["register_state_xpath"]
                ):
                    if found_province := self.env["res.country.state"].search(
                        [
                            ("code", "=", register_province),
                            ("country_id", "=", country.id),
                        ],
                        limit=1,
                    ):
                        vals["l10n_edi_it_register_province_id"] = found_province.id
                    else:
                        message = self.env._(
                            "Register Province (%(register_province)s) not present in "
                            "your system",
                            register_province=register_province,
                        )
                        self.sudo().message_post(body=message)

            if address_parts := list(
                filter(
                    None,
                    [
                        get_text(tree, partner_info["street_xpath"]),
                        get_text(tree, partner_info["street_number_xpath"]),
                    ],
                )
            ):
                vals["street"] = " ".join(address_parts)

            if name := get_text(tree, partner_info["name_xpath"]):
                vals["name"] = name
                vals["is_company"] = True
            if first_name := get_text(tree, partner_info["first_name_xpath"]):
                vals["firstname"] = first_name
            if last_name := get_text(tree, partner_info["last_name_xpath"]):
                vals["lastname"] = last_name
        else:
            vals = dict()
        return vals

    def _l10n_it_edi_extension_create_partner(self, invoice_data, role):
        partner_values = self._l10n_it_edi_extension_prepare_partner_values(
            invoice_data,
            role,
        )
        if partner_values:
            partner = self.env["res.partner"].create(partner_values)
        else:
            partner = self.env["res.partner"].browse()
        return partner

    def _l10n_it_edi_import_invoice(self, invoice, data, is_new):
        invoice = super()._l10n_it_edi_import_invoice(invoice, data, is_new)

        body_tree = data["xml_tree"]
        is_incoming = self.is_purchase_document(include_receipts=True)
        partner_role = "seller" if is_incoming else "buyer"
        if (
            invoice
            and invoice.partner_id
            and not invoice.partner_id.l10n_edi_it_electronic_invoice_no_contact_update
        ):
            self._l10n_it_edi_update_partner(
                body_tree, partner_role, invoice.partner_id
            )
        elif (
            invoice
            and not invoice.partner_id
            and self.env.company.l10n_edi_it_create_partner
        ):
            invoice.partner_id = self._l10n_it_edi_extension_create_partner(
                body_tree,
                partner_role,
            )

        if tax_representative := self._l10n_it_edi_extension_create_partner(
            body_tree,
            "tax_representative",
        ):
            invoice.l10n_it_edi_tax_representative_id = tax_representative

        return invoice
