# -*- coding: utf-8 -*-
# Copyright 2019 Giacomo Grasso, Gabriele Baldessari
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.currency_rate_update import CurrencyGetterInterface

import requests
from odoo.tools.safe_eval import safe_eval


class BoItalyGetter(CurrencyGetterInterface):
    """Implementation of Curreny_getter_factory interface
    for Bank of Italy
    """
    # Bank of Italy provides a web service to access the exchange rate
    # http://www.bancaditalia.it/compiti/operazioni-cambi/cambi-automatici.pdf
    code = 'IT_BOI'
    name = 'Banca d\'Italia'

    supported_currency_array = [
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
        "ZMK", "ZWD", "ZWN", ]

    def get_updated_currency(self, currency_array, main_currency,
                             max_delta_days):
        """
        Implementation of abstract method of Curreny_getter_interface.
        For technical details refer to the documentation at this url:
        http://www.bancaditalia.it/compiti/operazioni-cambi/cambi-automatici.pdf
        """
        # Emptying the dictionary of currencies to update
        self.updated_currency = {}
        # We do not want to update the main currency
        if main_currency in currency_array:
            currency_array.remove(main_currency)

        url = (
            "https://tassidicambio.bancaditalia.it/terzevalute-wf-web/"
            "rest/v1.0/latestRates?referenceDate={ref_date}"
            "&baseCurrencyIsoCode={ref_cur}&lang={lang}".format(
                ref_date="{}",
                ref_cur='EUR',
                lang='EN',
                ))
        response = requests.get(url, headers={'Accept': 'application/json'})
        curr_dict = response.content
        for row in safe_eval(curr_dict)['latestRates']:
            curr = row['isoCode']
            value = row['eurRate']
            if curr in currency_array:
                self.updated_currency[curr] = value

        return self.updated_currency, self.log_info
