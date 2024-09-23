# Copyright 2020 Giuseppe Borruso
# Copyright 2020 Marco Colombo
import logging
import os
from datetime import datetime

from lxml import etree
from unidecode import unidecode

from odoo.exceptions import UserError
from odoo.tools import float_repr
from odoo.tools.translate import _

from odoo.addons.l10n_it_account.tools.account_tools import (
    encode_for_export,
    fpa_schema,
)

_logger = logging.getLogger(__name__)

DEFAULT_INVOICE_ITALIAN_DATE_FORMAT = "%Y-%m-%d"


def format_numbers(number):
    # format number to str with between 2 and 8 decimals (event if it's .00)
    number_splited = str(number).split(".")
    if len(number_splited) == 1:
        return "%.02f" % number

    cents = number_splited[1]
    if len(cents) > 8:
        return "%.08f" % number
    return float_repr(number, max(2, len(cents)))


def fpaToEur(amount, invoice, euro, rate=None):
    currency = invoice.currency_id
    if currency == euro:
        return amount
    elif rate is not None:
        return amount * (1 / rate)
    return currency._convert(amount, euro, invoice.company_id, invoice.date, False)


class EFatturaOut:
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

        def format_price(line, sign=1, original_currency=False):
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

            # force EUR unless we want the original currency
            if not original_currency:
                res = fpa_to_eur(res, line.move_id, line.currency_rate)

            # XXX arrotondamento?
            res = "{prezzo:.{precision}f}".format(
                prezzo=sign * res, precision=price_precision
            )
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

        def get_id_fiscale_iva(partner, prefer_fiscalcode=False):
            id_paese = partner.country_id.code
            if partner.vat:
                if (id_paese == "IT" and partner.vat.startswith("IT")) or (
                    id_paese == "SM" and partner.vat.startswith("SM")
                ):
                    id_codice = partner.vat[2:]
                else:
                    id_codice = partner.vat
            elif partner.fiscalcode or id_paese == "IT":
                id_codice = False
            else:
                id_codice = "99999999999"

            if prefer_fiscalcode and partner.fiscalcode:
                id_codice = partner.fiscalcode

            return {
                "id_paese": id_paese,
                "id_codice": id_codice,
            }

        def get_causale(invoice):
            res = []
            if invoice.narration:
                # see: OCA/server-tools/html_text/models/ir_fields_converter.py
                # after server_tools/html_text is ported to 16.0 we could use:
                # narration_text = self.env["ir.fields.converter"]
                #                  .text_from_html(invoice.narration, 40, 100, "...")
                # meanwhile: 8<
                from lxml import html

                try:
                    narration_text = "\n".join(
                        text.strip()
                        for text in html.fromstring(invoice.narration).xpath("//text()")
                    )
                except Exception:
                    narration_text = ""
                # >8 end meanwhile

                # max length of Causale is 200
                caus_list = narration_text.split("\n")
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
            # wrapper to a method in wizard (for better overriding)
            wiz = self.env["wizard.export.fatturapa"]
            return wiz.getAllTaxes(record)

        def get_importo(line):
            str_number = str(line.discount)
            number = str_number[::-1].find(".")
            if number <= 2:
                return False
            return line.price_unit * line.discount / 100

        def get_importo_totale(invoice):
            # wrapper to a method in wizard (for better overriding)
            wiz = self.env["wizard.export.fatturapa"]
            return wiz.getImportoTotale(invoice)

        def get_payments(invoice):
            # wrapper to a method in wizard (for better overriding)
            wiz = self.env["wizard.export.fatturapa"]
            return wiz.getPayments(invoice)

        def fpa_to_eur(amount, invoice, rate=None):
            euro = self.env.ref("base.EUR")
            return fpaToEur(amount, invoice, euro, rate)

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
            "get_causale": get_causale,
            "get_nome_attachment": get_nome_attachment,
            "get_type_attachment": get_type_attachment,
            "get_id_fiscale_iva": get_id_fiscale_iva,
            "codice_destinatario": code.upper(),
            "in_eu": in_eu,
            "unidecode": unidecode,
            "wizard": self.wizard,
            "get_importo": get_importo,
            "get_importo_totale": get_importo_totale,
            "get_payments": get_payments,
            "all_taxes": {
                invoice.id: get_all_taxes(invoice) for invoice in self.invoices
            },
            "fpa_to_eur": fpa_to_eur,
        }

        wiz = self.env["wizard.export.fatturapa"]
        return wiz.getTemplateValues(template_values)

    def to_xml(self, env):
        """Create the xml file content.
        :return: The XML content as str.
        """

        self.env = env

        template_values = self.get_template_values()
        ir_ui_view = env.ref(
            "l10n_it_fatturapa_out.account_invoice_it_FatturaPA_export"
        )
        content = ir_ui_view._render_template(
            "l10n_it_fatturapa_out.account_invoice_it_FatturaPA_export", template_values
        )

        # 14.0 - occorre rimuovere gli spazi tra i tag
        root = etree.fromstring(content, parser=etree.XMLParser(remove_blank_text=True))
        # già che ci siamo, validiamo con l'XMLSchema dello SdI
        errors = list(fpa_schema.iter_errors(root))
        if errors:
            # XXX - da migliorare?
            # i controlli precedenti dovrebbero escludere errori di sintassi XML
            # with open("/tmp/fatturaout.xml", "wb") as o:
            #    o.write(etree.tostring(root, xml_declaration=True, encoding="utf-8"))
            # Print error paths, as they can be helpful even for non-technical people
            error_path_string = "\n- ".join(
                err.path[err.path.index(":") + 1 :] for err in errors
            )
            error_msg = _(
                "Error processing invoice(s) %(invoices)s.\n\n"
                "Errors in the following fields:\n- %(error_path_string)s\n\n",
                invoices=", ".join(
                    inv.display_name for inv in template_values["invoices"]
                ),
                error_path_string=error_path_string,
            )
            # add details in debug mode
            if env.user.user_has_groups("base.group_no_one"):
                error_msg += _("Full error follows:\n\n") + "\n".join(
                    str(e) for e in errors
                )
            else:
                error_msg += _("Activate debug mode to see the full error.")
            raise UserError(error_msg)
        content = etree.tostring(root, xml_declaration=True, encoding="utf-8")
        return content

    def _get_company_from_invoices(self, invoices):
        company = invoices.mapped("company_id")
        if len(company) > 1:
            raise UserError(
                _("Invoices %s must belong to the same company.")
                % ", ".join(invoices.mapped("name"))
            )
        return company

    def __init__(self, wizard, partner_id, invoices, progressivo_invio):
        self.wizard = wizard
        self.company_id = (
            self._get_company_from_invoices(invoices) or wizard.env.company
        )
        self.partner_id = partner_id
        self.invoices = invoices
        self.progressivo_invio = progressivo_invio
