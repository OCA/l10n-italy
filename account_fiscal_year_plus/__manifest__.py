# Copyright 2016 Camptocamp SA
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Account Fiscal Year",
    "summary": "Create a menu for Account Fiscal Year",
    "version": "12.0.1.1.1",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-financial-tools",
    "author": "Agile Business Group, Camptocamp SA, "
              "Odoo Community Association (OCA) and other partners",
    "maintainers": ["eLBati"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        'account_fiscal_year',
        "date_range_plus",
        "account_fiscal_year",
    ],
    "data": [
        # "data/date_range_type.xml",
        "views/account_views.xml",
    ],
}
