import re

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export

NS_2 = "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v2.0"
VERSION = "DAT20"
NS_MAP = {
    "ns2": NS_2,
}
etree.register_namespace("vi", NS_2)


def format_decimal(value=0.0):
    return "{:.2f}".format(value)


def clear_xml_element(element):
    if element.text:
        return False
    return all(clear_xml_element(e) for e in element.iterchildren())


def clear_xml(xml_root):
    xml_root = etree.iterwalk(xml_root)
    for _dummy, xml_element in xml_root:
        parent = xml_element.getparent()
        if clear_xml_element(xml_element):
            parent.remove(xml_element)


def check_normalized_string(value):
    normalized = True
    if not value:
        return normalized
    if value != value.strip():
        normalized = False
    return normalized


class ComunicazioneDatiIva(models.Model):
    _name = "comunicazione.dati.iva"
    _description = "Invoices data communication"
    _rec_name = "identificativo"
    _inherit = ["mail.thread"]

    @api.model
    def _default_company(self):
        company_id = self._context.get("company_id", self.env.company.id)
        return company_id

    @api.constrains("identificativo")
    def _check_identificativo(self):
        domain = [("identificativo", "=", self.identificativo)]
        dichiarazioni = self.search(domain)
        if len(dichiarazioni) > 1:
            raise ValidationError(
                _("Statement already exists with ID {}").format(self.identificativo)
            )

    def _get_identificativo(self):
        dichiarazioni = self.search([])
        if dichiarazioni:
            return len(dichiarazioni) + 1
        else:
            return 1

    company_id = fields.Many2one(
        "res.company", string="Company", required=True, default=_default_company
    )
    identificativo = fields.Integer(
        string="Identifier", copy=False, default=_get_identificativo
    )
    id_comunicazione = fields.Char(
        string="Communication ID",
        help="Identifier provided by the Revenue Agency after performing the "
        "communication by XML file",
    )
    splitting_note = fields.Text("Splitting note", readonly=True, copy=False)
    declarant_fiscalcode = fields.Char(
        string="Declarant fiscal code",
        help="Fiscal code of the person communicating the invoices data",
    )
    codice_carica_id = fields.Many2one("appointment.code", string="Role code")
    date_start = fields.Date(string="Date start", required=True)
    date_end = fields.Date(string="Date end", required=True)
    fatture_emesse_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.emesse", "comunicazione_id"
    )
    fatture_ricevute_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.ricevute", "comunicazione_id"
    )
    fatture_emesse = fields.Boolean(string="Customer invoices")
    fatture_ricevute = fields.Boolean(string="Supplier bills")
    dati_trasmissione = fields.Selection(
        [
            ("DTE", "Customer invoices"),
            ("DTR", "Supplier bills"),
            ("ANN", "Cancellation previously sent data"),
        ],
        string="Data transmission",
        required=True,
    )
    # Cedente
    partner_cedente_id = fields.Many2one("res.partner")
    cedente_IdFiscaleIVA_IdPaese = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cedente_IdFiscaleIVA_IdCodice = fields.Char(size=28)
    cedente_CodiceFiscale = fields.Char(size=16)
    cedente_Denominazione = fields.Char(size=80)
    cedente_Nome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.3 <Cognome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cedente_Cognome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.2 <Nome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cedente_sede_Indirizzo = fields.Char(size=60)
    cedente_sede_NumeroCivico = fields.Char(size=8)
    cedente_sede_Cap = fields.Char(size=5)
    cedente_sede_Comune = fields.Char(size=60)
    cedente_sede_Provincia = fields.Char(size=2)
    cedente_sede_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cedente_so_Indirizzo = fields.Char(size=60)
    cedente_so_NumeroCivico = fields.Char(size=8)
    cedente_so_Cap = fields.Char(size=5)
    cedente_so_Comune = fields.Char(size=60)
    cedente_so_Provincia = fields.Char(size=2)
    cedente_so_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cedente_rf_IdFiscaleIVA_IdPaese = fields.Char(size=2, help="Only IT is accepted")
    cedente_rf_IdFiscaleIVA_IdCodice = fields.Char(size=11)
    cedente_rf_Denominazione = fields.Char(size=80)
    cedente_rf_Nome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.3 <Cognome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cedente_rf_Cognome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.2 <Nome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    # Cessionario
    partner_cessionario_id = fields.Many2one("res.partner")
    cessionario_IdFiscaleIVA_IdPaese = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cessionario_IdFiscaleIVA_IdCodice = fields.Char(size=28)
    cessionario_CodiceFiscale = fields.Char(size=16)
    cessionario_Denominazione = fields.Char(size=80)
    cessionario_Nome = fields.Char(
        size=60,
        help="To fill along with 3.1.2.3 <Cognome> and alternatively to "
        "3.1.2.1 <Denominazione>",
    )
    cessionario_Cognome = fields.Char(
        size=60,
        help="To fill along with 3.1.2.3 <Nome> and alternatively to "
        "3.1.2.1 <Denominazione>",
    )
    cessionario_sede_Indirizzo = fields.Char(size=60)
    cessionario_sede_NumeroCivico = fields.Char(size=8)
    cessionario_sede_Cap = fields.Char(size=5)
    cessionario_sede_Comune = fields.Char(size=60)
    cessionario_sede_Provincia = fields.Char(size=2)
    cessionario_sede_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cessionario_so_Indirizzo = fields.Char(size=60)
    cessionario_so_NumeroCivico = fields.Char(size=8)
    cessionario_so_Cap = fields.Char(size=5)
    cessionario_so_Comune = fields.Char(size=60)
    cessionario_so_Provincia = fields.Char(size=2)
    cessionario_so_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cessionario_rf_IdFiscaleIVA_IdPaese = fields.Char(
        size=2, help="Only IT is accepted"
    )
    cessionario_rf_IdFiscaleIVA_IdCodice = fields.Char(size=11)
    cessionario_rf_Denominazione = fields.Char(size=80)
    cessionario_rf_Nome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.3 <Cognome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cessionario_rf_Cognome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.2 <Nome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    errors = fields.Text(copy=False)
    esterometro = fields.Boolean(default=True, string="Esterometro")

    @api.onchange("partner_cedente_id")
    def onchange_partner_cedente_id(self):
        for comunicazione in self:
            if comunicazione.partner_cedente_id:
                vals = self._prepare_cedente_partner_id(
                    comunicazione.partner_cedente_id
                )
                comunicazione.cedente_IdFiscaleIVA_IdPaese = vals[
                    "cedente_IdFiscaleIVA_IdPaese"
                ]
                comunicazione.cedente_IdFiscaleIVA_IdCodice = vals[
                    "cedente_IdFiscaleIVA_IdCodice"
                ]
                comunicazione.cedente_CodiceFiscale = vals["cedente_CodiceFiscale"]
                comunicazione.cedente_Denominazione = vals["cedente_Denominazione"]
                # Sede
                comunicazione.cedente_sede_Indirizzo = vals["cedente_sede_Indirizzo"]
                comunicazione.cedente_sede_Cap = vals["cedente_sede_Cap"]
                comunicazione.cedente_sede_Comune = vals["cedente_sede_Comune"]
                comunicazione.cedente_sede_Provincia = vals["cedente_sede_Provincia"]
                comunicazione.cedente_sede_Nazione = vals["cedente_sede_Nazione"]

    def _prepare_cedente_partner_id(self, partner, vals=None):
        vals = {}
        # ----- Get vat
        partner_vat = partner.commercial_partner_id.vat or ""
        if partner.country_id:
            vals["cedente_IdFiscaleIVA_IdPaese"] = partner.country_id.code
        elif partner_vat:
            vals["cedente_IdFiscaleIVA_IdPaese"] = partner_vat[:2]
        else:
            vals["cedente_IdFiscaleIVA_IdPaese"] = ""
        vals["cedente_IdFiscaleIVA_IdCodice"] = partner_vat[2:] if partner_vat else ""
        # ----- Get fiscalcode
        vals["cedente_CodiceFiscale"] = partner.commercial_partner_id.fiscalcode or ""
        vals["cedente_Denominazione"] = encode_for_export(partner.name, 80)
        # Sede
        vals["cedente_sede_Indirizzo"] = "{} {}".format(
            encode_for_export(partner.street or "", 60),
            encode_for_export(partner.street2 or "", 60),
        ).strip()
        vals["cedente_sede_Cap"] = encode_for_export(
            partner.zip or "", 5, encoding="ascii"
        )
        vals["cedente_sede_Comune"] = encode_for_export(partner.city or "", 60)
        vals["cedente_sede_Provincia"] = (
            partner.state_id and partner.state_id.code or ""
        )
        if partner.country_id:
            vals["cedente_sede_Nazione"] = partner.country_id.code
        elif partner_vat:
            vals["cedente_sede_Nazione"] = partner_vat[:2]
        else:
            vals["cedente_sede_Nazione"] = ""
        # Normalizzazione dati in base alla nazione UE o EXTRA UE:
        vals_norm = {
            "sede_Nazione": vals["cedente_sede_Nazione"],
            "IdFiscaleIVA_IdCodice": vals["cedente_IdFiscaleIVA_IdCodice"],
        }
        vals_norm = self._normalizza_dati_partner(partner, vals_norm)
        if "sede_Cap" in vals_norm:
            vals["cedente_sede_Cap"] = vals_norm["sede_Cap"]
        if "sede_Provincia" in vals_norm:
            vals["cedente_sede_Provincia"] = vals_norm["sede_Provincia"]
        if "CodiceFiscale" in vals_norm:
            vals["cedente_CodiceFiscale"] = vals_norm["CodiceFiscale"]
        if "IdFiscaleIVA_IdCodice" in vals_norm:
            vals["cedente_IdFiscaleIVA_IdCodice"] = vals_norm["IdFiscaleIVA_IdCodice"]
        return vals

    @api.onchange("partner_cessionario_id")
    def onchange_partner_cessionario_id(self):
        for comunicazione in self:
            if comunicazione.partner_cessionario_id:
                vals = self._prepare_cessionario_partner_id(
                    comunicazione.partner_cessionario_id
                )
                comunicazione.cessionario_IdFiscaleIVA_IdPaese = vals[
                    "cessionario_IdFiscaleIVA_IdPaese"
                ]
                comunicazione.cessionario_IdFiscaleIVA_IdCodice = vals[
                    "cessionario_IdFiscaleIVA_IdCodice"
                ]
                comunicazione.cessionario_CodiceFiscale = vals[
                    "cessionario_CodiceFiscale"
                ]
                comunicazione.cessionario_Denominazione = vals[
                    "cessionario_Denominazione"
                ]
                # Sede
                comunicazione.cessionario_sede_Indirizzo = vals[
                    "cessionario_sede_Indirizzo"
                ]
                comunicazione.cessionario_sede_Cap = vals["cessionario_sede_Cap"]
                comunicazione.cessionario_sede_Comune = vals["cessionario_sede_Comune"]
                comunicazione.cessionario_sede_Provincia = vals[
                    "cessionario_sede_Provincia"
                ]
                comunicazione.cessionario_sede_Nazione = vals[
                    "cessionario_sede_Nazione"
                ]

    def _prepare_cessionario_partner_id(self, partner, vals=None):
        vals = {}
        # ----- Get vat
        partner_vat = partner.commercial_partner_id.vat or ""
        if partner.country_id:
            vals["cessionario_IdFiscaleIVA_IdPaese"] = partner.country_id.code
        elif partner_vat:
            vals["cessionario_IdFiscaleIVA_IdPaese"] = partner_vat[:2]
        else:
            vals["cessionario_IdFiscaleIVA_IdPaese"] = ""
        vals["cessionario_IdFiscaleIVA_IdCodice"] = (
            partner_vat[2:] if partner_vat else ""
        )
        # ----- Get fiscalcode
        vals["cessionario_CodiceFiscale"] = (
            partner.commercial_partner_id.fiscalcode or ""
        )
        vals["cessionario_Denominazione"] = encode_for_export(partner.name or "", 80)
        # Sede
        vals["cessionario_sede_Indirizzo"] = "{} {}".format(
            encode_for_export(partner.street or "", 60),
            encode_for_export(partner.street2 or "", 60),
        ).strip()
        vals["cessionario_sede_Cap"] = encode_for_export(
            partner.zip or "", 5, encoding="ascii"
        )
        vals["cessionario_sede_Comune"] = encode_for_export(partner.city or "", 60)
        vals["cessionario_sede_Provincia"] = (
            partner.state_id and partner.state_id.code or ""
        )
        if partner.country_id:
            vals["cessionario_sede_Nazione"] = partner.country_id.code
        elif partner_vat:
            vals["cessionario_sede_Nazione"] = partner_vat[:2]
        else:
            vals["cessionario_sede_Nazione"] = ""
        # Normalizzazione dati in base alla nazione UE o EXTRA UE:
        vals_norm = {
            "sede_Nazione": vals["cessionario_sede_Nazione"],
            "IdFiscaleIVA_IdCodice": vals["cessionario_IdFiscaleIVA_IdCodice"],
        }
        vals_norm = self._normalizza_dati_partner(partner, vals_norm)
        if "sede_Cap" in vals_norm:
            vals["cessionario_sede_Cap"] = vals_norm["sede_Cap"]
        if "sede_Provincia" in vals_norm:
            vals["cessionario_sede_Provincia"] = vals_norm["sede_Provincia"]
        if "CodiceFiscale" in vals_norm:
            vals["cessionario_CodiceFiscale"] = vals_norm["CodiceFiscale"]
        if "IdFiscaleIVA_IdCodice" in vals_norm:
            vals["cessionario_IdFiscaleIVA_IdCodice"] = vals_norm[
                "IdFiscaleIVA_IdCodice"
            ]
        return vals

    def _normalizza_dati_partner(self, partner, vals):
        # Paesi Esteri :
        # - Rimuovo CAP/provincia che potrebbero dare problemi nella
        #   validazione
        # Paesi UE :
        # - No codice fiscale se presente partita iva
        # Paesi EXTRA-UE :
        # - Non ci sono controlli su id fiscale, ma dato che va messo e può
        # non esistere, viene messa la ragione sociale(troncata a 28)
        if vals["sede_Nazione"] not in ["", "IT"]:
            vals["sede_Cap"] = ""
            vals["sede_Provincia"] = ""
            country = self.env["res.country"].search(
                [("code", "=", vals["sede_Nazione"])]
            )
            if country.intrastat:
                if vals["IdFiscaleIVA_IdCodice"]:
                    vals["CodiceFiscale"] = ""
            if not country.intrastat:
                if not vals["IdFiscaleIVA_IdCodice"]:
                    vals["IdFiscaleIVA_IdCodice"] = partner.name[:28]
        return vals

    def _prepare_fattura_emessa(self, vals, fattura):
        return vals

    def _prepare_fattura_ricevuta(self, vals, fattura):
        return vals

    def _parse_fattura_numero(self, fattura_numero):
        try:
            fattura_numero = fattura_numero[-20:]
        except BaseException:
            pass
        return fattura_numero

    def compute_values(self):
        # Unlink existing lines
        self._unlink_sections()
        for comunicazione in self:
            comunicazione.splitting_note = ""
            # Fatture Emesse
            if comunicazione.dati_trasmissione == "DTE":
                comunicazione.compute_fatture_emesse()
            # Fatture Ricevute
            if comunicazione.dati_trasmissione == "DTR":
                comunicazione.compute_fatture_ricevute()

    def _prepare_cessionari_dati_fatture(self, fatture_emesse, cessionari):
        dati_fatture = []
        posizione = 0
        for cessionario in cessionari:
            fatture = fatture_emesse.filtered(
                lambda fe: fe.partner_id.id == cessionario.id
            )
            vals_fatture = []
            for fattura in fatture:
                posizione += 1
                val = {
                    "posizione": posizione,
                    "invoice_id": fattura.id,
                    "dati_fattura_TipoDocumento": fattura.fiscal_document_type_id.id,
                    "dati_fattura_Data": fattura.invoice_date,
                    "dati_fattura_Numero": self._parse_fattura_numero(fattura.name),
                    "dati_fattura_iva_ids": fattura._get_tax_comunicazione_dati_iva(),
                }
                val = self._prepare_fattura_emessa(val, fattura)
                vals_fatture.append((0, 0, val))

            val_cessionario = {
                "partner_id": cessionario.id,
                "fatture_emesse_body_ids": vals_fatture,
            }
            vals = self._prepare_cessionario_partner_id(cessionario)
            val_cessionario.update(vals)
            dati_fatture.append((0, 0, val_cessionario))
        return dati_fatture

    def compute_fatture_emesse(self):
        self.ensure_one()
        fatture_emesse = self._get_fatture_emesse()
        if fatture_emesse:
            # Cedente
            self.partner_cedente_id = fatture_emesse[0].company_id.partner_id.id
            self.onchange_partner_cedente_id()

            # Cessionari
            cessionari = fatture_emesse.mapped("partner_id")
            dati_fatture = self._prepare_cessionari_dati_fatture(
                fatture_emesse, cessionari
            )
            self.fatture_emesse_ids = dati_fatture

    def _get_fatture_emesse_domain(self):
        domain = [("comunicazione_dati_iva_escludi", "=", True)]
        no_journal_ids = self.env["account.journal"].search(domain).ids
        domain = [
            ("move_type", "in", ["out_invoice", "out_refund"]),
            ("comunicazione_dati_iva_escludi", "=", False),
            ("state", "=", "posted"),
            ("journal_id", "not in", no_journal_ids),
            ("company_id", "=", self.company_id.id),
            ("invoice_date", ">=", self.date_start),
            ("invoice_date", "<=", self.date_end),
            "|",
            ("fiscal_document_type_id.out_invoice", "=", True),
            ("fiscal_document_type_id.out_refund", "=", True),
        ]
        if self.esterometro:
            domain.append(("partner_id.country_id.code", "not in", (False, "IT")))
        return domain

    def _get_fatture_emesse(self):
        self.ensure_one()
        domain = self._get_fatture_emesse_domain()
        return self.env["account.move"].search(domain)

    def _prepare_cedenti_dati_fatture(self, fatture_ricevute, cedenti):
        dati_fatture = []
        posizione = 0
        for cedente in cedenti:
            # Fatture
            fatture = fatture_ricevute.filtered(
                lambda fr: fr.partner_id.id == cedente.id
            )
            vals_fatture = []
            for fattura in fatture:
                posizione += 1
                val = {
                    "posizione": posizione,
                    "invoice_id": fattura.id,
                    "dati_fattura_TipoDocumento": fattura.fiscal_document_type_id.id,
                    "dati_fattura_Data": fattura.invoice_date,
                    "dati_fattura_DataRegistrazione": fattura.date,
                    "dati_fattura_Numero": self._parse_fattura_numero(fattura.ref)
                    or "",
                    "dati_fattura_iva_ids": fattura._get_tax_comunicazione_dati_iva(),
                }
                val = self._prepare_fattura_ricevuta(val, fattura)
                vals_fatture.append((0, 0, val))

            val_cedente = {
                "partner_id": cedente.id,
                "fatture_ricevute_body_ids": vals_fatture,
            }
            vals = self._prepare_cedente_partner_id(cedente)
            val_cedente.update(vals)
            dati_fatture.append((0, 0, val_cedente))
        return dati_fatture

    def compute_fatture_ricevute(self):
        self.ensure_one()
        fatture_ricevute = self._get_fatture_ricevute()
        if fatture_ricevute:
            self.partner_cessionario_id = fatture_ricevute[0].company_id.partner_id.id
            self.onchange_partner_cessionario_id()

            cedenti = fatture_ricevute.mapped("partner_id")
            dati_fatture = self._prepare_cedenti_dati_fatture(fatture_ricevute, cedenti)
            self.fatture_ricevute_ids = dati_fatture

    def _get_fatture_ricevute_domain(self):
        domain = [("comunicazione_dati_iva_escludi", "=", True)]
        no_journal_ids = self.env["account.journal"].search(domain).ids
        domain = [
            ("move_type", "in", ["in_invoice", "in_refund"]),
            ("comunicazione_dati_iva_escludi", "=", False),
            ("state", "=", "posted"),
            ("journal_id", "not in", no_journal_ids),
            ("company_id", "=", self.company_id.id),
            ("invoice_date", ">=", self.date_start),
            ("invoice_date", "<=", self.date_end),
            "|",
            ("fiscal_document_type_id.in_invoice", "=", True),
            ("fiscal_document_type_id.in_refund", "=", True),
        ]
        if self.esterometro:
            domain.append(("partner_id.country_id.code", "not in", (False, "IT")))
        return domain

    def _get_fatture_ricevute(self):
        self.ensure_one()
        domain = self._get_fatture_ricevute_domain()
        return self.env["account.move"].search(domain)

    def _unlink_sections(self):
        for comunicazione in self:
            comunicazione.fatture_emesse_ids.unlink()
            comunicazione.fatture_ricevute_ids.unlink()

        return True

    def split_communication(self):
        self.ensure_one()
        if self.dati_trasmissione == "DTE":
            if not self.check_fatture_emesse_partners():
                fatture_emesse = self.mapped(
                    "fatture_emesse_ids.fatture_emesse_body_ids.invoice_id"
                )
                cessionari = fatture_emesse.mapped("partner_id")
                first_set_ids = cessionari.ids[: len(cessionari) / 2]
                second_set_ids = cessionari.ids[len(cessionari) / 2 :]
                first_set_cessionari = self.env["res.partner"].browse(first_set_ids)
                second_set_cessionari = self.env["res.partner"].browse(second_set_ids)
                self._unlink_sections()
                dati_fatture_1 = self._prepare_cessionari_dati_fatture(
                    fatture_emesse, first_set_cessionari
                )
                self.fatture_emesse_ids = dati_fatture_1
                self.splitting_note = _(
                    "Splitted considering partners\n%s"
                    % "\n".join(first_set_cessionari.mapped("name"))
                )
                comm_2 = self.copy()
                comm_2._unlink_sections()
                dati_fatture_2 = self._prepare_cessionari_dati_fatture(
                    fatture_emesse, second_set_cessionari
                )
                comm_2.fatture_emesse_ids = dati_fatture_2
                comm_2.splitting_note = _(
                    "Splitted considering partners\n%s"
                    % "\n".join(second_set_cessionari.mapped("name"))
                )
                return self | comm_2
            elif not self.check_fatture_emesse_body():
                fatture_emesse = self.mapped(
                    "fatture_emesse_ids.fatture_emesse_body_ids.invoice_id"
                )
                cessionari = fatture_emesse.mapped("partner_id")
                new_set = self.env["account.move"]
                old_set = fatture_emesse
                for cessionario in cessionari:
                    fatture = fatture_emesse.filtered(
                        lambda fe: fe.partner_id.id == cessionario.id
                    )
                    if len(fatture) > 1000:
                        new_set_ids = fatture.ids[: len(fatture) / 2]
                        new_partial_set = self.env["account.move"].browse(new_set_ids)
                        new_set |= new_partial_set
                        old_set -= new_partial_set
                self._unlink_sections()
                cessionari_1 = old_set.mapped("partner_id")
                dati_fatture_1 = self._prepare_cessionari_dati_fatture(
                    old_set, cessionari_1
                )
                self.fatture_emesse_ids = dati_fatture_1
                self.splitting_note = _(
                    "Splitted considering invoices\n%s"
                    % "\n".join(old_set.mapped("name"))
                )
                comm_2 = self.copy()
                comm_2._unlink_sections()
                cessionari_2 = new_set.mapped("partner_id")
                dati_fatture_2 = self._prepare_cessionari_dati_fatture(
                    new_set, cessionari_2
                )
                comm_2.fatture_emesse_ids = dati_fatture_2
                comm_2.splitting_note = _(
                    "Splitted considering invoices\n%s"
                    % "\n".join(new_set.mapped("name"))
                )
                return self | comm_2

        elif self.dati_trasmissione == "DTR":
            if not self.check_fatture_ricevute_partners():
                fatture_ricevute = self.mapped(
                    "fatture_ricevute_ids.fatture_ricevute_body_ids.invoice_id"
                )
                cedenti = fatture_ricevute.mapped("partner_id")
                first_set_ids = cedenti.ids[: len(cedenti) / 2]
                second_set_ids = cedenti.ids[len(cedenti) / 2 :]
                first_set_cedenti = self.env["res.partner"].browse(first_set_ids)
                second_set_cedenti = self.env["res.partner"].browse(second_set_ids)
                self._unlink_sections()
                dati_fatture_1 = self._prepare_cedenti_dati_fatture(
                    fatture_ricevute, first_set_cedenti
                )
                self.fatture_ricevute_ids = dati_fatture_1
                self.splitting_note = _(
                    "Splitted considering partners\n%s"
                    % "\n".join(first_set_cedenti.mapped("name"))
                )
                comm_2 = self.copy()
                comm_2._unlink_sections()
                dati_fatture_2 = self._prepare_cedenti_dati_fatture(
                    fatture_ricevute, second_set_cedenti
                )
                comm_2.fatture_ricevute_ids = dati_fatture_2
                comm_2.splitting_note = _(
                    "Splitted considering partners\n%s"
                    % "\n".join(second_set_cedenti.mapped("name"))
                )
                return self | comm_2
            elif not self.check_fatture_ricevute_body():
                fatture_ricevute = self.mapped(
                    "fatture_ricevute_ids.fatture_ricevute_body_ids.invoice_id"
                )
                cedenti = fatture_ricevute.mapped("partner_id")
                new_set = self.env["account.move"]
                old_set = fatture_ricevute
                for cedente in cedenti:
                    fatture = fatture_ricevute.filtered(
                        lambda fr: fr.partner_id.id == cedente.id
                    )
                    if len(fatture) > 1000:
                        new_set_ids = fatture.ids[: len(fatture) / 2]
                        new_partial_set = self.env["account.move"].browse(new_set_ids)
                        new_set |= new_partial_set
                        old_set -= new_partial_set
                self._unlink_sections()
                cedenti_1 = old_set.mapped("partner_id")
                dati_fatture_1 = self._prepare_cedenti_dati_fatture(old_set, cedenti_1)
                self.fatture_ricevute_ids = dati_fatture_1
                self.splitting_note = _(
                    "Splitted considering invoices\n%s"
                    % "\n".join(old_set.mapped("name"))
                )
                comm_2 = self.copy()
                comm_2._unlink_sections()
                cedenti_2 = new_set.mapped("partner_id")
                dati_fatture_2 = self._prepare_cedenti_dati_fatture(new_set, cedenti_2)
                comm_2.fatture_ricevute_ids = dati_fatture_2
                comm_2.splitting_note = _(
                    "Splitted considering invoices\n%s"
                    % "\n".join(new_set.mapped("name"))
                )
                return self | comm_2

    def split_communications(self):
        res = self.env["comunicazione.dati.iva"]
        for com in self:
            if com.check_1k_limit():
                res |= com
            else:
                new_communications = com.split_communication()
                res |= new_communications.split_communications()
        return res

    def check_1k_limit(self):
        self.ensure_one()
        if (
            self.check_fatture_emesse_body()
            and self.check_fatture_emesse_partners()
            and self.check_fatture_ricevute_body()
            and self.check_fatture_ricevute_partners()
        ):
            return True
        return False

    def check_fatture_emesse_body(self):
        for line in self.fatture_emesse_ids:
            invoices_limit = len(line.fatture_emesse_body_ids)
            if invoices_limit > 1000:
                return False
        return True

    def check_fatture_emesse_partners(self):
        if len(self.fatture_emesse_ids) > 1000:
            return False
        return True

    def check_fatture_ricevute_body(self):
        for line in self.fatture_ricevute_ids:
            invoices_limit = len(line.fatture_ricevute_body_ids)
            if invoices_limit > 1000:
                return False
        return True

    def check_fatture_ricevute_partners(self):
        if len(self.fatture_ricevute_ids) > 1000:
            return False
        return True

    def _check_errors_dte(self):  # noqa
        self.ensure_one()
        comunicazione = self
        errors = []
        # ----- Conta il limite di partner e fatture
        partner_limit = 0
        for line in comunicazione.fatture_emesse_ids:
            partner_limit += 1
            invoices_limit = len(line.fatture_emesse_body_ids)
            if invoices_limit > 1000:
                errors += [
                    _("Limit of 1000 invoices per assignee (%s) exceeded")
                    % line.partner_id.display_name
                ]
        if partner_limit > 1000:
            errors += [_("Limit of 1000 assignees per communication exceeded")]
        # ----- Cedente
        # -----     Normalizzazione delle stringhe
        if not check_normalized_string(comunicazione.cedente_Denominazione):
            errors.append(_("Remove empty characters around seller's denomination"))
        if not check_normalized_string(comunicazione.cedente_Nome):
            errors.append(_("Remove empty characters around seller's name"))
        if not check_normalized_string(comunicazione.cedente_Cognome):
            errors.append(_("Remove empty characters around seller's surname"))
        if not check_normalized_string(comunicazione.cedente_sede_Indirizzo):
            errors.append(
                _("Remove empty characters around seller's headquarters " "address")
            )
        if not check_normalized_string(comunicazione.cedente_sede_NumeroCivico):
            errors.append(_("Remove empty characters around seller's street number"))
        if not check_normalized_string(comunicazione.cedente_sede_Comune):
            errors.append(_("Remove empty characters around seller's city"))
        if not check_normalized_string(comunicazione.cedente_so_Indirizzo):
            errors.append(
                _(
                    "Remove empty characters around address of permanent "
                    "establishment"
                )
            )
        if not check_normalized_string(comunicazione.cedente_so_NumeroCivico):
            errors.append(
                _(
                    "Remove empty characters around street number of permanent "
                    "establishment"
                )
            )
        if not check_normalized_string(comunicazione.cedente_so_Comune):
            errors.append(
                _("Remove empty characters around city of permanent " "establishment")
            )
        if not check_normalized_string(comunicazione.cedente_rf_Denominazione):
            errors.append(
                _(
                    "Remove empty characters around denomination of fiscal "
                    "representative"
                )
            )
        if not check_normalized_string(comunicazione.cedente_rf_Nome):
            errors.append(
                _("Remove empty characters around name of fiscal " "representative")
            )
        if not check_normalized_string(comunicazione.cedente_rf_Cognome):
            errors.append(
                _("Remove empty characters around surname of fiscal " "representative")
            )
        # ----- Cessionario
        for partner in comunicazione.fatture_emesse_ids:
            # -----     Normalizzazione delle stringhe
            if not check_normalized_string(partner.cessionario_Denominazione):
                errors.append(
                    _("Remove empty characters around denomination of assignee " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_Nome):
                errors.append(
                    _("Remove empty characters around name of assignee " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_Cognome):
                errors.append(
                    _("Remove empty characters around surname of assignee " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_sede_Indirizzo):
                errors.append(
                    _(
                        "Remove empty characters around headquarters address of "
                        "assignee %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_sede_NumeroCivico):
                errors.append(
                    _("Remove empty characters around street number of assignee" " %s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_sede_Comune):
                errors.append(
                    _("Remove empty characters around city of assignee " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_so_Indirizzo):
                errors.append(
                    _(
                        "Remove empty characters around address of permanent "
                        "establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_so_NumeroCivico):
                errors.append(
                    _(
                        "Remove empty characters around street number of "
                        "permanent establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_so_Comune):
                errors.append(
                    _(
                        "Remove empty characters around city of permanent "
                        "establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_rf_Denominazione):
                errors.append(
                    _(
                        "Remove empty characters around denomination of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_rf_Nome):
                errors.append(
                    _(
                        "Remove empty characters around name of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cessionario_rf_Cognome):
                errors.append(
                    _(
                        "Remove empty characters around surname of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            # ----- Dati fiscali
            if (
                not partner.cessionario_IdFiscaleIVA_IdPaese
                and partner.cessionario_IdFiscaleIVA_IdCodice
            ):
                errors.append(
                    _("Define a country ID for assignee %s")
                    % partner.partner_id.display_name
                )
            # ----- Dati Sede
            if not all(
                [
                    partner.cessionario_sede_Indirizzo,
                    partner.cessionario_sede_Comune,
                    partner.cessionario_sede_Nazione,
                ]
            ):
                errors.append(
                    _("Address, city, country of %s are mandatory")
                    % partner.partner_id.display_name
                )
            # ----- Dati Stabile Organizzazione
            if any(
                [
                    partner.cessionario_so_Indirizzo,
                    partner.cessionario_so_NumeroCivico,
                    partner.cessionario_so_Cap,
                    partner.cessionario_so_Comune,
                    partner.cessionario_so_Provincia,
                    partner.cessionario_so_Nazione,
                ]
            ) and not all(
                [
                    partner.cessionario_so_Indirizzo,
                    partner.cessionario_so_Comune,
                    partner.cessionario_so_Cap,
                    partner.cessionario_so_Nazione,
                ]
            ):
                errors.append(
                    _(
                        "Address, city, ZIP and country of permanent "
                        "establishment %s are mandatory, when at least one value "
                        "is defined"
                    )
                    % partner.partner_id.display_name
                )
            # ----- Rappresentante Fiscale
            if any(
                [
                    partner.cessionario_rf_IdFiscaleIVA_IdPaese,
                    partner.cessionario_rf_IdFiscaleIVA_IdCodice,
                    partner.cessionario_rf_Denominazione,
                    partner.cessionario_rf_Nome,
                    partner.cessionario_rf_Cognome,
                ]
            ) and not all(
                [
                    partner.cessionario_rf_IdFiscaleIVA_IdPaese,
                    partner.cessionario_rf_IdFiscaleIVA_IdCodice,
                ]
            ):
                errors.append(
                    _(
                        "Country ID and fiscal identifier of fiscal "
                        "representative %s are mandatory, when at least one "
                        "value is defined"
                    )
                    % partner.partner_id.display_name
                )
            # ----- CAP
            if partner.cessionario_sede_Cap and not re.match(
                "[0-9]{5}", partner.cessionario_sede_Cap
            ):
                errors.append(
                    _("ZIP %s of assignee %s is not 5 numeric characters")
                    % (partner.cessionario_sede_Cap, partner.partner_id.display_name)
                )
            # ----- Dettagli IVA
            for invoice in partner.fatture_emesse_body_ids:
                if not invoice.dati_fattura_iva_ids:
                    errors.append(
                        _("No VAT data defined for invoice %s of partner %s")
                        % (invoice.invoice_id.name, partner.partner_id.display_name)
                    )
        return errors

    def _check_errors_dtr(self):  # noqa
        self.ensure_one()
        comunicazione = self
        errors = []
        # ----- Conta il limite di partner e fatture
        partner_limit = 0
        for line in comunicazione.fatture_ricevute_ids:
            partner_limit += 1
            invoices_limit = len(line.fatture_ricevute_body_ids)
            if invoices_limit > 1000:
                errors += [
                    _("Limit of 1000 invoices per assignee (%s) exceeded")
                    % line.partner_id.display_name
                ]
        if partner_limit > 1000:
            errors += [_("Limit of 1000 assignees per communication exceeded")]
        # ----- Cessionario
        # -----     Normalizzazione delle stringhe
        if not check_normalized_string(comunicazione.cessionario_Denominazione):
            errors.append(_("Remove empty characters around assignee's denomination"))
        if not check_normalized_string(comunicazione.cessionario_Nome):
            errors.append(_("Remove empty characters around assignee's name"))
        if not check_normalized_string(comunicazione.cessionario_Cognome):
            errors.append(_("Remove empty characters around assignee's surname"))
        if not check_normalized_string(comunicazione.cessionario_sede_Indirizzo):
            errors.append(
                _("Remove empty characters around assignee's headquarters " "address")
            )
        if not check_normalized_string(comunicazione.cessionario_sede_NumeroCivico):
            errors.append(_("Remove empty characters around assignee's street number"))
        if not check_normalized_string(comunicazione.cessionario_sede_Comune):
            errors.append(_("Remove empty characters around assignee's city"))
        if not check_normalized_string(comunicazione.cessionario_so_Indirizzo):
            errors.append(
                _(
                    "Remove empty characters around address of permanent "
                    "establishment"
                )
            )
        if not check_normalized_string(comunicazione.cessionario_so_NumeroCivico):
            errors.append(
                _(
                    "Remove empty characters around street number of permanent "
                    "establishment"
                )
            )
        if not check_normalized_string(comunicazione.cessionario_so_Comune):
            errors.append(
                _("Remove empty characters around city of permanent " "establishment")
            )
        if not check_normalized_string(comunicazione.cessionario_rf_Denominazione):
            errors.append(
                _(
                    "Remove empty characters around denomination of fiscal "
                    "representative"
                )
            )
        if not check_normalized_string(comunicazione.cessionario_rf_Nome):
            errors.append(
                _("Remove empty characters around name of fiscal " "representative")
            )
        if not check_normalized_string(comunicazione.cessionario_rf_Cognome):
            errors.append(
                _("Remove empty characters around surname of fiscal " "representative")
            )
        # ----- Cedente
        for partner in comunicazione.fatture_ricevute_ids:
            # -----     Normalizzazione delle stringhe
            if not check_normalized_string(partner.cedente_Denominazione):
                errors.append(
                    _("Remove empty characters around denomination of seller " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_Nome):
                errors.append(
                    _("Remove empty characters around name of seller " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_Cognome):
                errors.append(
                    _("Remove empty characters around surname of seller " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_sede_Indirizzo):
                errors.append(
                    _(
                        "Remove empty characters around headquarters address of "
                        "seller %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_sede_NumeroCivico):
                errors.append(
                    _("Remove empty characters around street number of seller " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_sede_Comune):
                errors.append(
                    _("Remove empty characters around city of seller " "%s")
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_so_Indirizzo):
                errors.append(
                    _(
                        "Remove empty characters around address of permanent "
                        "establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_so_NumeroCivico):
                errors.append(
                    _(
                        "Remove empty characters around street number of "
                        "permanent establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_so_Comune):
                errors.append(
                    _(
                        "Remove empty characters around city of permanent "
                        "establishment %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_rf_Denominazione):
                errors.append(
                    _(
                        "Remove empty characters around denomination of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_rf_Nome):
                errors.append(
                    _(
                        "Remove empty characters around name of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            if not check_normalized_string(partner.cedente_rf_Cognome):
                errors.append(
                    _(
                        "Remove empty characters around surname of fiscal "
                        "representative %s"
                    )
                    % partner.partner_id.display_name
                )
            # ----- Dati fiscali
            if (
                not partner.cedente_IdFiscaleIVA_IdPaese
                and partner.cedente_IdFiscaleIVA_IdCodice
            ):
                errors.append(
                    _("Define a country ID for seller %s")
                    % partner.partner_id.display_name
                )
            # ----- Dati Sede
            if not all(
                [
                    partner.cedente_sede_Indirizzo,
                    partner.cedente_sede_Comune,
                    partner.cedente_sede_Nazione,
                ]
            ):
                errors.append(
                    _("Address, city, country of %s are mandatory")
                    % partner.partner_id.display_name
                )
            # ----- Dati Stabile Organizzazione
            if any(
                [
                    partner.cedente_so_Indirizzo,
                    partner.cedente_so_NumeroCivico,
                    partner.cedente_so_Cap,
                    partner.cedente_so_Comune,
                    partner.cedente_so_Provincia,
                    partner.cedente_so_Nazione,
                ]
            ) and not all(
                [
                    partner.cedente_so_Indirizzo,
                    partner.cedente_so_Comune,
                    partner.cedente_so_Cap,
                    partner.cedente_so_Nazione,
                ]
            ):
                errors.append(
                    _(
                        "Address, city, ZIP and country of permanent "
                        "establishment %s are mandatory, when at least one value "
                        "is defined"
                    )
                    % partner.partner_id.display_name
                )
            # ----- Rappresentante Fiscale
            if any(
                [
                    partner.cedente_rf_IdFiscaleIVA_IdPaese,
                    partner.cedente_rf_IdFiscaleIVA_IdCodice,
                    partner.cedente_rf_Denominazione,
                    partner.cedente_rf_Nome,
                    partner.cedente_rf_Cognome,
                ]
            ) and not all(
                [
                    partner.cedente_rf_IdFiscaleIVA_IdPaese,
                    partner.cedente_rf_IdFiscaleIVA_IdCodice,
                ]
            ):
                errors.append(
                    _(
                        "Country ID and fiscal identifier of fiscal "
                        "representative %s are mandatory, when at least one "
                        "value is defined"
                    )
                    % partner.partner_id.display_name
                )
            # ----- CAP
            if partner.cedente_sede_Cap and not re.match(
                "[0-9]{5}", partner.cedente_sede_Cap
            ):
                errors.append(
                    _("ZIP %s of seller %s is not 5 characters")
                    % (partner.cedente_sede_Cap, partner.partner_id.display_name)
                )
            # ----- Dettagli IVA
            for invoice in partner.fatture_ricevute_body_ids:
                if not invoice.dati_fattura_iva_ids:
                    errors.append(
                        _("No VAT data defined for invoice %s of partner %s")
                        % (invoice.invoice_id.name, partner.partner_id.display_name)
                    )
                if not invoice.dati_fattura_Numero:
                    errors.append(
                        _("No invoice number for supplier bill %s")
                        % (invoice.invoice_id.name)
                    )
                if not invoice.dati_fattura_DataRegistrazione:
                    errors.append(
                        _("No registration date for supplier bill %s")
                        % (invoice.invoice_id.name)
                    )
        return errors

    def check_errors(self):
        for comunicazione in self:
            errors = []
            if comunicazione.dati_trasmissione == "DTE":
                errors += comunicazione._check_errors_dte()
            elif comunicazione.dati_trasmissione == "DTR":
                errors += comunicazione._check_errors_dtr()
            if not errors:
                errors = [
                    _("All data are correct.\nIt's possible to export " "XML file")
                ]
            else:
                errors = [_("Errors:")] + errors
            comunicazione.errors = "\n - ".join(errors)

    def _validate(self):
        """
        Controllo congruità dati della comunicazione
        """
        return True

    def _export_xml_get_dati_fattura(self):
        # ----- 0 - Dati Fattura
        attrs = {"versione": VERSION}
        x_0_dati_fattura = etree.Element(
            etree.QName(NS_2, "DatiFattura"), attrib=attrs, nsmap=NS_MAP
        )
        return x_0_dati_fattura

    def _export_xml_get_dati_fattura_header(self):
        # ----- 1 - Dati Fattura
        x_1_dati_fattura_header = etree.Element(etree.QName("DatiFatturaHeader"))
        # ----- 1.1 - Progressivo Invio
        x_1_1_progressivo_invio = etree.SubElement(
            x_1_dati_fattura_header, etree.QName("ProgressivoInvio")
        )
        x_1_1_progressivo_invio.text = str(self.identificativo)

        # Nota del file excel:
        # Questo blocco va valorizzato solo se il soggetto obbligato
        # alla comunicazione dei dati fattura non coincide con
        # il soggetto passivo IVA al quale i dati si riferiscono.
        # NON deve essere valorizzato se per il soggetto trasmittente
        # è vera una delle seguenti affermazioni:
        # - coincide  con il soggetto IVA al quale i dati si riferiscono;
        # - è legato da vincolo di incarico con il soggetto IVA al quale i dati
        #     si riferiscono;
        # - è un intermediario.
        # In tutti gli altri casi questo blocco DEVE essere valorizzato.

        # ----- 1.2 - Dichiarante
        x_1_2_dichiarante = etree.SubElement(
            x_1_dati_fattura_header, etree.QName("Dichiarante")
        )
        # ----- 1.2.1 - Codice Fiscale
        x_1_2_1_codice_fiscale = etree.SubElement(
            x_1_2_dichiarante, etree.QName("CodiceFiscale")
        )
        x_1_2_1_codice_fiscale.text = self.declarant_fiscalcode or ""
        # ----- 1.2.2 - Carica
        x_1_2_2_carica = etree.SubElement(x_1_2_dichiarante, etree.QName("Carica"))
        x_1_2_2_carica.text = (
            self.codice_carica_id.code if self.codice_carica_id else ""
        )
        return x_1_dati_fattura_header

    def _export_xml_get_dte(self):
        # ----- 2 - DTE
        x_2_dte = etree.Element(etree.QName("DTE"))
        # -----     2.1 - Cedente Prestatore DTE
        x_2_1_cedente_prestatore = etree.SubElement(
            x_2_dte, etree.QName("CedentePrestatoreDTE")
        )
        # -----         2.1.1 - IdentificativiFiscali
        x_2_1_1_identificativi_fiscali = etree.SubElement(
            x_2_1_cedente_prestatore, etree.QName("IdentificativiFiscali")
        )
        # -----             2.1.1.1 - Id Fiscale IVA
        x_2_1_1_1_id_fiscale_iva = etree.SubElement(
            x_2_1_1_identificativi_fiscali, etree.QName("IdFiscaleIVA")
        )
        # -----                 2.1.1.1.1 - Id Paese
        x_2_1_1_1_1_id_paese = etree.SubElement(
            x_2_1_1_1_id_fiscale_iva, etree.QName("IdPaese")
        )
        x_2_1_1_1_1_id_paese.text = self.cedente_IdFiscaleIVA_IdPaese or ""
        # -----                 2.1.1.1.2 - Id Codice
        x_2_1_1_1_2_id_codice = etree.SubElement(
            x_2_1_1_1_id_fiscale_iva, etree.QName("IdCodice")
        )
        x_2_1_1_1_2_id_codice.text = self.cedente_IdFiscaleIVA_IdCodice or ""
        # -----             2.1.1.2 - Codice Fiscale
        x_2_1_1_2_codice_fiscale = etree.SubElement(
            x_2_1_1_identificativi_fiscali, etree.QName("CodiceFiscale")
        )
        x_2_1_1_2_codice_fiscale.text = self.cedente_CodiceFiscale or ""
        # -----         2.1.2 - AltriDatiIdentificativi
        x_2_1_2_altri_identificativi = etree.SubElement(
            x_2_1_cedente_prestatore, etree.QName("AltriDatiIdentificativi")
        )
        # -----             2.1.2.1 - Denominazione
        x_2_1_2_1_denominazione = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("Denominazione")
        )
        x_2_1_2_1_denominazione.text = self.cedente_Denominazione or ""
        # -----             2.1.2.2 - Nome
        x_2_1_2_2_nome = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("Nome")
        )
        x_2_1_2_2_nome.text = self.cedente_Nome or ""
        # -----             2.1.2.3 - Cognome
        x_2_1_2_3_cognome = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("Cognome")
        )
        x_2_1_2_3_cognome.text = self.cedente_Cognome or ""
        # -----             2.1.2.4 - Sede
        x_2_1_2_4_sede = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("Sede")
        )
        # -----                 2.1.2.4.1 - Indirizzo
        x_2_1_2_4_1_indirizzo = etree.SubElement(
            x_2_1_2_4_sede, etree.QName("Indirizzo")
        )
        x_2_1_2_4_1_indirizzo.text = self.cedente_sede_Indirizzo or ""
        # -----                 2.1.2.4.2 - Numero Civico
        x_2_1_2_4_2_numero_civico = etree.SubElement(
            x_2_1_2_4_sede, etree.QName("NumeroCivico")
        )
        x_2_1_2_4_2_numero_civico.text = self.cedente_sede_NumeroCivico or ""
        # -----                 2.1.2.4.3 - CAP
        x_2_1_2_4_3_cap = etree.SubElement(x_2_1_2_4_sede, etree.QName("CAP"))
        x_2_1_2_4_3_cap.text = self.cedente_sede_Cap or ""
        # -----                 2.1.2.4.4 - Comune
        x_2_1_2_4_4_comune = etree.SubElement(x_2_1_2_4_sede, etree.QName("Comune"))
        x_2_1_2_4_4_comune.text = self.cedente_sede_Comune or ""
        # -----                 2.1.2.4.5 - Provincia
        x_2_1_2_4_5_provincia = etree.SubElement(
            x_2_1_2_4_sede, etree.QName("Provincia")
        )
        x_2_1_2_4_5_provincia.text = self.cedente_sede_Provincia or ""
        # -----                 2.1.2.4.6 - Nazione
        x_2_1_2_4_6_nazione = etree.SubElement(x_2_1_2_4_sede, etree.QName("Nazione"))
        x_2_1_2_4_6_nazione.text = self.cedente_sede_Nazione or ""
        # -----             2.1.2.5 - Stabile Organizzazione
        x_2_1_2_5_stabile_organizzazione = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("StabileOrganizzazione")
        )
        # -----                 2.1.2.5.1 - Indirizzo
        x_2_1_2_5_1_indirizzo = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("Indirizzo")
        )
        x_2_1_2_5_1_indirizzo.text = self.cedente_so_Indirizzo or ""
        # -----                 2.1.2.5.2 - Numero Civico
        x_2_1_2_5_2_numero_civico = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("Numerocivico")
        )
        x_2_1_2_5_2_numero_civico.text = self.cedente_so_NumeroCivico or ""
        # -----                 2.1.2.5.3 - CAP
        x_2_1_2_5_3_cap = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("CAP")
        )
        x_2_1_2_5_3_cap.text = self.cedente_so_Cap or ""
        # -----                 2.1.2.5.4 - Comune
        x_2_1_2_5_4_comune = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("Comune")
        )
        x_2_1_2_5_4_comune.text = self.cedente_so_Comune or ""
        # -----                 2.1.2.5.5 - Provincia
        x_2_1_2_5_5_provincia = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("Provincia")
        )
        x_2_1_2_5_5_provincia.text = self.cedente_so_Provincia or ""
        # -----                 2.1.2.5.6 - Nazione
        x_2_1_2_5_6_nazione = etree.SubElement(
            x_2_1_2_5_stabile_organizzazione, etree.QName("Nazione")
        )
        x_2_1_2_5_6_nazione.text = self.cedente_so_Nazione or ""
        # -----             2.1.2.6 - Rappresentante Fiscale
        x_2_1_2_6_rappresentante_fiscale = etree.SubElement(
            x_2_1_2_altri_identificativi, etree.QName("RappresentanteFiscale")
        )
        # -----                 2.1.2.6.1 - Id Fiscale IVA
        x_2_1_2_6_1_id_fiscale_iva = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale, etree.QName("IdFiscaleIVA")
        )
        # -----                     2.1.2.6.1.1 - Id Paese
        x_2_1_2_6_1_1_id_paese = etree.SubElement(
            x_2_1_2_6_1_id_fiscale_iva, etree.QName("IdPaese")
        )
        x_2_1_2_6_1_1_id_paese.text = self.cedente_rf_IdFiscaleIVA_IdPaese or ""
        # -----                     2.1.2.6.1.2 - Id Codice
        x_2_1_2_6_1_2_id_codice = etree.SubElement(
            x_2_1_2_6_1_id_fiscale_iva, etree.QName("IdCodice")
        )
        x_2_1_2_6_1_2_id_codice.text = self.cedente_rf_IdFiscaleIVA_IdCodice or ""
        # -----                 2.1.2.6.2 - Denominazione
        x_2_1_2_6_2_denominazione = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale, etree.QName("Denominazione")
        )
        x_2_1_2_6_2_denominazione.text = self.cedente_rf_Denominazione or ""
        # -----                 2.1.2.6.3 - Nome
        x_2_1_2_6_3_nome = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale, etree.QName("Nome")
        )
        x_2_1_2_6_3_nome.text = self.cedente_rf_Nome or ""
        # -----                 2.1.2.6.4 - Cognome
        x_2_1_2_6_4_cognome = etree.SubElement(
            x_2_1_2_6_rappresentante_fiscale, etree.QName("Cognome")
        )
        x_2_1_2_6_4_cognome.text = self.cedente_rf_Cognome or ""

        for partner_invoice in self.fatture_emesse_ids:
            # -----     2.2 - Cessionario Committente DTE
            x_2_2_cessionario_committente = etree.SubElement(
                x_2_dte, etree.QName("CessionarioCommittenteDTE")
            )
            # -----         2.2.1 - IdentificativiFiscali
            x_2_2_1_identificativi_fiscali = etree.SubElement(
                x_2_2_cessionario_committente, etree.QName("IdentificativiFiscali")
            )
            if (
                partner_invoice.cessionario_IdFiscaleIVA_IdPaese
                and partner_invoice.cessionario_IdFiscaleIVA_IdCodice
            ):
                # -----             2.2.1.1 - Id Fiscale IVA
                x_2_2_1_1_id_fiscale_iva = etree.SubElement(
                    x_2_2_1_identificativi_fiscali, etree.QName("IdFiscaleIVA")
                )
                # -----                 2.2.1.1.1 - Id Paese
                x_2_2_1_1_1_id_paese = etree.SubElement(
                    x_2_2_1_1_id_fiscale_iva, etree.QName("IdPaese")
                )
                x_2_2_1_1_1_id_paese.text = (
                    partner_invoice.cessionario_IdFiscaleIVA_IdPaese or ""
                )
                # -----                 2.2.1.1.2 - Id Codice
                x_2_2_1_1_2_id_codice = etree.SubElement(
                    x_2_2_1_1_id_fiscale_iva, etree.QName("IdCodice")
                )
                x_2_2_1_1_2_id_codice.text = (
                    partner_invoice.cessionario_IdFiscaleIVA_IdCodice or ""
                )
            # -----             2.2.1.2 - Codice Fiscale
            x_2_2_1_2_codice_fiscale = etree.SubElement(
                x_2_2_1_identificativi_fiscali, etree.QName("CodiceFiscale")
            )
            x_2_2_1_2_codice_fiscale.text = (
                partner_invoice.cessionario_CodiceFiscale or ""
            )
            # -----         2.2.2 - AltriDatiIdentificativi
            x_2_2_2_altri_identificativi = etree.SubElement(
                x_2_2_cessionario_committente, etree.QName("AltriDatiIdentificativi")
            )
            # -----             2.2.2.1 - Denominazione
            x_2_2_2_1_altri_identificativi_denominazione = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("Denominazione")
            )
            x_2_2_2_1_altri_identificativi_denominazione.text = encode_for_export(
                partner_invoice.cessionario_Denominazione or "", 80
            )
            # -----             2.2.2.2 - Nome
            x_2_2_2_2_nome = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("Nome")
            )
            x_2_2_2_2_nome.text = encode_for_export(
                partner_invoice.cessionario_Nome or "", 60
            )
            # -----             2.2.2.3 - Cognome
            x_2_2_2_3_cognome = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("Cognome")
            )
            x_2_2_2_3_cognome.text = encode_for_export(
                partner_invoice.cessionario_Cognome or "", 60
            )
            # -----             2.2.2.4 - Sede
            x_2_2_2_4_sede = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("Sede")
            )
            # -----                 2.2.2.4.1 - Indirizzo
            x_2_2_2_4_1_indirizzo = etree.SubElement(
                x_2_2_2_4_sede, etree.QName("Indirizzo")
            )
            x_2_2_2_4_1_indirizzo.text = encode_for_export(
                partner_invoice.cessionario_sede_Indirizzo or "", 60
            )
            # -----                 2.2.2.4.2 - Numero Civico
            x_2_2_2_4_2_numero_civico = etree.SubElement(
                x_2_2_2_4_sede, etree.QName("NumeroCivico")
            )
            x_2_2_2_4_2_numero_civico.text = encode_for_export(
                partner_invoice.cessionario_sede_NumeroCivico or "", 8, encoding="ascii"
            )
            # -----                 2.2.2.4.3 - CAP
            x_2_2_2_4_3_cap = etree.SubElement(x_2_2_2_4_sede, etree.QName("CAP"))
            x_2_2_2_4_3_cap.text = encode_for_export(
                partner_invoice.cessionario_sede_Cap or "", 5, encoding="ascii"
            )
            # -----                 2.2.2.4.4 - Comune
            x_2_2_2_4_4_comune = etree.SubElement(x_2_2_2_4_sede, etree.QName("Comune"))
            x_2_2_2_4_4_comune.text = encode_for_export(
                partner_invoice.cessionario_sede_Comune or "", 60
            )
            # -----                 2.2.2.4.5 - Provincia
            x_2_2_2_4_5_provincia = etree.SubElement(
                x_2_2_2_4_sede, etree.QName("Provincia")
            )
            x_2_2_2_4_5_provincia.text = (
                partner_invoice.cessionario_sede_Provincia or ""
            )
            # -----                 2.2.2.4.6 - Nazione
            x_2_2_2_4_6_nazione = etree.SubElement(
                x_2_2_2_4_sede, etree.QName("Nazione")
            )
            x_2_2_2_4_6_nazione.text = partner_invoice.cessionario_sede_Nazione or ""
            # -----             2.2.2.5 - Stabile Organizzazione
            x_2_2_2_5_stabile_organizzazione = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("StabileOrganizzazione")
            )
            # -----                 2.2.2.5.1 - Indirizzo
            x_2_2_2_5_1_indirizzo = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("Indirizzo")
            )
            x_2_2_2_5_1_indirizzo.text = encode_for_export(
                partner_invoice.cessionario_so_Indirizzo or "", 60
            )
            # -----                 2.2.2.5.2 - Numero Civico
            x_2_2_2_5_2_numero_civico = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("NumeroCivico")
            )
            x_2_2_2_5_2_numero_civico.text = encode_for_export(
                partner_invoice.cessionario_so_NumeroCivico or "", 8, encoding="ascii"
            )
            # -----                 2.2.2.5.3 - CAP
            x_2_2_2_5_3_cap = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("CAP")
            )
            x_2_2_2_5_3_cap.text = encode_for_export(
                partner_invoice.cessionario_so_Cap or "", 5, encoding="ascii"
            )
            # -----                 2.2.2.5.4 - Comune
            x_2_2_2_5_4_comune = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("Comune")
            )
            x_2_2_2_5_4_comune.text = encode_for_export(
                partner_invoice.cessionario_so_Comune or "", 60
            )
            # -----                 2.2.2.5.5 - Provincia
            x_2_2_2_5_5_provincia = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("Provincia")
            )
            x_2_2_2_5_5_provincia.text = partner_invoice.cessionario_so_Provincia or ""
            # -----                 2.2.2.5.6 - Nazione
            x_2_2_2_5_6_nazione = etree.SubElement(
                x_2_2_2_5_stabile_organizzazione, etree.QName("Nazione")
            )
            x_2_2_2_5_6_nazione.text = partner_invoice.cessionario_so_Nazione or ""
            # -----             2.2.2.6 - Rappresentante Fiscale
            x_2_2_2_6_rappresentante_fiscale = etree.SubElement(
                x_2_2_2_altri_identificativi, etree.QName("RappresentanteFiscale")
            )
            # -----                 2.2.2.6.1 - Id Fiscale IVA
            x_2_2_2_6_1_id_fiscale_iva = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale, etree.QName("IdFiscaleIVA")
            )
            x_2_2_2_6_rappresentante_fiscale.text = (
                partner_invoice.cessionario_rf_IdFiscaleIVA_IdPaese or ""
            )
            # -----                     2.2.2.6.1.1 - Id Paese
            x_2_2_2_6_1_1_id_paese = etree.SubElement(
                x_2_2_2_6_1_id_fiscale_iva, etree.QName("IdPaese")
            )
            x_2_2_2_6_1_1_id_paese.text = (
                partner_invoice.cessionario_rf_IdFiscaleIVA_IdPaese or ""
            )
            # -----                     2.2.2.6.1.2 - Id Codice
            x_2_2_2_6_1_2_id_codice = etree.SubElement(
                x_2_2_2_6_1_id_fiscale_iva, etree.QName("IdCodice")
            )
            x_2_2_2_6_1_2_id_codice.text = (
                partner_invoice.cessionario_rf_IdFiscaleIVA_IdCodice or ""
            )
            # -----                 2.2.2.6.2 - Denominazione
            x_2_2_2_6_2_denominazione = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale, etree.QName("Denominazione")
            )
            x_2_2_2_6_2_denominazione.text = encode_for_export(
                partner_invoice.cessionario_rf_Denominazione or "", 80
            )
            # -----                 2.2.2.6.3 - Nome
            x_2_2_2_6_3_nome = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale, etree.QName("Nome")
            )
            x_2_2_2_6_3_nome.text = encode_for_export(
                partner_invoice.cessionario_rf_Nome or "", 60
            )
            # -----                 2.2.2.6.4 - Cognome
            x_2_2_2_6_4_cognome = etree.SubElement(
                x_2_2_2_6_rappresentante_fiscale, etree.QName("Cognome")
            )
            x_2_2_2_6_4_cognome.text = encode_for_export(
                partner_invoice.cessionario_rf_Cognome or "", 60
            )

            for invoice in partner_invoice.fatture_emesse_body_ids:
                # -----         2.2.3 - Dati Fattura Body DTE
                x_2_2_3_dati_fattura_body_dte = etree.SubElement(
                    x_2_2_cessionario_committente, etree.QName("DatiFatturaBodyDTE")
                )
                # -----             2.2.3.1 - Dati Generali
                x_2_2_3_1_dati_generali = etree.SubElement(
                    x_2_2_3_dati_fattura_body_dte, etree.QName("DatiGenerali")
                )
                # -----                 2.2.3.1.1 - Tipo Documento
                x_2_2_3_1_1_tipo_documento = etree.SubElement(
                    x_2_2_3_1_dati_generali, etree.QName("TipoDocumento")
                )
                x_2_2_3_1_1_tipo_documento.text = (
                    invoice.dati_fattura_TipoDocumento.code or ""
                )
                # -----                 2.2.3.1.2 - Data
                x_2_2_3_1_2_data = etree.SubElement(
                    x_2_2_3_1_dati_generali, etree.QName("Data")
                )
                x_2_2_3_1_2_data.text = (
                    fields.Date.to_string(invoice.dati_fattura_Data) or ""
                )
                # -----                 2.2.3.1.3 - Numero
                x_2_2_3_1_2_numero = etree.SubElement(
                    x_2_2_3_1_dati_generali, etree.QName("Numero")
                )
                x_2_2_3_1_2_numero.text = invoice.dati_fattura_Numero or ""

                for tax in invoice.dati_fattura_iva_ids:
                    # -----             2.2.3.2 - Dati Riepilogo
                    x_2_2_3_2_riepilogo = etree.SubElement(
                        x_2_2_3_dati_fattura_body_dte, etree.QName("DatiRiepilogo")
                    )
                    # -----                 2.2.3.2.1 - Imponibile Importo
                    x_2_2_3_2_1_imponibile_importo = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("ImponibileImporto")
                    )
                    x_2_2_3_2_1_imponibile_importo.text = format_decimal(
                        tax.ImponibileImporto
                    )
                    # -----                 2.2.3.2.2 - Dati IVA
                    x_2_2_3_2_2_dati_iva = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("DatiIVA")
                    )
                    # -----                     2.2.3.2.2.1 - Imposta
                    x_2_2_3_2_2_1_imposta = etree.SubElement(
                        x_2_2_3_2_2_dati_iva, etree.QName("Imposta")
                    )
                    x_2_2_3_2_2_1_imposta.text = format_decimal(tax.Imposta)
                    # -----                     2.2.3.2.2.2 - Aliquota
                    x_2_2_3_2_2_2_aliquota = etree.SubElement(
                        x_2_2_3_2_2_dati_iva, etree.QName("Aliquota")
                    )
                    x_2_2_3_2_2_2_aliquota.text = format_decimal(tax.Aliquota)
                    # -----                 2.2.3.2.3 - Natura
                    x_2_2_3_2_3_natura = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("Natura")
                    )
                    x_2_2_3_2_3_natura.text = (
                        tax.Natura_id.code if tax.Natura_id else ""
                    )
                    # -----                 2.2.3.2.4 - Detraibile
                    x_2_2_3_2_4_detraibile = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("Detraibile")
                    )
                    x_2_2_3_2_4_detraibile.text = format_decimal(tax.Detraibile)
                    # -----                 2.2.3.2.5 - Deducibile
                    x_2_2_3_2_5_deducibile = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("Deducibile")
                    )
                    x_2_2_3_2_5_deducibile.text = tax.Deducibile or ""
                    # -----                 2.2.3.2.6 - Esigibilita IVA
                    x_2_2_3_2_6_esagibilita_iva = etree.SubElement(
                        x_2_2_3_2_riepilogo, etree.QName("EsigibilitaIVA")
                    )
                    x_2_2_3_2_6_esagibilita_iva.text = tax.EsigibilitaIVA or ""

        return x_2_dte

    def _export_xml_get_dtr(self):
        # ----- 3 - DTR
        x_3_dtr = etree.Element(etree.QName("DTR"))
        # -----     2.1 - Cessionario Committente DTR
        x_3_1_cessionario_committente = etree.SubElement(
            x_3_dtr, etree.QName("CessionarioCommittenteDTR")
        )
        # -----         2.1.1 - IdentificativiFiscali
        x_3_1_1_identificativi_fiscali = etree.SubElement(
            x_3_1_cessionario_committente, etree.QName("IdentificativiFiscali")
        )
        # -----             2.1.1.1 - Id Fiscale IVA
        x_3_1_1_1_id_fiscale_iva = etree.SubElement(
            x_3_1_1_identificativi_fiscali, etree.QName("IdFiscaleIVA")
        )
        # -----                 2.1.1.1.1 - Id Paese
        x_3_1_1_1_1_id_paese = etree.SubElement(
            x_3_1_1_1_id_fiscale_iva, etree.QName("IdPaese")
        )
        x_3_1_1_1_1_id_paese.text = self.cessionario_IdFiscaleIVA_IdPaese or ""
        # -----                 2.1.1.1.2 - Id Codice
        x_3_1_1_1_2_id_codice = etree.SubElement(
            x_3_1_1_1_id_fiscale_iva, etree.QName("IdCodice")
        )
        x_3_1_1_1_2_id_codice.text = self.cessionario_IdFiscaleIVA_IdCodice or ""
        # -----             2.1.1.2 - Codice Fiscale
        x_3_1_1_2_codice_fiscale = etree.SubElement(
            x_3_1_1_identificativi_fiscali, etree.QName("CodiceFiscale")
        )
        x_3_1_1_2_codice_fiscale.text = self.cessionario_CodiceFiscale or ""
        # -----         2.1.2 - AltriDatiIdentificativi
        x_3_1_2_altri_identificativi = etree.SubElement(
            x_3_1_cessionario_committente, etree.QName("AltriDatiIdentificativi")
        )
        # -----             2.1.2.1 - Denominazione
        x_3_1_2_1_denominazione = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("Denominazione")
        )
        x_3_1_2_1_denominazione.text = self.cessionario_Denominazione or ""
        # -----             2.1.2.2 - Nome
        x_3_1_2_2_nome = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("Nome")
        )
        x_3_1_2_2_nome.text = self.cessionario_Nome or ""
        # -----             2.1.2.3 - Cognome
        x_3_1_2_3_cognome = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("Cognome")
        )
        x_3_1_2_3_cognome.text = self.cessionario_Cognome or ""
        # -----             2.1.2.4 - Sede
        x_3_1_2_4_sede = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("Sede")
        )
        # -----                 2.1.2.4.1 - Indirizzo
        x_3_1_2_4_1_indirizzo = etree.SubElement(
            x_3_1_2_4_sede, etree.QName("Indirizzo")
        )
        x_3_1_2_4_1_indirizzo.text = self.cessionario_sede_Indirizzo or ""
        # -----                 2.1.2.4.2 - Numero Civico
        x_3_1_2_4_2_numero_civico = etree.SubElement(
            x_3_1_2_4_sede, etree.QName("NumeroCivico")
        )
        x_3_1_2_4_2_numero_civico.text = self.cessionario_sede_NumeroCivico or ""
        # -----                 2.1.2.4.3 - CAP
        x_3_1_2_4_3_cap = etree.SubElement(x_3_1_2_4_sede, etree.QName("CAP"))
        x_3_1_2_4_3_cap.text = self.cessionario_sede_Cap or ""
        # -----                 2.1.2.4.4 - Comune
        x_3_1_2_4_4_comune = etree.SubElement(x_3_1_2_4_sede, etree.QName("Comune"))
        x_3_1_2_4_4_comune.text = self.cessionario_sede_Comune or ""
        # -----                 2.1.2.4.5 - Provincia
        x_3_1_2_4_5_provincia = etree.SubElement(
            x_3_1_2_4_sede, etree.QName("Provincia")
        )
        x_3_1_2_4_5_provincia.text = self.cessionario_sede_Provincia or ""
        # -----                 2.1.2.4.6 - Nazione
        x_3_1_2_4_6_nazione = etree.SubElement(x_3_1_2_4_sede, etree.QName("Nazione"))
        x_3_1_2_4_6_nazione.text = self.cessionario_sede_Nazione or ""
        # -----             2.1.2.5 - Stabile Organizzazione
        x_3_1_2_5_stabile_organizzazione = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("StabileOrganizzazione")
        )
        # -----                 2.1.2.5.1 - Indirizzo
        x_3_1_2_5_1_indirizzo = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("Indirizzo")
        )
        x_3_1_2_5_1_indirizzo.text = self.cessionario_so_Indirizzo or ""
        # -----                 2.1.2.5.2 - Numero Civico
        x_3_1_2_5_2_numero_civico = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("Numerocivico")
        )
        x_3_1_2_5_2_numero_civico.text = self.cessionario_so_NumeroCivico or ""
        # -----                 2.1.2.5.3 - CAP
        x_3_1_2_5_3_cap = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("CAP")
        )
        x_3_1_2_5_3_cap.text = self.cessionario_so_Cap or ""
        # -----                 2.1.2.5.4 - Comune
        x_3_1_2_5_4_comune = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("Comune")
        )
        x_3_1_2_5_4_comune.text = self.cessionario_so_Comune or ""
        # -----                 2.1.2.5.5 - Provincia
        x_3_1_2_5_5_provincia = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("Provincia")
        )
        x_3_1_2_5_5_provincia.text = self.cessionario_so_Provincia or ""
        # -----                 2.1.2.5.6 - Nazione
        x_3_1_2_5_6_nazione = etree.SubElement(
            x_3_1_2_5_stabile_organizzazione, etree.QName("Nazione")
        )
        x_3_1_2_5_6_nazione.text = self.cessionario_so_Nazione or ""
        # -----             2.1.2.6 - Rappresentante Fiscale
        x_3_1_2_6_rappresentante_fiscale = etree.SubElement(
            x_3_1_2_altri_identificativi, etree.QName("RappresentanteFiscale")
        )
        # -----                 2.1.2.6.1 - Id Fiscale IVA
        x_3_1_2_6_1_id_fiscale_iva = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale, etree.QName("IdFiscaleIVA")
        )
        # -----                     2.1.2.6.1.1 - Id Paese
        x_3_1_2_6_1_1_id_paese = etree.SubElement(
            x_3_1_2_6_1_id_fiscale_iva, etree.QName("IdPaese")
        )
        x_3_1_2_6_1_1_id_paese.text = self.cessionario_rf_IdFiscaleIVA_IdPaese or ""
        # -----                     2.1.2.6.1.2 - Id Codice
        x_3_1_2_6_1_2_id_codice = etree.SubElement(
            x_3_1_2_6_1_id_fiscale_iva, etree.QName("IdCodice")
        )
        x_3_1_2_6_1_2_id_codice.text = self.cessionario_rf_IdFiscaleIVA_IdCodice or ""
        # -----                 2.1.2.6.2 - Denominazione
        x_3_1_2_6_2_denominazione = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale, etree.QName("Denominazione")
        )
        x_3_1_2_6_2_denominazione.text = self.cessionario_rf_Denominazione or ""
        # -----                 2.1.2.6.3 - Nome
        x_3_1_2_6_3_nome = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale, etree.QName("Nome")
        )
        x_3_1_2_6_3_nome.text = self.cessionario_rf_Nome or ""
        # -----                 2.1.2.6.4 - Cognome
        x_3_1_2_6_4_cognome = etree.SubElement(
            x_3_1_2_6_rappresentante_fiscale, etree.QName("Cognome")
        )
        x_3_1_2_6_4_cognome.text = self.cessionario_rf_Cognome or ""

        for partner_invoice in self.fatture_ricevute_ids:
            # -----     2.2 - Cessionario Committente DTE
            x_3_2_cedente_prestatore = etree.SubElement(
                x_3_dtr, etree.QName("CedentePrestatoreDTR")
            )
            # -----         2.2.1 - IdentificativiFiscali
            x_3_2_1_identificativi_fiscali = etree.SubElement(
                x_3_2_cedente_prestatore, etree.QName("IdentificativiFiscali")
            )
            if (
                partner_invoice.cedente_IdFiscaleIVA_IdPaese
                and partner_invoice.cedente_IdFiscaleIVA_IdCodice
            ):
                # -----             2.2.1.1 - Id Fiscale IVA
                x_3_2_1_1_id_fiscale_iva = etree.SubElement(
                    x_3_2_1_identificativi_fiscali, etree.QName("IdFiscaleIVA")
                )
                # -----                 2.2.1.1.1 - Id Paese
                x_3_2_1_1_1_id_paese = etree.SubElement(
                    x_3_2_1_1_id_fiscale_iva, etree.QName("IdPaese")
                )
                x_3_2_1_1_1_id_paese.text = (
                    partner_invoice.cedente_IdFiscaleIVA_IdPaese or ""
                )
                # -----                 2.2.1.1.2 - Id Codice
                x_3_2_1_1_2_id_codice = etree.SubElement(
                    x_3_2_1_1_id_fiscale_iva, etree.QName("IdCodice")
                )
                x_3_2_1_1_2_id_codice.text = (
                    partner_invoice.cedente_IdFiscaleIVA_IdCodice or ""
                )
            # -----             2.2.1.2 - Codice Fiscale
            x_3_2_1_2_codice_fiscale = etree.SubElement(
                x_3_2_1_identificativi_fiscali, etree.QName("CodiceFiscale")
            )
            x_3_2_1_2_codice_fiscale.text = partner_invoice.cedente_CodiceFiscale or ""
            # -----         2.2.2 - AltriDatiIdentificativi
            x_3_2_2_altri_identificativi = etree.SubElement(
                x_3_2_cedente_prestatore, etree.QName("AltriDatiIdentificativi")
            )
            # -----             2.2.2.1 - Denominazione
            x_3_2_2_1_altri_identificativi_denominazione = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("Denominazione")
            )
            x_3_2_2_1_altri_identificativi_denominazione.text = encode_for_export(
                partner_invoice.cedente_Denominazione or "", 80
            )
            # -----             2.2.2.2 - Nome
            x_3_2_2_2_nome = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("Nome")
            )
            x_3_2_2_2_nome.text = encode_for_export(
                partner_invoice.cedente_Nome or "", 60
            )
            # -----             2.2.2.3 - Cognome
            x_3_2_2_3_cognome = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("Cognome")
            )
            x_3_2_2_3_cognome.text = encode_for_export(
                partner_invoice.cedente_Cognome or "", 60
            )
            # -----             2.2.2.4 - Sede
            x_3_2_2_4_sede = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("Sede")
            )
            # -----                 2.2.2.4.1 - Indirizzo
            x_3_2_2_4_1_indirizzo = etree.SubElement(
                x_3_2_2_4_sede, etree.QName("Indirizzo")
            )
            x_3_2_2_4_1_indirizzo.text = encode_for_export(
                partner_invoice.cedente_sede_Indirizzo or "", 60
            )
            # -----                 2.2.2.4.2 - Numero Civico
            x_3_2_2_4_2_numero_civico = etree.SubElement(
                x_3_2_2_4_sede, etree.QName("NumeroCivico")
            )
            x_3_2_2_4_2_numero_civico.text = encode_for_export(
                partner_invoice.cedente_sede_NumeroCivico or "", 8, encoding="ascii"
            )
            # -----                 2.2.2.4.3 - CAP
            x_3_2_2_4_3_cap = etree.SubElement(x_3_2_2_4_sede, etree.QName("CAP"))
            x_3_2_2_4_3_cap.text = encode_for_export(
                partner_invoice.cedente_sede_Cap or "", 5, encoding="ascii"
            )
            # -----                 2.2.2.4.4 - Comune
            x_3_2_2_4_4_comune = etree.SubElement(x_3_2_2_4_sede, etree.QName("Comune"))
            x_3_2_2_4_4_comune.text = encode_for_export(
                partner_invoice.cedente_sede_Comune or "", 60
            )
            # -----                 2.2.2.4.5 - Provincia
            x_3_2_2_4_5_provincia = etree.SubElement(
                x_3_2_2_4_sede, etree.QName("Provincia")
            )
            x_3_2_2_4_5_provincia.text = partner_invoice.cedente_sede_Provincia or ""
            # -----                 2.2.2.4.6 - Nazione
            x_3_2_2_4_6_nazione = etree.SubElement(
                x_3_2_2_4_sede, etree.QName("Nazione")
            )
            x_3_2_2_4_6_nazione.text = partner_invoice.cedente_sede_Nazione or ""
            # -----             2.2.2.5 - Stabile Organizzazione
            x_3_2_2_5_stabile_organizzazione = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("StabileOrganizzazione")
            )
            # -----                 2.2.2.5.1 - Indirizzo
            x_3_2_2_5_1_indirizzo = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("Indirizzo")
            )
            x_3_2_2_5_1_indirizzo.text = encode_for_export(
                partner_invoice.cedente_so_Indirizzo or "", 60
            )
            # -----                 2.2.2.5.2 - Numero Civico
            x_3_2_2_5_2_numero_civico = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("NumeroCivico")
            )
            x_3_2_2_5_2_numero_civico.text = encode_for_export(
                partner_invoice.cedente_so_NumeroCivico or "", 8, encoding="ascii"
            )
            # -----                 2.2.2.5.3 - CAP
            x_3_2_2_5_3_cap = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("CAP")
            )
            x_3_2_2_5_3_cap.text = encode_for_export(
                partner_invoice.cedente_so_Cap or "", 5, encoding="ascii"
            )
            # -----                 2.2.2.5.4 - Comune
            x_3_2_2_5_4_comune = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("Comune")
            )
            x_3_2_2_5_4_comune.text = encode_for_export(
                partner_invoice.cedente_so_Comune or "", 60
            )
            # -----                 2.2.2.5.5 - Provincia
            x_3_2_2_5_5_provincia = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("Provincia")
            )
            x_3_2_2_5_5_provincia.text = partner_invoice.cedente_so_Provincia or ""
            # -----                 2.2.2.5.6 - Nazione
            x_3_2_2_5_6_nazione = etree.SubElement(
                x_3_2_2_5_stabile_organizzazione, etree.QName("Nazione")
            )
            x_3_2_2_5_6_nazione.text = partner_invoice.cedente_so_Nazione or ""
            # -----             2.2.2.6 - Rappresentante Fiscale
            x_3_2_2_6_rappresentante_fiscale = etree.SubElement(
                x_3_2_2_altri_identificativi, etree.QName("RappresentanteFiscale")
            )
            # -----                 2.2.2.6.1 - Id Fiscale IVA
            x_3_2_2_6_1_id_fiscale_iva = etree.SubElement(
                x_3_2_2_6_rappresentante_fiscale, etree.QName("IdFiscaleIVA")
            )
            x_3_2_2_6_rappresentante_fiscale.text = (
                partner_invoice.cedente_rf_IdFiscaleIVA_IdPaese or ""
            )
            # -----                     2.2.2.6.1.1 - Id Paese
            x_3_2_2_6_1_1_id_paese = etree.SubElement(
                x_3_2_2_6_1_id_fiscale_iva, etree.QName("IdPaese")
            )
            x_3_2_2_6_1_1_id_paese.text = (
                partner_invoice.cedente_rf_IdFiscaleIVA_IdPaese or ""
            )
            # -----                     2.2.2.6.1.2 - Id Codice
            x_3_2_2_6_1_2_id_codice = etree.SubElement(
                x_3_2_2_6_1_id_fiscale_iva, etree.QName("IdCodice")
            )
            x_3_2_2_6_1_2_id_codice.text = (
                partner_invoice.cedente_rf_IdFiscaleIVA_IdCodice or ""
            )
            # -----                 2.2.2.6.2 - Denominazione
            x_3_2_2_6_2_denominazione = etree.SubElement(
                x_3_2_2_6_rappresentante_fiscale, etree.QName("Denominazione")
            )
            x_3_2_2_6_2_denominazione.text = encode_for_export(
                partner_invoice.cedente_rf_Denominazione or "", 80
            )
            # -----                 2.2.2.6.3 - Nome
            x_3_2_2_6_3_nome = etree.SubElement(
                x_3_2_2_6_rappresentante_fiscale, etree.QName("Nome")
            )
            x_3_2_2_6_3_nome.text = encode_for_export(
                partner_invoice.cedente_rf_Nome or "", 60
            )
            # -----                 2.2.2.6.4 - Cognome
            x_3_2_2_6_4_cognome = etree.SubElement(
                x_3_2_2_6_rappresentante_fiscale, etree.QName("Cognome")
            )
            x_3_2_2_6_4_cognome.text = encode_for_export(
                partner_invoice.cedente_rf_Cognome or "", 60
            )

            for invoice in partner_invoice.fatture_ricevute_body_ids:
                # -----         2.2.3 - Dati Fattura Body DTE
                x_3_2_3_dati_fattura_body_dte = etree.SubElement(
                    x_3_2_cedente_prestatore, etree.QName("DatiFatturaBodyDTR")
                )
                # -----             2.2.3.1 - Dati Generali
                x_3_2_3_1_dati_generali = etree.SubElement(
                    x_3_2_3_dati_fattura_body_dte, etree.QName("DatiGenerali")
                )
                # -----                 2.2.3.1.1 - Tipo Documento
                x_3_2_3_1_1_tipo_documento = etree.SubElement(
                    x_3_2_3_1_dati_generali, etree.QName("TipoDocumento")
                )
                x_3_2_3_1_1_tipo_documento.text = (
                    invoice.dati_fattura_TipoDocumento.code or ""
                )
                # -----                 2.2.3.1.2 - Data
                x_3_2_3_1_2_data = etree.SubElement(
                    x_3_2_3_1_dati_generali, etree.QName("Data")
                )
                x_3_2_3_1_2_data.text = (
                    fields.Date.to_string(invoice.dati_fattura_Data) or ""
                )
                # -----                 2.2.3.1.3 - Numero
                x_3_2_3_1_3_numero = etree.SubElement(
                    x_3_2_3_1_dati_generali, etree.QName("Numero")
                )
                x_3_2_3_1_3_numero.text = invoice.dati_fattura_Numero or ""
                # -----                 2.2.3.1.4 - Data Registrazione
                x_3_2_3_1_4_data_registrazione = etree.SubElement(
                    x_3_2_3_1_dati_generali, etree.QName("DataRegistrazione")
                )
                x_3_2_3_1_4_data_registrazione.text = (
                    fields.Date.to_string(invoice.dati_fattura_DataRegistrazione) or ""
                )
                for tax in invoice.dati_fattura_iva_ids:
                    # -----             2.2.3.2 - Dati Riepilogo
                    x_3_2_3_2_riepilogo = etree.SubElement(
                        x_3_2_3_dati_fattura_body_dte, etree.QName("DatiRiepilogo")
                    )
                    # -----                 2.2.3.2.1 - Imponibile Importo
                    x_3_2_3_2_1_imponibile_importo = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("ImponibileImporto")
                    )
                    x_3_2_3_2_1_imponibile_importo.text = format_decimal(
                        tax.ImponibileImporto
                    )
                    # -----                 2.2.3.2.2 - Dati IVA
                    x_3_2_3_2_2_dati_iva = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("DatiIVA")
                    )
                    # -----                     2.2.3.2.2.1 - Imposta
                    x_3_2_3_2_2_1_imposta = etree.SubElement(
                        x_3_2_3_2_2_dati_iva, etree.QName("Imposta")
                    )
                    x_3_2_3_2_2_1_imposta.text = format_decimal(tax.Imposta)
                    # -----                     2.2.3.2.2.2 - Aliquota
                    x_3_2_3_2_2_2_aliquota = etree.SubElement(
                        x_3_2_3_2_2_dati_iva, etree.QName("Aliquota")
                    )
                    x_3_2_3_2_2_2_aliquota.text = format_decimal(tax.Aliquota)
                    # -----                 2.2.3.2.3 - Natura
                    x_3_2_3_2_3_natura = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("Natura")
                    )
                    x_3_2_3_2_3_natura.text = (
                        tax.Natura_id.code if tax.Natura_id else ""
                    )
                    # -----                 2.2.3.2.4 - Detraibile
                    x_3_2_3_2_4_detraibile = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("Detraibile")
                    )
                    x_3_2_3_2_4_detraibile.text = format_decimal(tax.Detraibile)
                    # -----                 2.2.3.2.5 - Deducibile
                    x_3_2_3_2_5_deducibile = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("Deducibile")
                    )
                    x_3_2_3_2_5_deducibile.text = tax.Deducibile or ""
                    # -----                 2.2.3.2.6 - Esigibilita IVA
                    x_3_2_3_2_6_esagibilita_iva = etree.SubElement(
                        x_3_2_3_2_riepilogo, etree.QName("EsigibilitaIVA")
                    )
                    x_3_2_3_2_6_esagibilita_iva.text = tax.EsigibilitaIVA or ""

        return x_3_dtr

    def _export_xml_get_ann(self):
        # ----- 4 - ANN
        x_4_ann = etree.Element(etree.QName("ANN"))
        # ----- 4.1 - Id File
        x_4_1_id_file = etree.SubElement(x_4_ann, etree.QName("IdFile"))
        x_4_1_id_file.text = self.id_comunicazione
        # ----- 4.2 - Posizione

        # If this node is empty, cancel all invoices of previous comunication
        # x_4_2_posizione = etree.SubElement(
        #     x_4_ann,
        #     etree.QName("Posizione"))
        return x_4_ann

    def get_export_xml_filename(self):
        self.ensure_one()
        filename = "{id}_{type}_{ann}{number}.{ext}".format(
            id=self.company_id.vat or "",
            type="DF",
            ann="A" if self.dati_trasmissione == "ANN" else "0",
            number=str(self.identificativo or 0).rjust(4, "0"),
            ext="xml",
        )
        return filename

    def get_export_xml(self):
        self.ensure_one()
        self._validate()
        # ----- 0 - Dati Fattura
        x_0_dati_fattura = self._export_xml_get_dati_fattura()
        # ----- 1 - Dati Fattura header
        if self.dati_trasmissione in ("DTE", "DTR"):
            x_1_dati_fattura_header = self._export_xml_get_dati_fattura_header()
            x_0_dati_fattura.append(x_1_dati_fattura_header)
        # ----- 2 - DTE
        if self.dati_trasmissione == "DTE":
            x_2_dte = self._export_xml_get_dte()
            x_0_dati_fattura.append(x_2_dte)
        # ----- 3 - DTR
        elif self.dati_trasmissione == "DTR":
            x_3_dtr = self._export_xml_get_dtr()
            x_0_dati_fattura.append(x_3_dtr)
        # ----- 4 - ANN
        elif self.dati_trasmissione == "ANN":
            x_4_ann = self._export_xml_get_ann()
            x_0_dati_fattura.append(x_4_ann)
        # ----- Remove empty nodes
        clear_xml(x_0_dati_fattura)
        # ----- Create XML
        xml_string = etree.tostring(
            x_0_dati_fattura, encoding="latin1", method="xml", pretty_print=True
        )
        return xml_string


