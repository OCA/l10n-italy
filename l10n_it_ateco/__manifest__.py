# Copyright (C) 2014 Abstract (<http://abstract.it>).
# Copyright (C) 2016 Ciro Urselli (<http://www.apuliasoftware.it>).
# Copyright (C) 2025 Michele Di Croce (<http://www.stesi.consulting>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Codici Ateco",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "author": "Abstract,Odoo Community Association (OCA),Odoo Italia Network",
    "development_status": "Beta",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/ateco_view.xml",
        "views/partner_view.xml",
        "data/ateco_data.xml",
    ],
    "installable": True,
}
