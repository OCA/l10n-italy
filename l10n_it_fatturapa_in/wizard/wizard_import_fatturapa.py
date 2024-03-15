#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re
from datetime import datetime

from odoo import api, fields, models, registry
from odoo.exceptions import UserError
from odoo.fields import first
from odoo.osv import expression
from odoo.tools import float_is_zero, frozendict
from odoo.tools.translate import _

from odoo.addons.base_iban.models.res_partner_bank import pretty_iban

_logger = logging.getLogger(__name__)

WT_CODES_MAPPING = {
    "RT01": "ritenuta",
    "RT02": "ritenuta",
    "RT03": "inps",
    "RT04": "enasarco",
    "RT05": "enpam",
    "RT06": "other",
}


class WizardImportFatturapa(models.TransientModel):
    _name = "wizard.import.fatturapa"
    _description = "Import E-bill"

    e_invoice_detail_level = fields.Selection(
        [
            ("0", "Minimum"),
            ("1", "Tax rate"),
            ("2", "Maximum"),
        ],
        string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
        "User will have to create them, according to what specified in "
        "the electronic bill.\n"
        "Tax rate level: Rate level: an invoice line is created for each "
        "rate present in the electronic invoice\n"
        "Maximum level: every line contained in the electronic bill "
        "will create a line in the bill.",
        required=True,
    )
    price_decimal_digits = fields.Integer(
        "Prices decimal digits",
        required=True,
        help="Decimal digits used in prices computation. This is needed to correctly "
        "import e-invoices with many decimal digits, not being forced to "
        "increase decimal digits of all your prices. "
        'Otherwise, increase "Product Price" precision.',
    )
    quantity_decimal_digits = fields.Integer(
        "Quantities decimal digits",
        required=True,
        help='Decimal digits used for quantity field. See "Prices decimal digits".',
    )
    discount_decimal_digits = fields.Integer(
        "Discounts decimal digits",
        required=True,
        help='Decimal digits used for discount field. See "Prices decimal digits".',
    )

    def _get_selected_model(self):
        context = self.env.context
        model_name = context.get("active_model")
        return model_name

    def _get_selected_records(self):
        context = self.env.context
        ids = context.get("active_ids", [])
        model_name = self._get_selected_model()
        attachments = self.env[model_name].browse(ids)
        return attachments

    def _check_attachment(self, attachment):
        if attachment.in_invoice_ids:
            raise UserError(_("File %s is linked to bills yet.", attachment.name))

    def _extract_supplier(self, fatturapa_attachment):
        return fatturapa_attachment.xml_supplier_id

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res["price_decimal_digits"] = self.env["decimal.precision"].precision_get(
            "Product Price"
        )
        res["quantity_decimal_digits"] = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        res["discount_decimal_digits"] = self.env["decimal.precision"].precision_get(
            "Discount"
        )
        res["e_invoice_detail_level"] = "2"

        fatturapa_attachments = self._get_selected_records()
        partners = self.env["res.partner"].browse()
        for fatturapa_attachment in fatturapa_attachments:
            self._check_attachment(fatturapa_attachment)
            partners |= self._extract_supplier(fatturapa_attachment)
            if len(partners) == 1:
                res["e_invoice_detail_level"] = partners[0].e_invoice_detail_level
                if partners[0].e_invoice_price_decimal_digits >= 0:
                    res["price_decimal_digits"] = partners[
                        0
                    ].e_invoice_price_decimal_digits
                if partners[0].e_invoice_quantity_decimal_digits >= 0:
                    res["quantity_decimal_digits"] = partners[
                        0
                    ].e_invoice_quantity_decimal_digits
                if partners[0].e_invoice_discount_decimal_digits >= 0:
                    res["discount_decimal_digits"] = partners[
                        0
                    ].e_invoice_discount_decimal_digits
        return res

    def CountryByCode(self, CountryCode):
        country_model = self.env["res.country"]
        return country_model.search([("code", "=", CountryCode)])

    def ProvinceByCode(self, provinceCode):
        province_model = self.env["res.country.state"]
        return province_model.search(
            [("code", "=", provinceCode), ("country_id.code", "=", "IT")]
        )

    def reset_inconsistencies(self):
        """
        Clean all existing inconsistencies.
        Note that inconsistencies are in all environments.
        """
        for env in self.env.all.envs:
            env_context = dict(env.context)
            env_context.pop("inconsistencies", None)
            env.context = frozendict(env_context)

    def get_inconsistencies(self):
        """
        Get all existing inconsistencies.
        """
        return self.env.context.get("inconsistencies", "")

    def log_inconsistency(self, message):
        """
        Add `message` to existing inconsistencies.
        Note that inconsistencies are in all environments.
        """
        inconsistencies = self.get_inconsistencies()
        if message not in inconsistencies:
            if inconsistencies:
                inconsistencies += "\n"
            inconsistencies += message
            # we can't set
            # self = self.with_context(inconsistencies=inconsistencies)
            # because self is a locale variable.
            # Environments are weakly referenced,
            # so they might disappear if they are no more referenced.
            # Save the inconsistencies in all the environments
            # to avoid losing them.
            for env in self.env.all.envs:
                env_context = dict(env.context)
                env_context.setdefault("inconsistencies", inconsistencies)
                env.context = frozendict(env_context)

    def check_partner_base_data(self, partner_id, DatiAnagrafici):
        partner = self.env["res.partner"].browse(partner_id)
        if (
            DatiAnagrafici.Anagrafica.Denominazione
            and partner.name != DatiAnagrafici.Anagrafica.Denominazione
        ):
            self.log_inconsistency(
                _(
                    "Company Name field contains '%(name)s'."
                    " Your System contains '%(partner)s'"
                )
                % {
                    "name": DatiAnagrafici.Anagrafica.Denominazione,
                    "partner": partner.name,
                }
            )
        if (
            DatiAnagrafici.Anagrafica.Nome
            and partner.firstname != DatiAnagrafici.Anagrafica.Nome
        ):
            self.log_inconsistency(
                _(
                    "Name field contains '%(name)s'."
                    " Your System contains '%(firstname)s'"
                )
                % {
                    "name": DatiAnagrafici.Anagrafica.Nome,
                    "firstname": partner.firstname,
                }
            )
        if (
            DatiAnagrafici.Anagrafica.Cognome
            and partner.lastname != DatiAnagrafici.Anagrafica.Cognome
        ):
            self.log_inconsistency(
                _(
                    "Surname field contains '%(surname)s'."
                    " Your System contains '%(lastname)s'"
                )
                % {
                    "surname": DatiAnagrafici.Anagrafica.Cognome,
                    "lastname": partner.lastname,
                }
            )

    def getPartnerBase(self, DatiAnagrafici):  # noqa: C901
        if not DatiAnagrafici:
            return False
        partner_model = self.env["res.partner"]
        cf = DatiAnagrafici.CodiceFiscale or False
        vat = False
        if DatiAnagrafici.IdFiscaleIVA:
            id_paese = DatiAnagrafici.IdFiscaleIVA.IdPaese.upper()
            id_codice = re.sub(r"\W+", "", DatiAnagrafici.IdFiscaleIVA.IdCodice).upper()
            # Format Italian VAT ID to always have 11 char
            # to avoid validation error when creating the given partner
            if id_paese == "IT" and not id_codice.startswith("IT"):
                vat = "IT{}".format(id_codice.rjust(11, "0")[:11])
            # XXX maybe San Marino needs special formatting too?
            else:
                vat = id_codice
        partners = partner_model
        res_partner_rule = self.sudo().env.ref(
            "base.res_partner_rule", raise_if_not_found=False
        )
        if vat:
            domain = [("vat", "=", vat)]
            if (
                self.env.context.get("from_attachment")
                and res_partner_rule
                and res_partner_rule.active
            ):
                att = self.env.context.get("from_attachment")
                domain.extend(
                    [
                        "|",
                        ("company_id", "child_of", att.company_id.id),
                        ("company_id", "=", False),
                    ]
                )
            partners = partner_model.search(domain)
        if not partners and cf:
            domain = [("fiscalcode", "=", cf)]
            if (
                self.env.context.get("from_attachment")
                and res_partner_rule
                and res_partner_rule.active
            ):
                att = self.env.context.get("from_attachment")
                domain.extend(
                    [
                        "|",
                        ("company_id", "child_of", att.company_id.id),
                        ("company_id", "=", False),
                    ]
                )
            partners = partner_model.search(domain)
        commercial_partner_id = False
        if len(partners) > 1:
            for partner in partners:
                if (
                    commercial_partner_id
                    and partner.commercial_partner_id.id != commercial_partner_id
                ):
                    self.log_inconsistency(
                        _(
                            "Two distinct partners with "
                            "VAT number %(vat)s or Fiscal Code %(fiscalcode)s already "
                            "present in db."
                        )
                        % {"vat": vat, "fiscalcode": cf}
                    )
                    return False
                commercial_partner_id = partner.commercial_partner_id.id
        if partners:
            if not commercial_partner_id:
                commercial_partner_id = partners[0].commercial_partner_id.id
            self.check_partner_base_data(commercial_partner_id, DatiAnagrafici)
            return commercial_partner_id
        else:
            # partner to be created
            country_id = False
            if DatiAnagrafici.IdFiscaleIVA:
                CountryCode = DatiAnagrafici.IdFiscaleIVA.IdPaese
                countries = self.CountryByCode(CountryCode)
                if countries:
                    country_id = countries[0].id
                else:
                    raise UserError(
                        _("Country Code %s not found in system.") % CountryCode
                    )
            vals = {
                "vat": vat,
                "fiscalcode": cf,
                "is_company": (
                    DatiAnagrafici.Anagrafica.Denominazione and True or False
                ),
                "eori_code": DatiAnagrafici.Anagrafica.CodEORI or "",
                "country_id": country_id,
            }
            if DatiAnagrafici.Anagrafica.Nome:
                vals["firstname"] = DatiAnagrafici.Anagrafica.Nome
            if DatiAnagrafici.Anagrafica.Cognome:
                vals["lastname"] = DatiAnagrafici.Anagrafica.Cognome
            if DatiAnagrafici.Anagrafica.Denominazione:
                vals["name"] = DatiAnagrafici.Anagrafica.Denominazione

            return partner_model.create(vals).id

    def getCedPrest(self, cedPrest):
        partner_model = self.env["res.partner"]
        # Assume that any non-IT VAT coming from SdI is correct
        partner_id = self.with_context(
            fatturapa_in_skip_no_it_vat_check=True,
        ).getPartnerBase(cedPrest.DatiAnagrafici)
        no_contact_update = False
        if partner_id:
            no_contact_update = partner_model.browse(
                partner_id
            ).electronic_invoice_no_contact_update
        fiscalPosModel = self.env["fatturapa.fiscal_position"]
        if partner_id and not no_contact_update:
            partner_company_id = partner_model.browse(partner_id).company_id.id
            vals = {
                "street": " ".join(
                    map(
                        str,
                        filter(
                            None, (cedPrest.Sede.Indirizzo, cedPrest.Sede.NumeroCivico)
                        ),
                    )
                ),
                "zip": cedPrest.Sede.CAP,
                "city": cedPrest.Sede.Comune,
                "register": cedPrest.DatiAnagrafici.AlboProfessionale or "",
            }
            if cedPrest.DatiAnagrafici.ProvinciaAlbo:
                ProvinciaAlbo = cedPrest.DatiAnagrafici.ProvinciaAlbo
                prov = self.ProvinceByCode(ProvinciaAlbo)
                if not prov:
                    self.log_inconsistency(
                        _("Register Province ( %s ) not present " "in your system")
                        % ProvinciaAlbo
                    )
                else:
                    vals["register_province"] = prov[0].id
            if cedPrest.Sede.Provincia:
                Provincia = cedPrest.Sede.Provincia
                prov_sede = self.ProvinceByCode(Provincia)
                if not prov_sede:
                    self.log_inconsistency(
                        _("Province ( %s ) not present in your system") % Provincia
                    )
                else:
                    vals["state_id"] = prov_sede[0].id

            vals["register_code"] = cedPrest.DatiAnagrafici.NumeroIscrizioneAlbo
            vals["register_regdate"] = cedPrest.DatiAnagrafici.DataIscrizioneAlbo

            if cedPrest.DatiAnagrafici.RegimeFiscale:
                rfPos = cedPrest.DatiAnagrafici.RegimeFiscale
                FiscalPos = fiscalPosModel.search([("code", "=", rfPos)])
                if not FiscalPos:
                    raise UserError(
                        _("Tax Regime %s not present in your system.") % rfPos
                    )
                else:
                    vals["register_fiscalpos"] = FiscalPos[0].id

            if cedPrest.IscrizioneREA:
                REA = cedPrest.IscrizioneREA
                offices = self.ProvinceByCode(REA.Ufficio)
                rea_nr = REA.NumeroREA

                if not offices:
                    office_id = False
                    self.log_inconsistency(
                        _(
                            "REA Office Province Code ( %s ) not present in "
                            "your system"
                        )
                        % REA.Ufficio
                    )
                else:
                    office_id = offices[0].id
                    vals["rea_office"] = office_id

                rea_domain = [
                    ("rea_code", "=", rea_nr),
                    ("company_id", "=", partner_company_id),
                    ("id", "!=", partner_id),
                ]
                if office_id:
                    rea_domain.append(("rea_office", "=", office_id))
                rea_partners = partner_model.search(rea_domain)
                if rea_partners:
                    rea_names = ", ".join(rea_partners.mapped("name"))
                    p_name = partner_model.browse(partner_id).name
                    self.log_inconsistency(
                        _(
                            "Current invoice is from %(partner)s with REA Code"
                            " %(code)s. Yet it seems that"
                            " partners %(partners)s have the same"
                            " REA Code. This code should be unique; please fix"
                            " it.",
                            partner=p_name,
                            code=rea_nr,
                            partners=rea_names,
                        )
                    )
                else:
                    vals["rea_code"] = REA.NumeroREA

                vals["rea_capital"] = REA.CapitaleSociale or 0.0
                vals["rea_member_type"] = REA.SocioUnico or False
                vals["rea_liquidation_state"] = REA.StatoLiquidazione or False

            if cedPrest.Contatti:
                if cedPrest.Contatti.Telefono:
                    vals["phone"] = cedPrest.Contatti.Telefono
                if cedPrest.Contatti.Email:
                    vals["email"] = cedPrest.Contatti.Email
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def getCarrirerPartner(self, Carrier):
        partner_model = self.env["res.partner"]
        partner_id = self.getPartnerBase(Carrier.DatiAnagraficiVettore)
        no_contact_update = False
        if partner_id:
            no_contact_update = partner_model.browse(
                partner_id
            ).electronic_invoice_no_contact_update
        if partner_id and not no_contact_update:
            vals = {
                "license_number": Carrier.DatiAnagraficiVettore.NumeroLicenzaGuida
                or "",
            }
            partner_model.browse(partner_id).write(vals)
        return partner_id

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_taxes = self.get_account_taxes(line.AliquotaIVA, line.Natura)
        if account_taxes:
            retLine["tax_ids"] = [fields.Command.set([account_taxes[0].id])]
        else:
            retLine["tax_ids"] = [fields.Command.clear()]
        return retLine

    def _get_default_product_taxes(self, tax_field_name):
        """Return default tax for field `product.product.<tax_field_name>`."""
        company = self.env.company
        default_taxes_ids = self.env["ir.default"].get(
            "product.product",
            tax_field_name,
            company_id=company.id,
        )
        tax_model = self.env["account.tax"]
        if default_taxes_ids is not None:
            default_taxes = tax_model.browse(default_taxes_ids)
            default_tax = first(default_taxes)
        else:
            default_tax = tax_model.browse()
        return default_tax

    def _get_account_tax_domain(self, amount):
        return [
            ("type_tax_use", "=", "purchase"),
            ("amount", "=", amount),
        ]

    def _get_zero_kind_account_tax(self, Natura):
        tax_amount = 0
        tax_domain = self._get_account_tax_domain(tax_amount)
        tax_domain = expression.AND(
            [
                tax_domain,
                [
                    ("kind_id.code", "=", Natura),
                ],
            ]
        )
        account_taxes = self.env["account.tax"].search(
            tax_domain,
            order="sequence",
        )
        account_tax = first(account_taxes)
        if not account_taxes:
            self.log_inconsistency(
                _(
                    "No tax with percentage "
                    "%(percentage)s and nature %(nature)s found. "
                    "Please configure this tax.",
                    percentage=tax_amount,
                    nature=Natura,
                )
            )
        elif len(account_taxes) > 1:
            self.log_inconsistency(
                _(
                    "Too many taxes with percentage "
                    "%(percentage)s and nature %(nature)s found. "
                    "Tax %(tax)s with lower priority has "
                    "been set on invoice lines.",
                    percentage=tax_amount,
                    nature=Natura,
                    tax=account_tax.description,
                )
            )
        return account_tax

    def _get_amount_account_tax(self, tax_amount):
        tax_domain = self._get_account_tax_domain(tax_amount)
        tax_domain = expression.AND(
            [
                tax_domain,
                [
                    ("price_include", "=", False),
                    # partially deductible VAT must be set by user
                    ("children_tax_ids", "=", False),
                ],
            ]
        )
        account_taxes = self.env["account.tax"].search(
            tax_domain,
            order="sequence",
        )
        account_tax = first(account_taxes)
        if not account_taxes:
            self.log_inconsistency(
                _(
                    "XML contains tax with percentage '%s' "
                    "but it does not exist in your system",
                    tax_amount,
                )
            )
        # check if there are multiple taxes with
        # same percentage
        elif len(account_taxes) > 1:
            # just logging because this is an usual case: see split payment
            _logger.warning(
                _(
                    "Too many taxes with percentage equals "
                    "to '%s'.\nFix it if required",
                    tax_amount,
                )
            )
            # if there are multiple taxes with same percentage
            # and there is a default tax with this percentage,
            # set taxes list equal to supplier_taxes_id
            default_tax = self._get_default_product_taxes("supplier_taxes_id")
            if default_tax and default_tax.amount == tax_amount:
                account_tax = default_tax
        return account_tax

    def get_account_taxes(self, AliquotaIVA, Natura):
        tax_amount = float(AliquotaIVA)
        if tax_amount == 0.0 and Natura:
            account_tax = self._get_zero_kind_account_tax(Natura)
        else:
            account_tax = self._get_amount_account_tax(tax_amount)
        return account_tax

    def get_line_product(self, line, partner):
        product = self.env["product.product"].browse()

        # Search the product using supplier infos
        supplier_info = self.env["product.supplierinfo"]
        partner_supplier_info = supplier_info.search(
            [
                ("partner_id", "=", partner.id),
            ]
        )
        found_supplier_infos = supplier_info.browse()
        if len(line.CodiceArticolo or []) == 1:
            supplier_code = line.CodiceArticolo[0].CodiceValore
            found_supplier_infos = supplier_info.search(
                [
                    ("id", "in", partner_supplier_info.ids),
                    ("product_code", "=", supplier_code),
                ]
            )
        if not found_supplier_infos:
            supplier_name = line.Descrizione
            found_supplier_infos = supplier_info.search(
                [
                    ("id", "in", partner_supplier_info.ids),
                    ("product_name", "=", supplier_name),
                ]
            )

        if found_supplier_infos:
            products = found_supplier_infos.mapped("product_id")
            if len(products) == 1:
                product = first(products)
            else:
                templates = found_supplier_infos.mapped("product_tmpl_id")
                if len(templates) == 1:
                    product = templates.product_variant_id

        if not product and partner.e_invoice_default_product_id:
            product = partner.e_invoice_default_product_id
        return product

    def adjust_accounting_data(self, product, line_vals):
        account = self.get_credit_account(product)
        line_vals["account_id"] = account.id

        new_tax = None
        if len(product.product_tmpl_id.supplier_taxes_id) == 1:
            new_tax = product.product_tmpl_id.supplier_taxes_id[0]
        elif len(account.tax_ids) == 1:
            new_tax = account.tax_ids[0]
        line_tax = self.env["account.tax"]
        if line_vals.get("tax_ids") and line_vals["tax_ids"][0] == fields.Command.SET:
            line_tax_id = line_vals["tax_ids"][0][2][0]
            line_tax = self.env["account.tax"].browse(line_tax_id)
        if new_tax and line_tax and new_tax != line_tax:
            if new_tax._get_tax_amount() != line_tax._get_tax_amount():
                self.log_inconsistency(
                    _(
                        "XML contains tax %(line_tax)s. "
                        "Product %(product)s has tax %(new_tax)s. Using "
                        "the XML one"
                    )
                    % {
                        "line_tax": line_tax.name,
                        "product": product.name,
                        "new_tax": new_tax.name,
                    }
                )
            else:
                # If product has the same amount of the one in XML,
                # I use it. Typical case: 22% det 50%
                line_vals["tax_ids"] = [(6, 0, [new_tax.id])]

    # move_line.tax_ids
    # move_line.name
    # move_line.sequence
    # move_line.account_id
    # move_line.price_unit
    # move_line.quantity
    def _prepareInvoiceLineAliquota(self, credit_account_id, line, nline):
        retLine = {}
        account_taxes = self.get_account_taxes(line.AliquotaIVA, line.Natura)
        if account_taxes:
            retLine["tax_ids"] = [fields.Command.set([account_taxes[0].id])]
        else:
            retLine["tax_ids"] = [fields.Command.clear()]

        retLine.update(
            {
                "name": f"Riepilogo Aliquota {line.AliquotaIVA}",
                "sequence": nline,
                "account_id": credit_account_id,
                "price_unit": float(abs(line.ImponibileImporto)),
            }
        )
        return retLine

    # move_line.name
    # move_line.sequence
    # move_line.account_id
    # move_line.price_unit
    # move_line.quantity
    # move_line.discount
    # move_line.admin_ref
    # move_line.invoice_line_tax_wt_ids
    def _prepareInvoiceLine(self, credit_account_id, line, wt_founds=False):
        retLine = self._prepare_generic_line_data(line)
        retLine.update(
            {
                "name": line.Descrizione,
                "sequence": int(line.NumeroLinea),
                "account_id": credit_account_id,
                "price_unit": float(line.PrezzoUnitario),
                "display_type": "product",
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
            retLine["discount"] = self._computeDiscount(line)
        if line.RiferimentoAmministrazione:
            retLine["admin_ref"] = line.RiferimentoAmministrazione
        if wt_founds and line.Ritenuta:
            retLine["invoice_line_tax_wt_ids"] = [(6, 0, [x.id for x in wt_founds])]

        return retLine

    def _prepareRelDocsLine(self, invoice_id, line, doc_type):
        res = []
        lineref = line.RiferimentoNumeroLinea or False
        IdDoc = line.IdDocumento or "Error"
        Data = line.Data or False
        NumItem = line.NumItem or ""
        Code = line.CodiceCommessaConvenzione or ""
        Cig = line.CodiceCIG or ""
        Cup = line.CodiceCUP or ""
        invoice_lineid = False
        if lineref:
            for numline in lineref:
                invoice_lineid = False
                invoice_line_model = self.env["account.move.line"]
                invoice_lines = invoice_line_model.search(
                    [
                        ("move_id", "=", invoice_id),
                        ("sequence", "=", int(numline)),
                    ]
                )
                if invoice_lines:
                    invoice_lineid = invoice_lines[0].id
                val = {
                    "type": doc_type,
                    "name": IdDoc,
                    "lineRef": numline,
                    "invoice_line_id": invoice_lineid,
                    "invoice_id": invoice_id,
                    "date": Data,
                    "numitem": NumItem,
                    "code": Code,
                    "cig": Cig,
                    "cup": Cup,
                }
                res.append(val)
        else:
            val = {
                "type": doc_type,
                "name": IdDoc,
                "invoice_line_id": invoice_lineid,
                "invoice_id": invoice_id,
                "date": Data,
                "numitem": NumItem,
                "code": Code,
                "cig": Cig,
                "cup": Cup,
            }
            res.append(val)
        return res

    def _prepareWelfareLine(self, invoice_id, line):
        TipoCassa = line.TipoCassa or False
        AlCassa = line.AlCassa and (float(line.AlCassa) / 100) or None
        ImportoContributoCassa = (
            line.ImportoContributoCassa and float(line.ImportoContributoCassa) or None
        )
        ImponibileCassa = line.ImponibileCassa and float(line.ImponibileCassa) or None
        AliquotaIVA = line.AliquotaIVA and (float(line.AliquotaIVA) / 100) or None
        Ritenuta = line.Ritenuta or ""
        Natura = line.Natura or False
        kind_id = False
        if Natura:
            kind = self.env["account.tax.kind"].search([("code", "=", Natura)])
            if not kind:
                self.log_inconsistency(_("Tax kind %s not found") % Natura)
            else:
                kind_id = kind[0].id

        RiferimentoAmministrazione = line.RiferimentoAmministrazione or ""
        WelfareTypeModel = self.env["welfare.fund.type"]
        if not TipoCassa:
            raise UserError(_("Welfare Fund is not defined."))
        WelfareType = WelfareTypeModel.search([("name", "=", TipoCassa)])

        res = {
            "welfare_rate_tax": AlCassa,
            "welfare_amount_tax": ImportoContributoCassa,
            "welfare_taxable": ImponibileCassa,
            "welfare_Iva_tax": AliquotaIVA,
            "subjected_withholding": Ritenuta,
            "kind_id": kind_id,
            "pa_line_code": RiferimentoAmministrazione,
            "invoice_id": invoice_id,
        }
        if not WelfareType:
            raise UserError(
                _("Welfare Fund %s not present in your system.") % TipoCassa
            )
        else:
            res["name"] = WelfareType[0].id

        return res

    def _prepareDiscRisePriceLine(self, line_id, line):
        Tipo = line.Tipo or False
        Percentuale = line.Percentuale and float(line.Percentuale) or 0.0
        Importo = line.Importo and float(line.Importo) or 0.0
        res = {
            "percentage": Percentuale,
            "amount": Importo,
            self.env.context.get("drtype"): line_id,
        }
        res["name"] = Tipo

        return res

    def _computeDiscount(self, DettaglioLinea):
        line_total = float(DettaglioLinea.PrezzoTotale)
        line_unit = line_total / float(DettaglioLinea.Quantita)
        discount = (1 - (line_unit / float(DettaglioLinea.PrezzoUnitario))) * 100.0
        return discount

    def _addGlobalDiscount(self, invoice_id, DatiGeneraliDocumento):
        discount = 0.0
        if (
            DatiGeneraliDocumento.ScontoMaggiorazione
            and self.e_invoice_detail_level == "2"
        ):
            invoice = self.env["account.move"].browse(invoice_id)
            for DiscRise in DatiGeneraliDocumento.ScontoMaggiorazione:
                if DiscRise.Percentuale:
                    amount = invoice.amount_total * (float(DiscRise.Percentuale) / 100)
                    if DiscRise.Tipo == "SC":
                        discount -= amount
                    elif DiscRise.Tipo == "MG":
                        discount += amount
                elif DiscRise.Importo:
                    if DiscRise.Tipo == "SC":
                        discount -= float(DiscRise.Importo)
                    elif DiscRise.Tipo == "MG":
                        discount += float(DiscRise.Importo)
            company = invoice.company_id
            global_discount_product = company.sconto_maggiorazione_product_id
            credit_account = self.get_credit_account(
                product=global_discount_product,
            )
            line_vals = {
                "move_id": invoice_id,
                "name": _("Global bill discount from document general data"),
                "account_id": credit_account.id,
                "price_unit": discount,
                "quantity": 1,
            }
            if global_discount_product:
                line_vals["product_id"] = global_discount_product.id
                line_vals["name"] = global_discount_product.name
                self.adjust_accounting_data(global_discount_product, line_vals)
            else:
                line_vals["tax_ids"] = [fields.Command.clear()]
            self.env["account.move.line"].with_context(
                check_move_validity=False
            ).create(line_vals)
        return True

    def _createPaymentsLine(self, payment_id, line, partner_id, invoice):
        details = line.DettaglioPagamento or False
        if details:
            PaymentModel = self.env["fatturapa.payment.detail"]
            PaymentMethodModel = self.env["fatturapa.payment_method"]
            BankModel = self.env["res.bank"]
            PartnerBankModel = self.env["res.partner.bank"]
            for dline in details:
                method = PaymentMethodModel.search(
                    [("code", "=", dline.ModalitaPagamento)]
                )
                if not method:
                    raise UserError(
                        _("Payment method %s is not defined in your system.")
                        % dline.ModalitaPagamento
                    )
                val = {
                    "recipient": dline.Beneficiario,
                    "fatturapa_pm_id": method[0].id,
                    "payment_term_start": dline.DataRiferimentoTerminiPagamento
                    or False,
                    "payment_days": dline.GiorniTerminiPagamento or 0,
                    "payment_due_date": dline.DataScadenzaPagamento or False,
                    "payment_amount": dline.ImportoPagamento or 0.0,
                    "post_office_code": dline.CodUfficioPostale or "",
                    "recepit_surname": dline.CognomeQuietanzante or "",
                    "recepit_name": dline.NomeQuietanzante or "",
                    "recepit_cf": dline.CFQuietanzante or "",
                    "recepit_title": dline.TitoloQuietanzante or "1",
                    "payment_bank_name": dline.IstitutoFinanziario or "",
                    "payment_bank_iban": dline.IBAN or "",
                    "payment_bank_abi": dline.ABI or "",
                    "payment_bank_cab": dline.CAB or "",
                    "payment_bank_bic": dline.BIC or "",
                    "payment_bank": False,
                    "prepayment_discount": dline.ScontoPagamentoAnticipato or 0.0,
                    "max_payment_date": dline.DataLimitePagamentoAnticipato or False,
                    "penalty_amount": dline.PenalitaPagamentiRitardati or 0.0,
                    "penalty_date": dline.DataDecorrenzaPenale or False,
                    "payment_code": dline.CodicePagamento or "",
                    "payment_data_id": payment_id,
                }
                bank = False
                payment_bank_id = False
                if dline.BIC:
                    banks = BankModel.search([("bic", "=", dline.BIC.strip())])
                    if not banks:
                        if not dline.IstitutoFinanziario:
                            self.log_inconsistency(
                                _(
                                    "Name of Bank with BIC '%s' is not set."
                                    " Can't create bank"
                                )
                                % dline.BIC
                            )
                        else:
                            bank = BankModel.create(
                                {
                                    "name": dline.IstitutoFinanziario,
                                    "bic": dline.BIC,
                                }
                            )
                    else:
                        bank = banks[0]
                if dline.IBAN:
                    iban = dline.IBAN.strip()
                    SearchDom = [
                        ("acc_number", "=", pretty_iban(iban)),
                        ("partner_id", "=", partner_id),
                    ]
                    payment_bank_id = False
                    payment_banks = PartnerBankModel.search(SearchDom)
                    if not payment_banks and not bank:
                        self.log_inconsistency(
                            _(
                                "BIC is required and not exist in Xml\n"
                                "Curr bank data is: \n"
                                "IBAN: %(iban)s\n"
                                "Bank Name: %(bank)s\n"
                            )
                            % {
                                "iban": iban or "",
                                "bank": dline.IstitutoFinanziario or "",
                            }
                        )
                    elif not payment_banks and bank:
                        existing_account = PartnerBankModel.search(
                            [
                                ("acc_number", "=", iban),
                                ("company_id", "=", invoice.company_id.id),
                            ]
                        )
                        if existing_account:
                            self.log_inconsistency(
                                _("Bank account %s already exists") % iban
                            )
                        else:
                            payment_bank_id = PartnerBankModel.create(
                                {
                                    "acc_number": iban,
                                    "partner_id": partner_id,
                                    "bank_id": bank.id,
                                    "bank_name": dline.IstitutoFinanziario or bank.name,
                                    "bank_bic": dline.BIC or bank.bic,
                                }
                            ).id
                    if payment_banks:
                        payment_bank_id = payment_banks[0].id

                if payment_bank_id:
                    val["payment_bank"] = payment_bank_id
                PaymentModel.create(val)
        return True

    # TODO sul partner?
    def set_StabileOrganizzazione(self, CedentePrestatore, invoice):
        if CedentePrestatore.StabileOrganizzazione:
            invoice.efatt_stabile_organizzazione_indirizzo = (
                CedentePrestatore.StabileOrganizzazione.Indirizzo
            )
            invoice.efatt_stabile_organizzazione_civico = (
                CedentePrestatore.StabileOrganizzazione.NumeroCivico
            )
            invoice.efatt_stabile_organizzazione_cap = (
                CedentePrestatore.StabileOrganizzazione.CAP
            )
            invoice.efatt_stabile_organizzazione_comune = (
                CedentePrestatore.StabileOrganizzazione.Comune
            )
            invoice.efatt_stabile_organizzazione_provincia = (
                CedentePrestatore.StabileOrganizzazione.Provincia
            )
            invoice.efatt_stabile_organizzazione_nazione = (
                CedentePrestatore.StabileOrganizzazione.Nazione
            )

    def _get_journal_domain(self, company):
        return [
            ("type", "=", "purchase"),
            ("company_id", "=", company.id),
        ]

    def get_journal(self, company):
        domain = self._get_journal_domain(company)
        journal = self.env["account.journal"].search(
            domain,
            limit=1,
        )
        if not journal:
            exception = self._get_missing_journal_exception(company)
            raise exception
        return journal

    def _get_missing_journal_exception(self, company):
        return UserError(
            _(
                "Define a purchase journal for this company: '%(name)s' (id: %(id)s).",
                name=company.name,
                id=company.id,
            )
        )

    def create_e_invoice_line(self, line):
        vals = {
            "line_number": int(line.NumeroLinea or 0),
            "service_type": line.TipoCessionePrestazione,
            "name": line.Descrizione,
            "qty": float(line.Quantita or 0),
            "uom": line.UnitaMisura,
            "period_start_date": line.DataInizioPeriodo,
            "period_end_date": line.DataFinePeriodo,
            "unit_price": float(line.PrezzoUnitario or 0),
            "total_price": float(line.PrezzoTotale or 0),
            "tax_amount": float(line.AliquotaIVA or 0),
            "wt_amount": line.Ritenuta,
            "tax_kind": line.Natura,
            "admin_ref": line.RiferimentoAmministrazione,
        }
        einvoiceline = self.env["einvoice.line"].create(vals)
        if line.CodiceArticolo:
            for caline in line.CodiceArticolo:
                self.env["fatturapa.article.code"].create(
                    {
                        "name": caline.CodiceTipo or "",
                        "code_val": caline.CodiceValore or "",
                        "e_invoice_line_id": einvoiceline.id,
                    }
                )
        if line.ScontoMaggiorazione:
            for DiscRisePriceLine in line.ScontoMaggiorazione:
                DiscRisePriceVals = self.with_context(
                    drtype="e_invoice_line_id"
                )._prepareDiscRisePriceLine(einvoiceline.id, DiscRisePriceLine)
                self.env["discount.rise.price"].create(DiscRisePriceVals)
        if line.AltriDatiGestionali:
            for dato in line.AltriDatiGestionali:
                self.env["einvoice.line.other.data"].create(
                    {
                        "name": dato.TipoDato,
                        "text_ref": dato.RiferimentoTesto,
                        "num_ref": float(dato.RiferimentoNumero or 0),
                        "date_ref": dato.RiferimentoData,
                        "e_invoice_line_id": einvoiceline.id,
                    }
                )
        return einvoiceline

    def get_credit_account(self, product=None):
        """
        Try to get default credit account for invoice line looking in

        1) product (if provided)
        2) journal
        3) company default.

        :param product: Product whose expense account will be used
        :return: The account found
        """
        credit_account = self.env["account.account"].browse()

        # If there is a product, get its default expense account
        if product:
            template = product.product_tmpl_id
            accounts_dict = template.get_product_accounts()
            credit_account = accounts_dict["expense"]

        company = self.env.company
        # Search in journal
        journal = self.get_journal(company)
        if not credit_account:
            credit_account = journal.default_account_id

        # Search in company defaults
        if not credit_account:
            credit_account = (
                self.env["ir.property"]
                .with_company(company)
                ._get("property_account_expense_categ_id", "product.category")
            )

        if not credit_account:
            raise UserError(
                _(
                    "Please configure Default Credit Account "
                    "in Journal '{journal}' "
                    "or check default expense account "
                    "for company '{company}'."
                ).format(
                    journal=journal.display_name,
                    company=company.display_name,
                )
            )

        return credit_account

    def _get_currency(self, FatturaBody):
        # currency 2.1.1.2
        currency_code = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Divisa
        currency = self.env["res.currency"].search(
            [
                ("name", "=", currency_code),
            ]
        )
        if not currency:
            raise UserError(
                _(
                    "No currency found with code %s.",
                    currency_code,
                )
            )
        return currency

    def _get_fiscal_document_type(self, FatturaBody):
        fiscal_document_type_code = (
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.TipoDocumento
        )
        if fiscal_document_type_code:
            fiscal_document_type = self.env["fiscal.document.type"].search(
                [
                    ("code", "=", fiscal_document_type_code),
                ],
                limit=1,
            )
            if not fiscal_document_type:
                raise UserError(
                    _(
                        "Document type %s not handled.",
                        fiscal_document_type_code,
                    )
                )
        else:
            fiscal_document_type = self.env["fiscal.document.type"].browse()
        return fiscal_document_type

    def _get_invoice_type(self, fiscal_document_type):
        if fiscal_document_type.code == "TD04":
            invoice_type = "in_refund"
        else:
            invoice_type = "in_invoice"
        return invoice_type

    def _get_received_date(self, attachment):
        received_date = attachment.e_invoice_received_date
        if not received_date:
            received_date = attachment.create_date
        received_date = received_date.date()
        return received_date

    def _prepare_invoice_values(self, fatt, fatturapa_attachment, FatturaBody, partner):
        company = self.env.company
        currency = self._get_currency(FatturaBody)
        purchase_journal = self.get_journal(company)
        comment = ""

        # 2.1.1
        fiscal_document_type = self._get_fiscal_document_type(FatturaBody)
        invoice_type = self._get_invoice_type(fiscal_document_type)

        # 2.1.1.11
        causLst = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Causale
        if causLst:
            for rel_doc in causLst:
                comment += rel_doc + "\n"
        if comment:
            comment = "<pre>" + comment + "</pre>"

        e_invoice_received_date = self._get_received_date(fatturapa_attachment)

        e_invoice_date = datetime.strptime(
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data, "%Y-%m-%d"
        ).date()

        delivery_partner_id = partner.address_get(["delivery"])["delivery"]
        delivery_partner = self.env["res.partner"].browse(delivery_partner_id)
        fiscal_position = self.env["account.fiscal.position"]._get_fiscal_position(
            partner,
            delivery=delivery_partner,
        )

        invoice_data = {
            "e_invoice_received_date": e_invoice_received_date,
            "invoice_date": e_invoice_date,
            "date": e_invoice_received_date
            if company.in_invoice_registration_date == "rec_date"
            else e_invoice_date,
            "fiscal_document_type_id": fiscal_document_type.id,
            "sender": fatt.FatturaElettronicaHeader.SoggettoEmittente or False,
            "move_type": invoice_type,
            "partner_id": partner.id,
            "currency_id": currency.id,
            "journal_id": purchase_journal.id,
            # 'origin': xmlData.datiOrdineAcquisto,
            "fiscal_position_id": fiscal_position.id,
            "invoice_payment_term_id": partner.property_supplier_payment_term_id.id,
            "company_id": company.id,
            "fatturapa_attachment_in_id": fatturapa_attachment.id,
            "narration": comment,
        }

        # 2.1.1.12
        self.set_art73(FatturaBody, invoice_data)

        self.set_e_invoice_lines(FatturaBody, invoice_data)
        return invoice_data

    def invoiceCreate(self, fatt, fatturapa_attachment, FatturaBody, partner_id):
        partner_model = self.env["res.partner"]
        partner = partner_model.browse(partner_id)
        invoice_data = self._prepare_invoice_values(
            fatt,
            fatturapa_attachment,
            FatturaBody,
            partner,
        )

        # 2.1.1.5
        found_withholding_taxes = self.set_withholding_tax(FatturaBody, invoice_data)

        invoice = self.env["account.move"].create(invoice_data)
        credit_account = self.get_credit_account()

        invoice_lines = []
        # 2.2.1
        invoice_lines.extend(
            self.set_invoice_line_ids(
                FatturaBody,
                credit_account.id,
                partner,
                found_withholding_taxes,
                invoice,
            )
        )

        # 2.1.1.7
        invoice_lines.extend(
            self.set_welfares_fund(
                FatturaBody, credit_account.id, invoice, found_withholding_taxes
            )
        )

        # 2.1.1.10
        invoice_lines.extend(self.set_efatt_rounding(FatturaBody, invoice))

        invoice.with_context(check_move_validity=False).update(
            {"invoice_line_ids": [(6, 0, invoice_lines)]}
        )

        invoice._onchange_invoice_line_wt_ids()

        rel_docs_dict = {
            # 2.1.2
            "order": FatturaBody.DatiGenerali.DatiOrdineAcquisto,
            # 2.1.3
            "contract": FatturaBody.DatiGenerali.DatiContratto,
            # 2.1.4
            "agreement": FatturaBody.DatiGenerali.DatiConvenzione,
            # 2.1.5
            "reception": FatturaBody.DatiGenerali.DatiRicezione,
            # 2.1.6
            "invoice": FatturaBody.DatiGenerali.DatiFattureCollegate,
        }

        for rel_doc_key, rel_doc_data in rel_docs_dict.items():
            if not rel_doc_data:
                continue
            for rel_doc in rel_doc_data:
                doc_datas = self._prepareRelDocsLine(invoice.id, rel_doc, rel_doc_key)
                for doc_data in doc_datas:
                    # Note for v12: must take advantage of batch creation
                    self.env["fatturapa.related_document_type"].create(doc_data)

        # 2.1.7
        self.set_activity_progress(FatturaBody, invoice)

        # 2.1.8
        self.set_ddt_data(FatturaBody, invoice)

        # 2.1.9
        self.set_delivery_data(FatturaBody, invoice)

        # 2.2.2
        self.set_summary_data(FatturaBody, invoice)

        # 2.1.10
        self.set_parent_invoice_data(FatturaBody, invoice)

        # 2.3
        self.set_vehicles_data(FatturaBody, invoice)

        # 2.4
        self.set_payments_data(FatturaBody, invoice, partner_id)

        # 2.5
        self.set_attachments_data(FatturaBody, invoice)

        self._addGlobalDiscount(
            invoice.id, FatturaBody.DatiGenerali.DatiGeneraliDocumento
        )

        if self.e_invoice_detail_level != "1":
            self.set_roundings(FatturaBody, invoice)

        self.set_vendor_bill_data(FatturaBody, invoice)

        # this can happen with refunds with negative amounts
        invoice.process_negative_lines()
        return invoice

    def set_vendor_bill_data(self, FatturaBody, invoice):
        if not invoice.invoice_date:
            invoice.update(
                {
                    "invoice_date": datetime.strptime(
                        FatturaBody.DatiGenerali.DatiGeneraliDocumento.Data, "%Y-%m-%d"
                    ).date(),
                }
            )
        if not invoice.ref:
            today = fields.Date.context_today(self)
            x = invoice.line_ids.filtered(
                lambda line: line.account_id.account_type
                in ("asset_receivable", "liability_payable")
            ).sorted(lambda line: line.date_maturity or today)
            if x:
                x[-1].name = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero
            invoice.ref = FatturaBody.DatiGenerali.DatiGeneraliDocumento.Numero
            if not invoice.payment_reference:
                invoice.payment_reference = invoice.ref

    def set_parent_invoice_data(self, FatturaBody, invoice):
        ParentInvoice = FatturaBody.DatiGenerali.FatturaPrincipale
        if ParentInvoice:
            parentinv_vals = {
                "related_invoice_code": ParentInvoice.NumeroFatturaPrincipale or "",
                "related_invoice_date": ParentInvoice.DataFatturaPrincipale or False,
            }
            invoice.write(parentinv_vals)

    def set_vehicles_data(self, FatturaBody, invoice):
        Vehicle = FatturaBody.DatiVeicoli
        if Vehicle:
            veicle_vals = {
                "vehicle_registration": Vehicle.Data or False,
                "total_travel": Vehicle.TotalePercorso or "",
            }
            invoice.write(veicle_vals)

    def set_attachments_data(self, FatturaBody, invoice):
        invoice_id = invoice.id
        AttachmentsData = FatturaBody.Allegati
        if AttachmentsData:
            self.env["fatturapa.attachment.in"].extract_attachments(
                AttachmentsData, invoice_id
            )

    def set_ddt_data(self, FatturaBody, invoice):
        invoice_id = invoice.id
        DdtDatas = FatturaBody.DatiGenerali.DatiDDT
        if not DdtDatas:
            return
        invoice_line_model = self.env["account.move.line"]
        DdTModel = self.env["fatturapa.related_ddt"]
        for DdtDataLine in DdtDatas:
            if not DdtDataLine.RiferimentoNumeroLinea:
                DdTModel.create(
                    {
                        "name": DdtDataLine.NumeroDDT or "",
                        "date": DdtDataLine.DataDDT or False,
                        "invoice_id": invoice_id,
                    }
                )
            else:
                for numline in DdtDataLine.RiferimentoNumeroLinea:
                    invoice_lines = invoice_line_model.search(
                        [
                            ("move_id", "=", invoice_id),
                            ("sequence", "=", int(numline)),
                        ]
                    )
                    invoice_lineid = False
                    if invoice_lines:
                        invoice_lineid = invoice_lines[0].id
                    DdTModel.create(
                        {
                            "name": DdtDataLine.NumeroDDT or "",
                            "date": DdtDataLine.DataDDT or False,
                            "invoice_id": invoice_id,
                            "invoice_line_id": invoice_lineid,
                        }
                    )

    def set_art73(self, FatturaBody, invoice_data):
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Art73:
            invoice_data["art73"] = True

    def set_roundings(self, FatturaBody, invoice):
        rounding = 0.0
        if FatturaBody.DatiBeniServizi.DatiRiepilogo:
            for summary in FatturaBody.DatiBeniServizi.DatiRiepilogo:
                rounding += float(summary.Arrotondamento or 0.0)
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento:
            summary = FatturaBody.DatiGenerali.DatiGeneraliDocumento
            rounding += float(summary.Arrotondamento or 0.0)

        if rounding:
            arrotondamenti_attivi_account_id = (
                self.env.company.arrotondamenti_attivi_account_id
            )
            if not arrotondamenti_attivi_account_id:
                raise UserError(
                    _("Round up account is not set " "in Accounting Settings")
                )

            arrotondamenti_passivi_account_id = (
                self.env.company.arrotondamenti_passivi_account_id
            )
            if not arrotondamenti_passivi_account_id:
                raise UserError(
                    _("Round down account is not set " "in Accounting Settings")
                )

            arrotondamenti_tax_id = self.env.company.arrotondamenti_tax_id
            if not arrotondamenti_tax_id:
                self.log_inconsistency(_("Round up and down tax is not set"))

            line_sequence = max(invoice.invoice_line_ids.mapped("sequence"), default=1)
            line_vals = []
            for summary in FatturaBody.DatiBeniServizi.DatiRiepilogo:
                # XXX fallisce cattivo se non trova l'imposta Arrotondamento
                to_round = float(summary.Arrotondamento or 0.0)
                if to_round != 0.0:
                    account_taxes = self.get_account_taxes(
                        summary.AliquotaIVA, summary.Natura
                    )
                    arrotondamenti_account_id = (
                        arrotondamenti_passivi_account_id.id
                        if to_round > 0.0
                        else arrotondamenti_attivi_account_id.id
                    )
                    invoice_line_tax_id = (
                        account_taxes[0].id
                        if account_taxes
                        else arrotondamenti_tax_id.id
                    )
                    name = _("Rounding down") if to_round > 0.0 else _("Rounding up")
                    line_sequence += 1
                    upd_vals = {
                        "sequence": line_sequence,
                        "move_id": invoice.id,
                        "name": name,
                        "account_id": arrotondamenti_account_id,
                        "price_unit": to_round,
                        "tax_ids": [(6, 0, [invoice_line_tax_id])],
                    }
                    # Valutare se in caso di importazione senza rounding sia meglio
                    # lavorare su debito e credito invece di
                    # mettere una tassa sul valore !!
                    #                     if to_round<0:
                    #                        upd_vals["debit"]= abs(to_round)
                    #                     else:
                    #                        upd_vals["credit"]= abs(to_round)
                    line_vals.append(upd_vals)

            if line_vals:
                self.env["account.move.line"].with_context(
                    check_move_validity=False
                ).create(line_vals)

    def set_efatt_rounding(self, FatturaBody, invoice):
        invoice_line_model = self.env["account.move.line"]
        invoice_line_ids = []
        if FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento:
            invoice.efatt_rounding = float(
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento
            )
            if invoice.efatt_rounding != 0:
                if invoice.efatt_rounding > 0:
                    arrotondamenti_account_id = (
                        self.env.company.arrotondamenti_passivi_account_id
                    )
                    if not arrotondamenti_account_id:
                        raise UserError(
                            _("Round down account is not set " "in Accounting Settings")
                        )
                    name = _("Rounding down")
                else:
                    arrotondamenti_account_id = (
                        self.env.company.arrotondamenti_attivi_account_id
                    )
                    if not arrotondamenti_account_id:
                        raise UserError(
                            _("Round up account is not set " "in Accounting Settings")
                        )
                    name = _("Rounding up")
                upd_vals = {
                    "move_id": invoice.id,
                    "name": name,
                    "account_id": arrotondamenti_account_id.id,
                    "price_unit": invoice.efatt_rounding,
                    "quantity": 1,
                    "tax_ids": [fields.Command.set([])],
                }
                self.create_and_get_line_id(
                    invoice_line_ids, invoice_line_model, upd_vals
                )
        return invoice_line_ids

    def set_activity_progress(self, FatturaBody, invoice):
        invoice_id = invoice.id
        SalDatas = FatturaBody.DatiGenerali.DatiSAL
        if SalDatas:
            SalModel = self.env["fatturapa.activity.progress"]
            for SalDataLine in SalDatas:
                SalModel.create(
                    {
                        "fatturapa_activity_progress": SalDataLine.RiferimentoFase or 0,
                        "invoice_id": invoice_id,
                    }
                )

    def _get_last_due_date(self, DatiPagamento):
        dates = []
        for PaymentLine in DatiPagamento or []:
            details = PaymentLine.DettaglioPagamento
            if details:
                for dline in details:
                    if dline.DataScadenzaPagamento:
                        dates.append(fields.Date.to_date(dline.DataScadenzaPagamento))
        dates.sort(reverse=True)
        return dates

    def set_payments_data(self, FatturaBody, invoice, partner_id):
        invoice_id = invoice.id
        PaymentsData = FatturaBody.DatiPagamento
        partner = self.env["res.partner"].browse(partner_id)
        if not partner.property_supplier_payment_term_id:
            due_dates = self._get_last_due_date(FatturaBody.DatiPagamento)
            if due_dates:
                self.env["account.move"].browse(
                    invoice_id
                ).invoice_date_due = due_dates[0]
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
                self._createPaymentsLine(PayDataId, PaymentLine, partner_id, invoice)

    def set_withholding_tax(self, FatturaBody, invoice_data):
        Withholdings = FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta
        if not Withholdings:
            return None

        withholding_tax_model = self.env["withholding.tax"]
        found_withholding_taxes = withholding_tax_model.browse()
        e_withholding_taxes_values = []
        for Withholding in Withholdings:
            payment_reason_code = Withholding.CausalePagamento
            withholding_taxes = withholding_tax_model.search(
                [("payment_reason_id.code", "=", payment_reason_code)],
            )
            if not withholding_taxes:
                raise UserError(
                    _(
                        "The bill contains withholding tax with "
                        "payment reason %s, "
                        "but such a tax is not found in your system. Please "
                        "set it.",
                        payment_reason_code,
                    )
                )

            withholding_tax_amount = Withholding.AliquotaRitenuta
            e_withholding_tax_type = Withholding.TipoRitenuta
            withholding_tax_type = WT_CODES_MAPPING[e_withholding_tax_type]
            for withholding_tax in withholding_taxes:
                if (
                    withholding_tax.tax == float(withholding_tax_amount)
                    and withholding_tax_type == withholding_tax.wt_types
                ):
                    found_withholding_taxes |= withholding_tax
                    break
            else:
                raise UserError(
                    _(
                        "No withholding tax found with document payment "
                        "reason %(reason)s rate %(rate)s and type %(type)s.",
                        reason=payment_reason_code,
                        rate=withholding_tax_amount,
                        type=withholding_tax_type,
                    )
                )

            e_withholding_tax_values = {
                "name": e_withholding_tax_type,
                "amount": Withholding.ImportoRitenuta,
            }
            e_withholding_taxes_values.append(e_withholding_tax_values)

        invoice_data["ftpa_withholding_ids"] = [
            (0, 0, withholding_tax_values)
            for withholding_tax_values in e_withholding_taxes_values
        ]
        return found_withholding_taxes

    def set_welfares_fund(self, FatturaBody, credit_account_id, invoice, wt_founds):
        invoice_line_model = self.env["account.move.line"]
        invoice_line_ids = []
        if self.e_invoice_detail_level == "2":
            Welfares = (
                FatturaBody.DatiGenerali.DatiGeneraliDocumento.DatiCassaPrevidenziale
            )
            if Welfares:
                WelfareFundLineModel = self.env["welfare.fund.data.line"]
                for welfareLine in Welfares:
                    WalfarLineVals = self._prepareWelfareLine(invoice.id, welfareLine)
                    WelfareFundLineModel.create(WalfarLineVals)

                    if welfareLine.TipoCassa == "TC07":
                        continue

                    line_vals = self._prepare_generic_line_data(welfareLine)
                    line_vals.update(
                        {
                            "name": _("Welfare Fund: %s") % welfareLine.TipoCassa,
                            "price_unit": float(welfareLine.ImportoContributoCassa),
                            "move_id": invoice.id,
                            "account_id": credit_account_id,
                            "quantity": 1,
                        }
                    )
                    if welfareLine.Ritenuta:
                        if not wt_founds:
                            raise UserError(
                                _(
                                    "Welfare Fund data %s has withholding tax but no "
                                    "withholding tax was found in the system."
                                )
                                % welfareLine.TipoCassa
                            )
                        line_vals["invoice_line_tax_wt_ids"] = [
                            (6, 0, [wt.id for wt in wt_founds])
                        ]
                    if self.env.company.cassa_previdenziale_product_id:
                        cassa_previdenziale_product = (
                            self.env.company.cassa_previdenziale_product_id
                        )
                        line_vals["product_id"] = cassa_previdenziale_product.id
                        line_vals["name"] = cassa_previdenziale_product.name
                        self.adjust_accounting_data(
                            cassa_previdenziale_product, line_vals
                        )
                    self.create_and_get_line_id(
                        invoice_line_ids, invoice_line_model, line_vals
                    )
        return invoice_line_ids

    def _convert_datetime(self, dtstring):
        ret = False
        try:
            dt = datetime.strptime(dtstring, "%Y-%m-%dT%H:%M:%S")
            if dt:
                ret = dt.strftime("%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):  # pylint: disable=except-pass
            pass
        return ret

    def set_delivery_data(self, FatturaBody, invoice):
        Delivery = FatturaBody.DatiGenerali.DatiTrasporto
        if Delivery:
            delivery_id = self.getCarrirerPartner(Delivery)
            delivery_dict = {
                "carrier_id": delivery_id,
                "transport_vehicle": Delivery.MezzoTrasporto or "",
                "transport_reason": Delivery.CausaleTrasporto or "",
                "number_items": Delivery.NumeroColli or 0,
                "description": Delivery.Descrizione or "",
                "unit_weight": Delivery.UnitaMisuraPeso or 0.0,
                "gross_weight": Delivery.PesoLordo or 0.0,
                "net_weight": Delivery.PesoNetto or 0.0,
                "pickup_datetime": self._convert_datetime(Delivery.DataOraRitiro)
                or False,
                "transport_date": Delivery.DataInizioTrasporto or False,
                "delivery_datetime": self._convert_datetime(Delivery.DataOraConsegna)
                or False,
                "delivery_address": "",
                "ftpa_incoterms": Delivery.TipoResa,
            }

            if Delivery.IndirizzoResa:
                delivery_dict["delivery_address"] = "{}, {}\n{} - {}\n{} {}".format(
                    Delivery.IndirizzoResa.Indirizzo or "",
                    Delivery.IndirizzoResa.NumeroCivico or "",
                    Delivery.IndirizzoResa.CAP or "",
                    Delivery.IndirizzoResa.Comune or "",
                    Delivery.IndirizzoResa.Provincia or "",
                    Delivery.IndirizzoResa.Nazione or "",
                )
            invoice.write(delivery_dict)

    def set_summary_data(self, FatturaBody, invoice):
        invoice_id = invoice.id
        Summary_datas = FatturaBody.DatiBeniServizi.DatiRiepilogo
        summary_data_model = self.env["fatturapa.summary.data"]
        if Summary_datas:
            for summary in Summary_datas:
                summary_line = {
                    "tax_rate": summary.AliquotaIVA or 0.0,
                    "non_taxable_nature": summary.Natura or False,
                    "incidental_charges": summary.SpeseAccessorie or 0.0,
                    "rounding": summary.Arrotondamento or 0.0,
                    "amount_untaxed": summary.ImponibileImporto or 0.0,
                    "amount_tax": summary.Imposta or 0.0,
                    "payability": summary.EsigibilitaIVA or False,
                    "law_reference": summary.RiferimentoNormativo or "",
                    "invoice_id": invoice_id,
                }
                summary_data_model.create(summary_line)

    def set_e_invoice_lines(self, FatturaBody, invoice_data):
        e_invoice_lines = self.env["einvoice.line"].browse()
        for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
            e_invoice_lines |= self.create_e_invoice_line(line)
        if e_invoice_lines:
            invoice_data["e_invoice_line_ids"] = [(6, 0, e_invoice_lines.ids)]

    def _set_invoice_lines(
        self, product, invoice_line_data, invoice_lines, invoice_line_model
    ):
        if product:
            invoice_line_data["product_id"] = product.id
            self.adjust_accounting_data(product, invoice_line_data)
        self.create_and_get_line_id(
            invoice_lines, invoice_line_model, invoice_line_data
        )

    # move_id
    # account_id
    def set_invoice_line_ids(
        self, FatturaBody, credit_account_id, partner, wt_founds, invoice
    ):
        invoice_lines = []
        invoice_line_model = self.env["account.move.line"]
        if self.e_invoice_detail_level == "1":
            for nline, line in enumerate(FatturaBody.DatiBeniServizi.DatiRiepilogo):
                invoice_line_data = self._prepareInvoiceLineAliquota(
                    credit_account_id, line, nline
                )
                invoice_line_data["move_id"] = invoice.id

                product = partner.e_invoice_default_product_id
                self._set_invoice_lines(
                    product, invoice_line_data, invoice_lines, invoice_line_model
                )

        elif self.e_invoice_detail_level == "2":
            for line in FatturaBody.DatiBeniServizi.DettaglioLinee:
                invoice_line_data = self._prepareInvoiceLine(
                    credit_account_id, line, wt_founds
                )
                invoice_line_data["move_id"] = invoice.id

                product = self.get_line_product(line, partner)
                self._set_invoice_lines(
                    product, invoice_line_data, invoice_lines, invoice_line_model
                )
        return invoice_lines

    def check_invoice_amount(self, invoice, FatturaElettronicaBody):
        dgd = FatturaElettronicaBody.DatiGenerali.DatiGeneraliDocumento
        if dgd.ScontoMaggiorazione and dgd.ImportoTotaleDocumento:
            # assuming that, if someone uses
            # DatiGeneraliDocumento.ScontoMaggiorazione, also fills
            # DatiGeneraliDocumento.ImportoTotaleDocumento
            ImportoTotaleDocumento = float(dgd.ImportoTotaleDocumento)
            if not float_is_zero(
                invoice.amount_total - ImportoTotaleDocumento, precision_digits=2
            ):
                self.log_inconsistency(
                    _(
                        "Bill total %(amount_total)s is different "
                        "from document total amount %(document_total_amount)s"
                    )
                    % {
                        "amount_total": invoice.amount_total,
                        "document_total_amount": ImportoTotaleDocumento,
                    }
                )
        else:
            # else, we can only check DatiRiepilogo if
            # DatiGeneraliDocumento.ScontoMaggiorazione is not present,
            # because otherwise DatiRiepilogo and odoo invoice total would
            # differ
            amount_untaxed = invoice.compute_xml_amount_untaxed(FatturaElettronicaBody)
            if not float_is_zero(
                invoice.amount_untaxed - amount_untaxed, precision_digits=2
            ):
                self.log_inconsistency(
                    _(
                        "Computed amount untaxed %(amount_untaxed)s is "
                        "different from summary data %(summary_data)s"
                    )
                    % {
                        "amount_untaxed": invoice.amount_untaxed,
                        "summary_data": amount_untaxed,
                    }
                )

    def create_and_get_line_id(self, invoice_line_ids, invoice_line_model, upd_vals):
        invoice_line_id = (
            invoice_line_model.with_context(check_move_validity=False)
            .create(upd_vals)
            .id
        )
        invoice_line_ids.append(invoice_line_id)

    def _set_decimal_precision(self, precision_name, field_name):
        precision = self.env["decimal.precision"].search(
            [("name", "=", precision_name)], limit=1
        )
        different_precisions = original_precision = None
        if precision:
            precision_id = precision.id
            original_precision = precision.digits
            different_precisions = self[field_name] != original_precision
            if different_precisions:
                with registry(self.env.cr.dbname).cursor() as new_cr:
                    # We need a new env (and cursor) because 'digits' property of Float
                    # fields is retrieved with a new LazyCursor,
                    # see class Float at odoo.fields,
                    # so we need to write (commit) to DB in order to make the new
                    # precision available
                    new_env = api.Environment(new_cr, self.env.uid, self.env.context)
                    new_precision = new_env["decimal.precision"].browse(precision_id)
                    new_precision.sudo().write({"digits": self[field_name]})
                    new_cr.commit()
        return precision, different_precisions, original_precision

    def _restore_original_precision(self, precision, original_precision):
        with registry(self.env.cr.dbname).cursor() as new_cr:
            new_env = api.Environment(new_cr, self.env.uid, self.env.context)
            new_price_precision = new_env["decimal.precision"].browse(precision.id)
            new_price_precision.sudo().write({"digits": original_precision})
            new_cr.commit()

    def _get_invoice_partner_id(self, fatt):
        cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
        partner_id = self.getCedPrest(cedentePrestatore)
        return partner_id

    def importFatturaPA(self):
        self.ensure_one()

        (
            price_precision,
            different_price_precisions,
            original_price_precision,
        ) = self._set_decimal_precision("Product Price", "price_decimal_digits")
        (
            qty_precision,
            different_qty_precisions,
            original_qty_precision,
        ) = self._set_decimal_precision(
            "Product Unit of Measure", "quantity_decimal_digits"
        )
        (
            discount_precision,
            different_discount_precisions,
            original_discount_precision,
        ) = self._set_decimal_precision("Discount", "discount_decimal_digits")

        new_invoices = []
        # convert to dict in order to be able to modify context
        fatturapa_attachments = self._get_selected_records()
        self.env.context = dict(self.env.context)
        for fatturapa_attachment in fatturapa_attachments:
            self.reset_inconsistencies()
            self._check_attachment(fatturapa_attachment)

            fatt = fatturapa_attachment.get_invoice_obj()
            if not fatt:
                raise UserError(
                    _(
                        "Cannot import an attachment that could not be parsed.\n"
                        "Please fix the parsing error first, then try again."
                    )
                )

            cedentePrestatore = fatt.FatturaElettronicaHeader.CedentePrestatore
            # 1.2
            partner_id = self._get_invoice_partner_id(fatt)
            # 1.3
            TaxRappresentative = fatt.FatturaElettronicaHeader.RappresentanteFiscale
            # 1.5
            Intermediary = (
                fatt.FatturaElettronicaHeader.TerzoIntermediarioOSoggettoEmittente
            )

            generic_inconsistencies = ""
            existing_inconsistencies = self.get_inconsistencies()
            if existing_inconsistencies:
                generic_inconsistencies = existing_inconsistencies + "\n\n"

            xmlproblems = getattr(fatt, "_xmldoctor", None)
            if xmlproblems:  # None or []
                generic_inconsistencies += "\n".join(xmlproblems) + "\n\n"

            # 2
            for fattura in fatt.FatturaElettronicaBody:
                # reset inconsistencies
                self.reset_inconsistencies()

                invoice = self.invoiceCreate(
                    fatt, fatturapa_attachment, fattura, partner_id
                )

                self.set_StabileOrganizzazione(cedentePrestatore, invoice)
                if TaxRappresentative:
                    tax_partner_id = self.getPartnerBase(
                        TaxRappresentative.DatiAnagrafici
                    )
                    invoice.write({"tax_representative_id": tax_partner_id})
                if Intermediary:
                    Intermediary_id = self.getPartnerBase(Intermediary.DatiAnagrafici)
                    invoice.write({"intermediary": Intermediary_id})
                new_invoices.append(invoice.id)
                self.check_invoice_amount(invoice, fattura)

                invoice.set_einvoice_data(fattura)

                existing_inconsistencies = self.get_inconsistencies()
                if existing_inconsistencies:
                    invoice_inconsistencies = existing_inconsistencies
                else:
                    invoice_inconsistencies = ""
                invoice.inconsistencies = (
                    generic_inconsistencies + invoice_inconsistencies
                )

        if price_precision and different_price_precisions:
            self._restore_original_precision(price_precision, original_price_precision)
        if qty_precision and different_qty_precisions:
            self._restore_original_precision(qty_precision, original_qty_precision)
        if discount_precision and different_discount_precisions:
            self._restore_original_precision(
                discount_precision, original_discount_precision
            )

        return {
            "view_type": "form",
            "name": "Electronic Bills",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", new_invoices)],
        }
