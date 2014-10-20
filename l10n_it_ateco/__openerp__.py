# -*- encoding: utf-8 -*-
{
    "name": "Ateco codes",
    "version": "1.0",
    "category": "Localisation/Italy",
    "description": """Italian Localisation module - Ateco codes

    Funcionalities:

    - Add Ateco codes model
    - Reference Ateco codes to partner model

    """,
    "author": "Abstract",
    "website": "http://www.openerp-italia.org",
    "depends": [
        "sale"
    ],
    "data": [
        "security/ir.model.access.csv",
        "view/ateco_view.xml",
        "view/partner_view.xml",
        "data/ateco_data.xml"
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    "installable": True
}
