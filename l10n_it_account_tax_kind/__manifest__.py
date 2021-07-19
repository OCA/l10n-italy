# Copyright 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2021 Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "ITA - Natura delle aliquote IVA",
    "version": "14.0.1.0.1",
    "development_status": "Production/Stable",
    "category": "Localization/Italy",
    "summary": "Gestione natura delle aliquote IVA",
    "author": "Odoo Community Association (OCA), Apulia Software s.r.l",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_account",
    ],
    "data": [
        "view/account_tax_kind_view.xml",
        "view/account_tax_view.xml",
        "data/account.tax.kind.csv",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
