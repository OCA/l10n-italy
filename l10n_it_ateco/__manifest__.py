# Copyright (C) 2014 Abstract (<http://abstract.it>).
# Copyright (C) 2016 Ciro Urselli (<http://www.apuliasoftware.it>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Codici Ateco",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Abstract,Odoo Community Association (OCA),Odoo Italia Network",
    "development_status": "Beta",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "view/ateco_view.xml",
        "view/partner_view.xml",
        "data/ateco_data.xml",
    ],
    "installable": True,
}
