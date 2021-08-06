# Copyright 2020 Giuseppe Borruso
# Copyright 2020 Marco Colombo
import logging
import os
from datetime import datetime

import xmlschema
from lxml import etree
from unidecode import unidecode

from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
from odoo.tools import float_repr

from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export

_logger = logging.getLogger(__name__)

# XXX da vedere se spostare in fatturapa e fare una import del validator, es.
# from from odoo.addons.l10n_it_fatturapa import FPAValidator


# fix <xs:import namespace="http://www.w3.org/2000/09/xmldsig#"
#      schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd" /> # noqa: B950
class FPAValidator:

    _XSD_SCHEMA = "Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd"
    _xml_schema_1_2_1 = get_module_resource(
        "l10n_it_fatturapa", "data", "xsd", _XSD_SCHEMA
    )
    _old_xsd_specs = get_module_resource(
        "l10n_it_fatturapa", "data", "xsd", "xmldsig-core-schema.xsd"
    )

    def __init__(self):
        self.error_log = []
        locations = {"http://www.w3.org/2000/09/xmldsig#": self._old_xsd_specs}
        self._validator = xmlschema.XMLSchema(
            self._xml_schema_1_2_1,
            locations=locations,
            validation="lax",
            allow="local",
            loglevel=20,
        )

    def __call__(self, *args, **kwargs):
        self.error_log = list(self._validator.iter_errors(*args, **kwargs))
        return not self.error_log


DEFAULT_INVOICE_ITALIAN_DATE_FORMAT = "%Y-%m-%d"