class ComunicazioneDatiIvaFattureEmesse(models.Model):
    _name = "comunicazione.dati.iva.fatture.emesse"
    _description = "Invoices data communication - Customer invoices"

    comunicazione_id = fields.Many2one(
        "comunicazione.dati.iva",
        string="Communication",
        readonly=True,
        ondelete="cascade",
    )
    # Cedente
    partner_id = fields.Many2one("res.partner", string="Partner")
    cessionario_IdFiscaleIVA_IdPaese = fields.Char(
        string="Country ID",
        size=2,
        help="Country code, expressed using the 3166-1 alpha-2 standard",
    )
    cessionario_IdFiscaleIVA_IdCodice = fields.Char(string="Fiscal identifier", size=28)
    cessionario_CodiceFiscale = fields.Char(size=16)
    cessionario_Denominazione = fields.Char(size=80)
    cessionario_Nome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.3 <Cognome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cessionario_Cognome = fields.Char(
        size=60,
        help="To fill along with 2.1.2.2 <Nome> and alternatively to "
        "2.1.2.1 <Denominazione>",
    )
    cessionario_sede_Indirizzo = fields.Char(size=60)
    cessionario_sede_NumeroCivico = fields.Char(size=8)
    cessionario_sede_Cap = fields.Char(size=5)
    cessionario_sede_Comune = fields.Char(size=60)
    cessionario_sede_Provincia = fields.Char(size=2)
    cessionario_sede_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cessionario_so_Indirizzo = fields.Char(size=60)
    cessionario_so_NumeroCivico = fields.Char(size=8)
    cessionario_so_Cap = fields.Char(size=5)
    cessionario_so_Comune = fields.Char(size=60)
    cessionario_so_Provincia = fields.Char(size=2)
    cessionario_so_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cessionario_rf_IdFiscaleIVA_IdPaese = fields.Char(
        size=2, help="Only IT is accepted"
    )
    cessionario_rf_IdFiscaleIVA_IdCodice = fields.Char(size=11)
    cessionario_rf_Denominazione = fields.Char(size=80)
    cessionario_rf_Nome = fields.Char(size=60)
    cessionario_rf_Cognome = fields.Char(size=60)
    # Dati Cessionario e Fattura
    fatture_emesse_body_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.emesse.body",
        "fattura_emessa_id",
        string="Customer invoices body",
    )

    # Rettifica
    rettifica_IdFile = fields.Char(
        string="File identifier",
        help="Identifier of file to be amended. This identifer is "
        "communicated by the system after transmission",
    )
    rettifica_Posizione = fields.Integer(
        string="Position", help="Invoice position within transmitted file"
    )
    # totali
    totale_imponibile = fields.Float(
        "Total untaxed amount", compute="_compute_total", store=True
    )
    totale_iva = fields.Float("Total VAT", compute="_compute_total", store=True)

    @api.depends(
        "fatture_emesse_body_ids.totale_imponibile",
        "fatture_emesse_body_ids.totale_iva",
    )
    def _compute_total(self):
        for line in self:
            totale_imponibile = 0
            totale_iva = 0
            for fattura in line.fatture_emesse_body_ids:
                totale_imponibile += fattura.totale_imponibile
                totale_iva += fattura.totale_iva
            line.totale_imponibile = totale_imponibile
            line.totale_iva = totale_iva

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        for fattura in self:
            if fattura.partner_id:
                vals = fattura.comunicazione_id._prepare_cessionario_partner_id(
                    fattura.partner_id
                )
                fattura.cessionario_IdFiscaleIVA_IdPaese = vals[
                    "cessionario_IdFiscaleIVA_IdPaese"
                ]
                fattura.cessionario_IdFiscaleIVA_IdCodice = vals[
                    "cessionario_IdFiscaleIVA_IdCodice"
                ]
                fattura.cessionario_CodiceFiscale = vals["cessionario_CodiceFiscale"]
                fattura.cessionario_Denominazione = vals["cessionario_Denominazione"]
                # Sede
                fattura.cessionario_sede_Indirizzo = vals["cessionario_sede_Indirizzo"]
                fattura.cessionario_sede_Cap = vals["cessionario_sede_Cap"]
                fattura.cessionario_sede_Comune = vals["cessionario_sede_Comune"]
                fattura.cessionario_sede_Provincia = vals["cessionario_sede_Provincia"]
                fattura.cessionario_sede_Nazione = vals["cessionario_sede_Nazione"]


