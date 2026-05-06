# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# Copyright 2025 Simone Rubino
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, osv
from odoo.exceptions import UserError
from odoo.tools import float_compare, html2plaintext, is_html_empty

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
    l10n_it_edi_ext_attachment_in_id = fields.Many2one(
        comodel_name="ir.attachment",
        string="Imported Electronic Bill",
        readonly=True,
    )
    l10n_it_edi_ext_attachment_in_preview_link = fields.Char(
        string="Preview link for imported Electronic Bill",
        compute="_compute_l10n_it_edi_ext_attachment_in_preview_link",
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

    @api.depends("l10n_it_edi_ext_attachment_in_id")
    def _compute_l10n_it_edi_ext_attachment_in_preview_link(self):
        for move in self:
            if attachment := move.l10n_it_edi_ext_attachment_in_id:
                link = f"{move.get_base_url()}/fatturapa/preview/{attachment.id}"
            else:
                link = ""
            move.l10n_it_edi_ext_attachment_in_preview_link = link

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

    def _l10n_it_edi_is_to_validate(self):
        self.ensure_one()
        return (
            self.is_purchase_document()
            or self.env.context.get("l10n_it_validate_all_invoices")
            and self.is_sale_document()
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
            lambda inv: inv._l10n_it_edi_is_to_validate()
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

    def action_l10n_it_edi_ext_attachment_in_preview(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "name": "Show preview",
            "url": self.l10n_it_edi_ext_attachment_in_preview_link,
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
            # Build other_data list from l10n_it_edi_other_data_ids
            other_data_list = []
            for other_data in line.l10n_it_edi_other_data_ids:
                other_data_dict = {
                    "tipo_dato": other_data.name,
                    "riferimento_testo": other_data.text_ref or False,
                    "riferimento_numero": other_data.num_ref or False,
                    # Pass date object directly, format_date() in template handles it
                    "riferimento_data": other_data.date_ref or False,
                }
                other_data_list.append(other_data_dict)

            # Get existing altri_dati_gestionali_list or initialize empty list
            existing_list = base_line["it_values"].get("altri_dati_gestionali_list", [])
            base_line["it_values"].update(
                {
                    "admin_ref": line.l10n_it_edi_admin_ref or None,
                    "altri_dati_gestionali_list": existing_list + other_data_list,
                }
            )
        return res

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)

        causale_lines = []
        if not is_html_empty(self.narration):
            try:
                narration_text = html2plaintext(self.narration)
            except Exception:
                narration_text = ""

            # max length of Causale is 200
            for line in narration_text.splitlines():
                if line.strip():
                    causale_lines.extend(
                        line[i : i + 200] for i in range(0, len(line), 200)
                    )

        res["causale_lines"] = causale_lines

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
        amount_untaxed = sum(
            get_float(element_line, ".//PrezzoTotale")
            for element_line in body_tree.xpath(tag_name)
        )

        amount_tax = 0.0
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
            amount_tax = sum(
                get_float(element_summary, ".//Imposta")
                for element_summary in elements_summary
            )

        # Single batch write replaces N+M per-iteration writes from the
        # previous "self.field += value" accumulation loops.
        # skip_invoice_sync avoids _sync_dynamic_lines firing on a write
        # that only touches XML-derived header amounts.
        if amount_untaxed or amount_tax:
            self.with_context(skip_invoice_sync=True).write(
                {
                    "l10n_it_edi_amount_untaxed": amount_untaxed,
                    "l10n_it_edi_amount_tax": amount_tax,
                }
            )

        return extra_info, message_to_log

    @api.model
    def _l10n_it_edi_extension_core_partner_fields(self):
        """Return partner fields core writes during FatturaPA import.

        Override this hook when another module starts (or stops) writing
        a partner field through core's ``_l10n_it_edi_import_partner``,
        so that ``_l10n_it_edi_update_partner`` keeps respecting core.
        """
        return {
            "name",
            "vat",
            "email",
            "phone",
            "street",
            "street2",
            "zip",
            "city",
            "country_id",
            "is_company",
            "l10n_it_codice_fiscale",
        }

    def _l10n_it_edi_update_partner(self, xml_tree, role, partner):
        """Fill on ``partner`` the FatturaPA fields core does not handle.

        Core writes the basic identity and address block. Drop those
        keys from the prepared values so they stay as core wrote them,
        and write the FatturaPA extras (state_id, EORI, professional
        register data, firstname/lastname split).
        """
        vals = self._l10n_it_edi_extension_prepare_partner_values(xml_tree, role)
        for field_name in self._l10n_it_edi_extension_core_partner_fields():
            vals.pop(field_name, None)
        if vals:
            partner.update(vals)
        return partner

    def _l10n_it_edi_search_tax_for_import(
        self,
        company,
        percentage,
        extra_domain=None,
        l10n_it_exempt_reason=None,
        **kwargs,
    ):
        # Check if a tax of the default product fits what is requested
        partner_default_product = self.partner_id.l10n_it_edi_ext_default_product_id
        if default_product_taxes := partner_default_product.supplier_taxes_id:
            product_extra_domain = osv.expression.AND(
                [
                    extra_domain,
                    [
                        ("id", "in", default_product_taxes.ids),
                    ],
                ]
            )
            tax = super()._l10n_it_edi_search_tax_for_import(
                company,
                percentage,
                product_extra_domain,
                l10n_it_exempt_reason=l10n_it_exempt_reason,
                **kwargs,
            )
            if not tax:
                tax = super()._l10n_it_edi_search_tax_for_import(
                    company,
                    percentage,
                    extra_domain,
                    l10n_it_exempt_reason=l10n_it_exempt_reason,
                    **kwargs,
                )
        else:
            tax = super()._l10n_it_edi_search_tax_for_import(
                company,
                percentage,
                extra_domain,
                l10n_it_exempt_reason=l10n_it_exempt_reason,
                **kwargs,
            )
        return tax

    def _l10n_it_edi_ext_import_summary_line(self, element, extra_info=None):
        messages_to_log = []
        if extra_info is None:
            extra_info = {}
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
            line_values = {
                "move_id": self.id,
                "name": self.env._(
                    "Summary for tax amount %(percentage)s",
                    percentage=percentage,
                ),
                "price_unit": get_float(element, ".//ImponibileImporto"),
                "tax_ids": tax.ids,
            }
            if (
                partner_default_product
                := self.partner_id.l10n_it_edi_ext_default_product_id
            ):
                line_values["product_id"] = partner_default_product.id
            self.env["account.move.line"].create(line_values)
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
        partner = move_line.partner_id
        import_detail_level = (
            partner.l10n_it_edi_import_detail_level
            or company.l10n_it_edi_import_detail_level
        )
        if import_detail_level == "min":
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
        elif import_detail_level == "tax":
            # Lines will be replaced with summary lines in _l10n_it_edi_import_invoice
            line_description = " ".join(get_text(element, ".//Descrizione").split())
            messages_to_log.append(
                Markup("<br/>").join(
                    (
                        self.env._(
                            "Line with description %(line_description)s "
                            "has been replaced by summary line "
                            "because import detail level is tax.",
                            line_description=line_description,
                        ),
                        self._compose_info_message(element, "."),
                    )
                )
            )
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
            if not move_line.product_id and (
                partner_default_product := partner.l10n_it_edi_ext_default_product_id
            ):
                # If no product is found use the default one set on the partner,
                # without recomputing what was assigned
                with self.env.protecting(
                    [
                        move_line._fields[field_name]
                        for field_name in [
                            "price_unit",
                            "tax_ids",
                        ]
                    ],
                    move_line,
                ):
                    move_line.product_id = partner_default_product

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
        """Return a partner for ``role``, looking up an existing one first.

        Used for roles core does not handle (e.g. ``RappresentanteFiscale``).
        Follows the path core uses for buyer/seller: match by Italian
        Codice Fiscale, then delegate to ``_l10n_it_edi_import_partner``
        which calls ``_retrieve_partner`` and creates a new partner when
        nothing matches. ``_l10n_it_edi_update_partner`` fills the
        FatturaPA extras (state_id, EORI, Albo*, firstname/lastname)
        on top.
        """
        Partner = self.env["res.partner"]
        partner_values = self._l10n_it_edi_extension_prepare_partner_values(
            invoice_data,
            role,
        )
        if not partner_values:
            return Partner
        company = self.env.company
        codice_fiscale = partner_values.get("l10n_it_codice_fiscale")
        partner = Partner
        if codice_fiscale:
            partner = Partner.with_company(company).search(
                [
                    *Partner._check_company_domain(company),
                    ("l10n_it_codice_fiscale", "=like", codice_fiscale),
                ],
                limit=1,
            )
        if not partner:
            partner, _logs = self._l10n_it_edi_import_partner(
                company_id=company,
                name=partner_values.get("name"),
                phone=partner_values.get("phone"),
                email=partner_values.get("email"),
                vat=partner_values.get("vat"),
                street=partner_values.get("street"),
                city=partner_values.get("city"),
                zip_code=partner_values.get("zip"),
            )
            if partner and codice_fiscale and not partner.l10n_it_codice_fiscale:
                partner.l10n_it_codice_fiscale = codice_fiscale
            if partner and not partner.country_id and partner_values.get("country_id"):
                partner.country_id = partner_values["country_id"]
        if partner:
            self._l10n_it_edi_update_partner(invoice_data, role, partner)
        return partner

    def _l10n_it_edi_extension_get_bank_partner(self, invoice):
        """Return the partner that owns the bank accounts in this FatturaPA.

        Mirrors core's ``_l10n_it_edi_import_partner_bank`` selection
        via ``is_outbound``/``is_inbound``: the invoice partner on
        outbound documents (in_invoice, out_refund), the company
        partner on inbound documents (out_invoice, in_refund). Empty
        recordset on any other move type skips the bank update.
        """
        if invoice.is_outbound(include_receipts=False):
            return invoice.partner_id
        if invoice.is_inbound(include_receipts=False):
            return invoice.company_id.partner_id
        return self.env["res.partner"]

    def _l10n_it_edi_extension_get_or_create_bank(self, bic, bank_name):
        """Return a ``res.bank`` matching ``bic`` or ``bank_name``.

        Search by BIC, then by name; create one when nothing matches.
        Returns empty when both inputs are empty.
        """
        ResBank = self.env["res.bank"]
        if not (bic or bank_name):
            return ResBank
        bank = ResBank
        if bic:
            bank = ResBank.search([("bic", "=", bic)], limit=1)
        if not bank and bank_name:
            bank = ResBank.search([("name", "=", bank_name)], limit=1)
        if not bank:
            bank = ResBank.create({"name": bank_name or bic, "bic": bic or False})
        return bank

    def _l10n_it_edi_extension_update_partner_bank(self, tree, invoice):
        """Fill bank_id and acc_holder_name on partner banks created on import.

        Core sets ``acc_number`` on ``res.partner.bank`` and stops there.
        FatturaPA carries ``BIC`` and ``IstitutoFinanziario`` inside each
        ``DatiPagamento/DettaglioPagamento`` plus ``Beneficiario`` at the
        ``DatiPagamento`` level. Map them to ``res.bank`` (creating it
        when missing) and link the record via ``bank_id``. Values already
        set on the partner bank stay untouched.

        ``_l10n_it_edi_extension_get_bank_partner`` picks the partner
        the same way core does. The search filters by company so banks
        from other companies cannot match.
        """
        if tree is None:
            return
        bank_partner = self._l10n_it_edi_extension_get_bank_partner(invoice)
        if not bank_partner:
            return
        PartnerBank = self.env["res.partner.bank"]
        bank_domain = [
            *PartnerBank._check_company_domain(invoice.company_id),
            ("partner_id", "child_of", bank_partner.commercial_partner_id.id),
        ]
        for payment_node in tree.xpath("//DatiPagamento"):
            holder = get_text(payment_node, "./Beneficiario") or False
            for detail_node in payment_node.xpath("./DettaglioPagamento"):
                iban = get_text(detail_node, "./IBAN")
                if not iban:
                    continue
                bic = get_text(detail_node, "./BIC") or False
                bank_name = get_text(detail_node, "./IstitutoFinanziario") or False
                if not (bic or bank_name or holder):
                    continue
                partner_bank = PartnerBank.search(
                    [*bank_domain, ("acc_number", "=", iban)],
                    limit=1,
                )
                if not partner_bank:
                    continue
                vals = {}
                if holder and not partner_bank.acc_holder_name:
                    vals["acc_holder_name"] = holder
                if (bic or bank_name) and not partner_bank.bank_id:
                    if bank := self._l10n_it_edi_extension_get_or_create_bank(
                        bic, bank_name
                    ):
                        vals["bank_id"] = bank.id
                if vals:
                    partner_bank.write(vals)

    def _l10n_it_edi_import_invoice(self, invoice, data, is_new):
        invoice = super()._l10n_it_edi_import_invoice(invoice, data, is_new)
        if not invoice:
            return invoice

        body_tree = data.get("xml_tree")
        is_incoming = self.is_purchase_document(include_receipts=True)
        import_detail_level = (
            invoice.partner_id.l10n_it_edi_import_detail_level
            or invoice.company_id.l10n_it_edi_import_detail_level
        )
        if import_detail_level == "min":
            # Delete all lines - Odoo creates them in the import loop
            # but we don't want any for minimum detail level
            invoice.invoice_line_ids.unlink()
        elif import_detail_level == "tax":
            # Delete all lines created by Odoo and create summary lines instead
            invoice.invoice_line_ids.unlink()
            if body_tree is not None:
                # Ignore these messages
                # because they have already been logged
                # when this method was executed during super's import
                extra_info, _messages = self._l10n_it_edi_get_extra_info(
                    invoice.company_id,
                    get_text(body_tree, "//DatiGeneraliDocumento/TipoDocumento"),
                    body_tree,
                    incoming=is_incoming,
                )
                for summary_line in body_tree.xpath(".//DatiBeniServizi/DatiRiepilogo"):
                    messages = invoice._l10n_it_edi_ext_import_summary_line(
                        summary_line,
                        extra_info=extra_info,
                    )
                    for message in messages:
                        invoice.sudo().message_post(body=message)

        partner_role = "seller" if is_incoming else "buyer"
        if invoice.partner_id:
            if not invoice.partner_id.l10n_edi_it_electronic_invoice_no_contact_update:
                # Core creates the partner; fill the FatturaPA extras core
                # leaves out (Provincia, EORI, Albo*, firstname/lastname) on
                # both pre-existing partners and partners core created.
                self._l10n_it_edi_update_partner(
                    body_tree, partner_role, invoice.partner_id
                )
            self._l10n_it_edi_extension_update_partner_bank(body_tree, invoice)

        if tax_representative := self._l10n_it_edi_extension_create_partner(
            body_tree,
            "tax_representative",
        ):
            invoice.l10n_it_edi_tax_representative_id = tax_representative

        if attachment := data["attachment"]:
            invoice.l10n_it_edi_ext_attachment_in_id = attachment.id

        return invoice
