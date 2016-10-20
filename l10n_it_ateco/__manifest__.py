# -*- coding: utf-8 -*-
#
#    Copyright (C) 2014 Abstract (<http://abstract.it>).
#    Copyright (C) 2016 Ciro Urselli (<http://www.apuliasoftware.it>).
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Ateco codes",
    "version": "10.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Abstract,Odoo Community Association (OCA),Odoo Italia Network",
    "website": "http://abstract.it",
    "license": "AGPL-3",
    "depends": [
        "sales_team"
    ],
    "data": [
        "security/ir.model.access.csv",
        "view/ateco_view.xml",
        "view/partner_view.xml",
        "data/ateco_data.xml"
    ],
    "installable": True
}