class ComunicazioneDatiIvaFattureEmesseBody(models.Model):
    _name = "comunicazione.dati.iva.fatture.emesse.body"
    _description = "Invoices data communication - Customer invoices body"

    @api.depends(
        "dati_fattura_iva_ids.ImponibileImporto", "dati_fattura_iva_ids.Imposta"
    )
    def _compute_total(self):
        for ft in self:
            totale_imponibile = 0
            totale_iva = 0
            for tax_line in ft.dati_fattura_iva_ids:
                totale_imponibile += tax_line.ImponibileImporto
                totale_iva += tax_line.Imposta
            ft.totale_imponibile = totale_imponibile
            ft.totale_iva = totale_iva

    fattura_emessa_id = fields.Many2one(
        "comunicazione.dati.iva.fatture.emesse",
        string="Customer invoice",
        ondelete="cascade",
    )
    posizione = fields.Integer(
        "Position", help="Invoice position within transmitted file", required=True
    )
    invoice_id = fields.Many2one("account.move", string="Invoice")
    dati_fattura_TipoDocumento = fields.Many2one(
        "fiscal.document.type", string="Document type", required=True
    )
    dati_fattura_Data = fields.Date(string="Document date", required=True)
    dati_fattura_Numero = fields.Char(string="Document number", required=True)
    dati_fattura_iva_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.emesse.iva",
        "fattura_emessa_body_id",
        string="VAT summary",
    )
    totale_imponibile = fields.Float(
        "Total untaxed amount", compute="_compute_total", store=True
    )
    totale_iva = fields.Float("Total VAT", compute="_compute_total", store=True)

    @api.onchange("invoice_id")
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = (
                    fattura.invoice_id.fiscal_document_type_id
                    and fattura.invoice_id.fiscal_document_type_id.id
                    or False
                )
                fattura.dati_fattura_Numero = fattura.invoice_id.name
                fattura.dati_fattura_Data = fattura.invoice_id.invoice_date
                fattura.dati_fattura_iva_ids = (
                    fattura.invoice_id._get_tax_comunicazione_dati_iva()
                )


