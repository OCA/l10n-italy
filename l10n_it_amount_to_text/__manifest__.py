# Copyright 2020 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# Copyright 2022 Sergio Zanchetta (Associazione PNLug APS - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Localizzazione valute per amount_to_text",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Localizza le valute in italiano per amount_to_text",
    "author": "Sergio Zanchetta - Associazione PNLug APS,"
    "Ecosoft Co. Ltd,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["base"],
    "external_dependencies": {"python": ["num2words"]},  # num2words >= 0.5.12
    "data": [],
    "installable": True,
}
