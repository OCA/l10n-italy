# Copyright 2013-2017 Agile Business Group sagl (http://www.agilebg.com)
# Copyright 2013-2017 Alex Comba <alex.comba@agilebg.com>
# Copyright 2013-2017 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
# Copyright 2017 Diego Bruselli <d.bruselli@creativiquadrati.it>
# Copyright 2022 Simone Rubino - TAKOBI
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "ITA - Bolle doganali",
    "version": "16.0.1.0.1",
    "category": "Localization/Italy",
    "author": "Agile Business Group, CQ Creativi Quadrati, TAKOBI, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy" "/tree/16.0/l10n_it_bill_of_entry",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "views/company_view.xml",
        "views/account_invoice_view.xml",
    ],
    "demo": [
        "demo/bill_of_entry_demo.xml",
    ],
    "installable": True,
}