class ComunicazioneDatiIvaFattureEmesseIva(models.Model):
    _name = "comunicazione.dati.iva.fatture.emesse.iva"
    _description = "Invoices data communication - Customer invoices VAT"

    fattura_emessa_body_id = fields.Many2one(
        "comunicazione.dati.iva.fatture.emesse.body",
        string="Customer invoice body",
        readonly=True,
        ondelete="cascade",
    )
    ImponibileImporto = fields.Float(
        string="Base amount",
        help="Base amount (for operations VAT subjected) or not taxable amount"
        " (for operations where seller does not indicate VAT) or sum of "
        "taxable and tax amounts, when expected, like for simplified "
        "invoices (TD07 or TD08)",
    )
    Imposta = fields.Float(
        string="VAT",
        help="If element 2.2.3.1.1 is TD07 or TD08, this can be used instead "
        "of 2.2.3.2.2.2 <Aliquota>",
    )
    Aliquota = fields.Float(string="Tax rate", help="VAT rate, in percentage")
    Natura_id = fields.Many2one("account.tax.kind", string="Exemption kind")
    Detraibile = fields.Float(string="Deductible %")
    Deducibile = fields.Char(
        string="Deductible", size=2, help="Possible value: [SI] = deductible expense"
    )
    EsigibilitaIVA = fields.Selection(
        [("I", "Immediate"), ("D", "Deferred"), ("S", "Split payment")],
        string="VAT payability",
    )


