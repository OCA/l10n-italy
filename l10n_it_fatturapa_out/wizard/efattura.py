# Copyright 2020 Giuseppe Borruso
# Copyright 2020 Marco Colombo
import re
import os
import base64
from datetime import datetime
from unidecode import unidecode
from odoo.tools import float_repr
from odoo.addons.l10n_it_account.tools.account_tools import encode_for_export

DEFAULT_INVOICE_ITALIAN_DATE_FORMAT = '%Y-%m-%d'


class efattura_out:

    def to_xml(self, env):
        ''' Create the xml file content.
        :return: The XML content as str.
        '''

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
            number_splited = str(number).split('.')
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
            number = number.replace(' ', '').replace('/', '').replace('.', '')
            if len(number) > 4 and len(number) < 13:
                return number
            return False

        def format_price(line):
            res = line.price_unit
            if (
                line.invoice_line_tax_ids and
                line.invoice_line_tax_ids[0].price_include
            ):
                res = line.price_unit / (
                    1 + (line.invoice_line_tax_ids[0].amount / 100))
            price_precision = env['decimal.precision'].precision_get(
                'Product Price for XML e-invoices')
            if price_precision < 2:
                price_precision = 2

            # XXX arrotondamento?
            res = '{prezzo:.{precision}f}'.format(
                prezzo=res, precision=price_precision)
            return res

        def format_quantity(line):
            uom_precision = env['decimal.precision'].precision_get(
                'Product Unit of Measure')
            if uom_precision < 2:
                uom_precision = 2

            quantity = line.quantity + 0
            # XXX arrotondamento?
            res='{qta:.{precision}f}'.format(
                qta=quantity, precision=uom_precision),
            return res[0]

        def get_vat_number(vat):
            #return vat[2:].replace(' ', '') if vat else ""
            return vat[2:] if vat else ""

        def get_vat_country(vat):
            return vat[:2].upper() if vat else ""

        def get_causale(invoice):
            res = []
            if invoice.comment:
                # max length of Causale is 200
                caus_list = invoice.comment.split('\n')
                for causale in caus_list:
                    if not causale:
                        continue
                    causale_list_200 = \
                        [causale[i:i+200] for i in range(0, len(causale), 200)]
                    for causale200 in causale_list_200:
                        # Remove non latin chars, but go back to unicode string,
                        # as expected by String200LatinType
                        causale = encode_for_export(causale200, 200)
                        res.append(causale)
            return res

        def get_nome_attachment(doc_id):
            file_name, file_extension = os.path.splitext(doc_id.name)
            attachment_name = doc_id.datas_fname if len(
                doc_id.datas_fname) <= 60 else ''.join(
                [file_name[:(60 - len(file_extension))], file_extension])
            return encode_for_export(attachment_name, 60)

        def in_eu(partner):
            europe = env.ref('base.europe', raise_if_not_found=False)
            country = partner.country_id
            if not europe or not country or country in europe.country_ids:
                return True
            return False

        if self.partner_id.commercial_partner_id.is_pa:
            # check value code
            code = self.partner_id.ipa_code
        else:
            code = self.partner_id.codice_destinatario

        # Create file content.
        template_values = {
            'formato_trasmissione': "FPA12" if self.partner_id.is_pa else "FPR12",
            'company_id': self.company_id,
            'partner_id': self.partner_id,
            'invoices': self.invoices,
            'progressivo_invio': self.progressivo_invio,
            'encode_for_export': encode_for_export,
            'format_date': format_date,
            'format_monetary': format_monetary,
            'format_numbers': format_numbers,
            'format_numbers_two': format_numbers_two,
            'format_phone': format_phone,
            'format_quantity': format_quantity,
            'format_price': format_price,
            'get_vat_number': get_vat_number,
            'get_vat_country': get_vat_country,
            'get_causale': get_causale,
            'get_nome_attachment': get_nome_attachment,
            'codice_destinatario': code.upper(),
            'in_eu': in_eu,
            'abs': abs,
            'unidecode': unidecode,
            'base64': base64,
        }
        content = env.ref('l10n_it_fatturapa_out.account_invoice_it_FatturaPA_export')\
            .render(template_values)
        return content

    def __init__(self, company_id, partner_id, invoices, progressivo_invio):
        self.company_id = company_id
        self.partner_id = partner_id
        self.invoices = invoices
        self.progressivo_invio = progressivo_invio
