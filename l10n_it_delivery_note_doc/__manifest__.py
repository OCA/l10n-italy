# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# noinspection PyStatementEffect
{
    "name": "ITA - Documento di trasporto - Senza gestione del magazzino",
    "summary": "Gestione dei DDT senza avere il magazzino installato",
    "author": "Marco Calcagni, Gianmarco Conte, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "version": "14.0.1.0.0",
    "category": "Localization/Italy",
    "license": "AGPL-3",
    "maintainers": ["As400it", "Byloth"],
    "depends": [
        "base",
        "mail",
        "l10n_it_delivery_note_base",
    ],
    "data": [
        "security/delivery_note_group.xml",
        "security/ir.model.access.csv",
        "views/delivery_note_doc.xml",
        "views/report_delivery_note_doc.xml",
    ],
    "installable": True,
}