class ComunicazioneDatiIvaFattureRicevute(models.Model):
    _name = "comunicazione.dati.iva.fatture.ricevute"
    _description = "Invoices data communication - Supplier bills"

    comunicazione_id = fields.Many2one(
        "comunicazione.dati.iva",
        string="Communication",
        readonly=True,
        ondelete="cascade",
    )
    # Cessionario
    partner_id = fields.Many2one("res.partner", string="Partner")
    cedente_IdFiscaleIVA_IdPaese = fields.Char(
        string="Country ID",
        size=2,
        help="Country code, expressed using the 3166-1 alpha-2 standard",
    )
    cedente_IdFiscaleIVA_IdCodice = fields.Char(string="Fiscal identifier", size=28)
    cedente_CodiceFiscale = fields.Char(size=16)
    cedente_Denominazione = fields.Char(size=80)
    cedente_Nome = fields.Char(
        size=60,
        help="To fill along with 3.2.2.3 <Cognome> and alternatively to "
        "3.2.2.1 <Denominazione>",
    )
    cedente_Cognome = fields.Char(
        size=60,
        help="To fill along with 3.2.2.2 <Nome> and alternatively to "
        "3.2.2.1 <Denominazione>",
    )
    cedente_sede_Indirizzo = fields.Char(size=60)
    cedente_sede_NumeroCivico = fields.Char(size=8)
    cedente_sede_Cap = fields.Char(size=5)
    cedente_sede_Comune = fields.Char(size=60)
    cedente_sede_Provincia = fields.Char(size=2)
    cedente_sede_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cedente_so_Indirizzo = fields.Char(size=60)
    cedente_so_NumeroCivico = fields.Char(size=8)
    cedente_so_Cap = fields.Char(size=5)
    cedente_so_Comune = fields.Char(size=60)
    cedente_so_Provincia = fields.Char(size=2)
    cedente_so_Nazione = fields.Char(
        size=2, help="Country code, expressed using the 3166-1 alpha-2 standard"
    )
    cedente_rf_IdFiscaleIVA_IdPaese = fields.Char(size=2, help="Only IT is accepted")
    cedente_rf_IdFiscaleIVA_IdCodice = fields.Char(size=11)
    cedente_rf_Denominazione = fields.Char(size=80)
    cedente_rf_Nome = fields.Char(size=60)
    cedente_rf_Cognome = fields.Char(size=60)
    # Dati Cedente e Fattura
    fatture_ricevute_body_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.ricevute.body",
        "fattura_ricevuta_id",
        string="Supplier bills body",
    )

    # Rettifica
    rettifica_IdFile = fields.Char(
        string="File identifier",
        help="Identifier of file to be amended. This identifer is "
        "communicated by the system after transmission",
    )
    rettifica_Posizione = fields.Integer(
        string="Position", help="Invoice position within transmitted file"
    )
    # totali
    totale_imponibile = fields.Float(
        "Total untaxed amount", compute="_compute_total", store=True
    )
    totale_iva = fields.Float("Total VAT", compute="_compute_total", store=True)

    @api.depends(
        "fatture_ricevute_body_ids.totale_imponibile",
        "fatture_ricevute_body_ids.totale_iva",
    )
    def _compute_total(self):
        for line in self:
            totale_imponibile = 0
            totale_iva = 0
            for fattura in line.fatture_ricevute_body_ids:
                totale_imponibile += fattura.totale_imponibile
                totale_iva += fattura.totale_iva
            line.totale_imponibile = totale_imponibile
            line.totale_iva = totale_iva

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        for fattura in self:
            if fattura.partner_id:
                fattura.cedente_IdFiscaleIVA_IdPaese = (
                    fattura.partner_id.country_id.code or ""
                )
                fattura.cedente_IdFiscaleIVA_IdCodice = (
                    fattura.partner_id.vat[2:] if fattura.partner_id.vat else ""
                )
                fattura.cedente_CodiceFiscale = fattura.partner_id.fiscalcode or ""
                fattura.cedente_Denominazione = fattura.partner_id.name or ""
                # Sede
                fattura.cedente_sede_Indirizzo = "{} {}".format(
                    fattura.partner_id.street, fattura.partner_id.street2
                ).strip()
                fattura.cedente_sede_Cap = fattura.partner_id.zip or ""
                fattura.cedente_sede_Comune = fattura.partner_id.city or ""
                fattura.cedente_sede_Provincia = (
                    fattura.partner_id.state_id
                    and fattura.partner_id.state_id.code
                    or ""
                )
                fattura.cedente_sede_Nazione = (
                    fattura.partner_id.country_id
                    and fattura.partner_id.country_id.code
                    or ""
                )


