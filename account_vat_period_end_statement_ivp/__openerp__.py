# -*- coding: utf-8 -*-
# Copyright 2011-12 Domsense s.r.l. <http://www.domsense.com>.
# Copyright 2012-15 Agile Business Group sagl <http://www.agilebg.com>
# Copyright 2012-15 LinkIt Spa <http://http://www.linkgroup.it>
# Copyright 2015-17 Associazione Odoo Italia <http://www.odoo-italia.org>
# Copyright 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2017-18 Sergio Corato <https://efatto.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "IVP 2017",
    "summary": "IVP 2017 export xml file",
    "version": "8.0.4.0.0",
    "development_status": "Beta",
    "category": "Generic Modules/Accounting",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Agile Business Group, Odoo Italia Associazione,"
              " Odoo Community Association (OCA), Sergio Corato",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale",
        "account",
        "account_vat_period_end_statement",
        "l10n_it_vat_registries",
        "l10n_it_fiscalcode",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_view.xml",
        "wizard/vat_settlement.xml",
    ],
    "external_dependencies": {
        "python": ["pyxb"],
    },
}
