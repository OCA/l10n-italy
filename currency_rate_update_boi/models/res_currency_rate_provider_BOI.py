# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
import requests

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval


class ResCurrencyRateProviderBOI(models.Model):
    _inherit = 'res.currency.rate.provider'

    service = fields.Selection(
        selection_add=[('BOI', 'Bank of Italy')],
    )

    @api.multi
    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != 'BOI':
            return super()._get_supported_currencies()  # pragma: no cover

        return [
            "AFN", "ALL", "DZD", "ADP", "AOA", "XCD", "ANG", "SAR", "ARS", "AMD",
            "AWG", "AUD", "ATS", "AZN", "AZM", "BSD", "BHD", "BDT", "BBD", "BEF",
            "BZD", "XOF", "BMD", "BTN", "BYB", "BYN", "BYR", "BOB", "BAM", "BWP",
            "BRL", "BND", "BGL", "BGN", "XOF", "BIF", "KHR", "XAF", "CAD", "CVE",
            "KYD", "CZK", "CSK", "XAF", "XAF", "CLP", "CNY", "CYP", "COP", "KMF",
            "XAF", "ZRN", "CDF", "KPW", "KRW", "XOF", "CRC", "HRK", "CUP", "DKK",
            "XCD", "DOP", "ECS", "EGP", "SVC", "AED", "ERN", "EEK", "ETB", "FKP",
            "FJD", "PHP", "FIM", "XDR", "FRF", "XAF", "GMD", "GEL", "DEM", "DDM",
            "GHS", "GHC", "JMD", "JPY", "GIP", "DJF", "JOD", "GRD", "XCD", "GTQ",
            "GNF", "GWP", "XOF", "XAF", "GQE", "GYD", "HTG", "HNL", "HKD", "INR",
            "IDR", "IRR", "IQD", "IEP", "ISK", "ILS", "ITL", "YUM", "KZT", "KES",
            "KGS", "KWD", "LAK", "LSL", "LVL", "LBP", "LRD", "LYD", "LTL", "LUF",
            "MOP", "MKD", "MGA", "MGF", "MWK", "MYR", "MVR", "XOF", "MLF", "MTL",
            "MAD", "MRO", "MUR", "MXN", "MDL", "MNT", "MZM", "MZN", "MMK", "NAD",
            "NPR", "NIO", "XOF", "NGN", "NOK", "NZD", "NLG", "OMR", "PKR", "PAB",
            "PGK", "PYG", "PEN", "XPF", "PLN", "PTE", "QAR", "GBP", "ROL", "RON",
            "RUB", "RWF", "SBD", "WST", "SHP", "STD", "XOF", "CSD", "RSD", "CSD",
            "SCR", "SLL", "SGD", "SYP", "ECU", "SKK", "SIT", "SOS", "ESP", "LKR",
            "XCD", "XCD", "USD", "XCD", "ZAR", "SSP", "SDG", "SDD", "SRG", "SRD",
            "SEK", "CHF", "SZL", "TJS", "TJR", "TWD", "TZS", "THB", "XOF", "TOP",
            "TTD", "TND", "TRY", "TRL", "TMM", "TMT", "UAH", "UGX", "HUF", "EUR",
            "SUR", "UYU", "UZS", "VUV", "VEF", "VEB", "VND", "YER", "YDD", "ZMW",
            "ZMK", "ZWD", "ZWN",
        ]

    @api.multi
    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != 'BOI':
            return super()._obtain_rates(base_currency, currencies, date_from,
                                         date_to)  # pragma: no cover

        invert_calculation = False
        if base_currency != 'EUR':
            invert_calculation = True
            if base_currency not in currencies:
                currencies.append(base_currency)
        content = {}

        while date_from <= date_to:
            date_from_str = str(date_from)

            url = (
                "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/"
                "rest/v1.0/dailyRates?referenceDate={ref_date}"
                "&currencyIsoCode={ref_cur}&lang={lang}".format(
                    ref_date=date_from_str,
                    ref_cur='EUR',
                    lang='EN',
                ))
            response = requests.get(url, headers={'Accept': 'application/json'})
            curr_dict = response.content
            content[date_from_str] = {}
            for row in safe_eval(curr_dict)['rates']:
                if row['isoCode'] in currencies:
                    content[date_from_str][row['isoCode']] = row['avgRate']
            date_from += timedelta(days=1)

        if invert_calculation:
            for k in content.keys():
                base_rate = float(content[k][base_currency])
                for rate in content[k].keys():
                    content[k][rate] = str(float(content[k][rate])/base_rate)
                content[k]['EUR'] = str(1.0/base_rate)
        return content