class ComunicazioneDatiIvaFattureRicevuteBody(models.Model):
    _name = "comunicazione.dati.iva.fatture.ricevute.body"
    _description = "Invoices data communication - Supplier bills body"

    @api.depends(
        "dati_fattura_iva_ids.ImponibileImporto", "dati_fattura_iva_ids.Imposta"
    )
    def _compute_total(self):
        for ft in self:
            totale_imponibile = 0
            totale_iva = 0

            for tax_line in ft.dati_fattura_iva_ids:
                if (
                    ft.dati_fattura_TipoDocumento.out_refund
                    or ft.dati_fattura_TipoDocumento.in_refund
                ):
                    totale_imponibile -= tax_line.ImponibileImporto
                    totale_iva -= tax_line.Imposta
                else:
                    totale_imponibile += tax_line.ImponibileImporto
                    totale_iva += tax_line.Imposta

            ft.totale_imponibile = totale_imponibile
            ft.totale_iva = totale_iva

    fattura_ricevuta_id = fields.Many2one(
        "comunicazione.dati.iva.fatture.ricevute",
        string="Supplier bill",
        ondelete="cascade",
    )
    posizione = fields.Integer(
        "Position", help="Invoice position within transmitted file", required=True
    )
    invoice_id = fields.Many2one("account.move", string="Invoice")
    dati_fattura_TipoDocumento = fields.Many2one(
        "fiscal.document.type", string="Document type", required=True
    )
    dati_fattura_Data = fields.Date(string="Document date", required=True)
    dati_fattura_Numero = fields.Char(string="Document number", required=True)
    dati_fattura_DataRegistrazione = fields.Date(
        string="Registration date", required=True
    )
    dati_fattura_iva_ids = fields.One2many(
        "comunicazione.dati.iva.fatture.ricevute.iva",
        "fattura_ricevuta_body_id",
        string="VAT summary",
    )
    totale_imponibile = fields.Float(
        "Total untaxed amount", compute="_compute_total", store=True
    )
    totale_iva = fields.Float("Total VAT", compute="_compute_total", store=True)

    @api.onchange("invoice_id")
    def onchange_invoice_id(self):
        for fattura in self:
            if fattura.invoice_id:
                fattura.dati_fattura_TipoDocumento = (
                    fattura.invoice_id.fiscal_document_type_id
                    and fattura.invoice_id.fiscal_document_type_id.id
                    or False
                )
                fattura.dati_fattura_Numero = fattura.invoice_id.name
                fattura.dati_fattura_Data = fattura.invoice_id.invoice_date
                fattura.dati_fattura_DataRegistrazione = fattura.invoice_id.date
                # tax
                tax_lines = []
                for tax_line in fattura.invoice_id.tax_line_ids:
                    # aliquota
                    aliquota = 0
                    tax = tax_line.tax_id
                    if tax:
                        aliquota = tax.amount
                    val = {
                        "ImponibileImporto": tax_line.base,
                        "Imposta": tax_line.amount,
                        "Aliquota": aliquota,
                    }
                    tax_lines.append((0, 0, val))
                fattura.dati_fattura_iva_ids = tax_lines


