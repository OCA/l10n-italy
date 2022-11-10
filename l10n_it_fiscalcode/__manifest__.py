# Copyright 2014 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Andrea Gallina (Apulia Software)
# Copyright 2018 Matteo Bilotta (Link IT s.r.l.)
# Copyright 2018 Lorenzo Battistini (https://github.com/eLBati)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

{
    "name": "ITA - Codice fiscale",
    "version": "14.0.1.0.2",
    "development_status": "Production/Stable",
    "category": "Localization/Italy",
    "author": "Link IT s.r.l., "
    "Apulia Software, "
    "Odoo Italia Network, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": ["base_vat"],
    "external_dependencies": {
        "python": ["codicefiscale"],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/res.city.it.code.csv",
        "view/fiscalcode_view.xml",
        "view/report_invoice_document.xml",
        "wizard/compute_fc_view.xml",
        "view/company_view.xml",
    ],
    "installable": True,
}