class EFatturaOut:

    _validator = FPAValidator()

    def validate(self, tree):
        ret = self._validator(tree)
        errors = self._validator.error_log
        return (ret, errors)

    def get_template_values(self):  # noqa: C901
        """Prepare values and helper functions for the template"""

        env = self.env

        def format_date(dt):
            # Format the date in the italian standard.
            dt = dt or datetime.now()
            return dt.strftime(DEFAULT_INVOICE_ITALIAN_DATE_FORMAT)

        def format_monetary(number, currency):
            # Format the monetary values to avoid trailing decimals
            # (e.g. 90.85000000000001).
            return float_repr(number, min(2, currency.decimal_places))

        def format_numbers(number):
            # format number to str with between 2 and 8 decimals (event if it's .00)
            number_splited = str(number).split(".")
            if len(number_splited) == 1:
                return "%.02f" % number

            cents = number_splited[1]
            if len(cents) > 8:
                return "%.08f" % number
            return float_repr(number, max(2, len(cents)))

        def format_numbers_two(number):
            # format number to str with 2 (event if it's .00)
            return "%.02f" % number

        def format_phone(number):
            if not number:
                return False
            number = number.replace(" ", "").replace("/", "").replace(".", "")
            if len(number) > 4 and len(number) < 13:
                return number
            return False

        def format_price(line):
            res = line.price_unit
            if line.tax_ids and line.tax_ids[0].price_include:
                res = line.price_unit / (1 + (line.tax_ids[0].amount / 100))
            price_precision = env["decimal.precision"].precision_get(
                "Product Price for XML e-invoices"
            )
            if price_precision < 2:
                price_precision = 2

            # lo SdI non accetta quantità negative, quindi invertiamo price_unit
            # e quantity (vd. format_quantity)
            if line.quantity < 0:
                res = -res

            # XXX arrotondamento?
            res = "{prezzo:.{precision}f}".format(prezzo=res, precision=price_precision)
            return res

        def format_quantity(line):
            uom_precision = env["decimal.precision"].precision_get(
                "Product Unit of Measure"
            )
            if uom_precision < 2:
                uom_precision = 2

            if not line.quantity or line.display_type in ("line_section", "line_note"):
                quantity = 0
            else:
                quantity = line.quantity

            # lo SdI non accetta quantità negative, quindi invertiamo price_unit
            # e quantity (vd. format_price)
            if line.quantity < 0:
                quantity = -quantity

            # XXX arrotondamento?
            res = ("{qta:.{precision}f}".format(qta=quantity, precision=uom_precision),)
            return res[0]

        def get_vat_number(vat):
            # return vat[2:].replace(' ', '') if vat else ""
            return vat[2:] if vat else ""

        def get_vat_country(vat):
            return vat[:2].upper() if vat else ""

        def get_causale(invoice):
            res = []
            if invoice.narration:
                # max length of Causale is 200
                caus_list = invoice.narration.split("\n")
                for causale in caus_list:
                    if not causale:
                        continue
                    causale_list_200 = [
                        causale[i : i + 200] for i in range(0, len(causale), 200)
                    ]
                    for causale200 in causale_list_200:
                        # Remove non latin chars, but go back to unicode string,
                        # as expected by String200LatinType
                        causale = encode_for_export(causale200, 200)
                        res.append(causale)
            return res

        def get_nome_attachment(doc_id):
            file_name, file_extension = os.path.splitext(doc_id.name)
            attachment_name = (
                doc_id.name
                if len(doc_id.name) <= 60
                else "".join([file_name[: (60 - len(file_extension))], file_extension])
            )
            return encode_for_export(attachment_name, 60)

        def get_type_attachment(doc_id):
            mini_map = {
                "application/pdf": "PDF",
                "image/png": "PNG",
            }
            attachment_type = mini_map.get(doc_id.mimetype, False)
            return encode_for_export(attachment_type, 10) if attachment_type else False

        def in_eu(partner):
            europe = env.ref("base.europe", raise_if_not_found=False)
            country = partner.country_id
            if not europe or not country or country in europe.country_ids:
                return True
            return False

        def get_all_taxes(record):
            """Generate summary data for taxes.
            Odoo does that for us, but only for nonzero taxes.
            SdI expects a summary for every tax mentioned in the invoice,
            even those with price_total == 0.
            """
            out_computed = {}
            # existing tax lines
            tax_ids = record.line_ids.filtered(lambda line: line.tax_line_id)
            for tax_id in tax_ids:
                tax_line_id = tax_id.tax_line_id
                aliquota = format_numbers(tax_line_id.amount)
                key = "{}_{}".format(aliquota, tax_line_id.kind_id.code)
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
            for line in record.invoice_line_ids:
                if line.display_type in ("line_section", "line_note"):
                    # notes and sections
                    # we ignore line.tax_ids altogether,
                    # (it is popolated with a default tax usually)
                    # and use another tax in the template
                    continue
                for tax_id in line.tax_ids:
                    aliquota = format_numbers(tax_id.amount)
                    key = "{}_{}".format(aliquota, tax_id.kind_id.code)
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

        def get_importo(line):
            str_number = str(line.discount)
            number = str_number[::-1].find(".")
            if number <= 2:
                return False
            return line.price_unit * line.discount / 100

        if self.partner_id.commercial_partner_id.is_pa:
            # check value code
            code = self.partner_id.ipa_code
        else:
            code = self.partner_id.codice_destinatario

        # Create file content.
        template_values = {
            "formato_trasmissione": "FPA12" if self.partner_id.is_pa else "FPR12",
            "company_id": self.company_id,
            "partner_id": self.partner_id,
            "invoices": self.invoices,
            "progressivo_invio": self.progressivo_invio,
            "encode_for_export": encode_for_export,
            "format_date": format_date,
            "format_monetary": format_monetary,
            "format_numbers": format_numbers,
            "format_numbers_two": format_numbers_two,
            "format_phone": format_phone,
            "format_quantity": format_quantity,
            "format_price": format_price,
            "get_vat_number": get_vat_number,
            "get_vat_country": get_vat_country,
            "get_causale": get_causale,
            "get_nome_attachment": get_nome_attachment,
            "get_type_attachment": get_type_attachment,
            "codice_destinatario": code.upper(),
            "in_eu": in_eu,
            "unidecode": unidecode,
            "wizard": self.wizard,
            "get_importo": get_importo,
            "all_taxes": {
                invoice.id: get_all_taxes(invoice) for invoice in self.invoices
            },
        }
        return template_values

    def to_xml(self, env):
        """Create the xml file content.
        :return: The XML content as str.
        """

        self.env = env

        template_values = self.get_template_values()
        content = env.ref(
            "l10n_it_fatturapa_out.account_invoice_it_FatturaPA_export"
        )._render(template_values)
        # 14.0 - occorre rimuovere gli spazi tra i tag
        root = etree.fromstring(content, parser=etree.XMLParser(remove_blank_text=True))
        # già che ci siamo, validiamo con l'XMLSchema dello SdI
        ok, errors = self.validate(root)
        if not ok:
            # XXX - da migliorare?
            # i controlli precedenti dovrebbero escludere errori di sintassi XML
            # with open("/tmp/fatturaout.xml", "wb") as o:
            #    o.write(etree.tostring(root, xml_declaration=True, encoding="utf-8"))
            raise UserError("\n".join(str(e) for e in errors))
        content = etree.tostring(root, xml_declaration=True, encoding="utf-8")
        return content

    def __init__(self, wizard, partner_id, invoices, progressivo_invio):
        self.wizard = wizard
        self.company_id = wizard.env.company
        self.partner_id = partner_id
        self.invoices = invoices
        self.progressivo_invio = progressivo_invio