class ComunicazioneDatiIvaFattureRicevuteIva(models.Model):
    _name = "comunicazione.dati.iva.fatture.ricevute.iva"
    _description = "Invoices data communication - Supplier bills VAT"

    fattura_ricevuta_body_id = fields.Many2one(
        "comunicazione.dati.iva.fatture.ricevute.body",
        string="Supplier bill body",
        readonly=True,
        ondelete="cascade",
    )
    ImponibileImporto = fields.Float(
        string="Base amount",
        help="Base amount (for operations VAT subjected) or not taxable amount"
        " (for operations where seller does not indicate VAT) or sum of "
        "taxable and tax amounts, when expected, like for simplified "
        "invoices (TD07 or TD08)",
    )
    Imposta = fields.Float(
        string="VAT",
        help="If element 2.2.3.1.1 is TD07 or TD08, this can be used instead "
        "of 2.2.3.2.2.2 <Aliquota>",
    )
    Aliquota = fields.Float(string="Tax rate", help="VAT rate, in percentage")
    Natura_id = fields.Many2one("account.tax.kind", string="Exemption kind")
    Detraibile = fields.Float(string="Deductible %")
    Deducibile = fields.Char(
        string="Deductible", size=2, help="Possible value: [SI] = deductible expense"
    )
    EsigibilitaIVA = fields.Selection(
        [("I", "Immediate"), ("D", "Deferred"), ("S", "Split payment")],
        string="VAT payability",
    )
