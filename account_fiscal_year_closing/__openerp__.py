# -*- coding: utf-8 -*-
# Copyright 2016 Odoo Italian Community
#                Odoo Community Association (OCA)
# Copyright 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2012 Domsense srl (<http://www.domsense.com>)
# Copyright 2011 Associazione OpenERP Italia
# Copyright 2009 Zikzakmedia S.L. (http://zikzakmedia.com)
#                Jordi Esteve <jesteve@zikzakmedia.com>
# Copyright 2008 ACYSOS S.L. (http://acysos.com)
#                Pedro Tarrafeta <pedro@acysos.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Fiscal Year Closing",
    "description": """
Generalization of l10n_es_fiscal_year_closing
See http://apps.openerp.com/addon/4506

Fiscal Year Closing Wizard


Replaces the default OpenERP end of year wizards (from account module)
with a more advanced all-in-one wizard that will let the users:
  - Check for unbalanced moves, moves with invalid dates
    or period or draft moves on the fiscal year to be closed.
  - Create the Loss and Profit entry.
  - Create the Net Loss and Profit entry.
  - Create the Closing entry.
  - Create the Opening entry.

It is stateful, saving all the info about the fiscal year closing, so the
user can cancel and undo the operations easily.
    """,
    "version": "8.0.1.0.0",
    "category": "Generic Modules/Accounting",
    "website": "https://odoo-italia.org/",
    "author": "Odoo Italian Community,"
              "Pexego,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
    },
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/fyc_workflow.xml",
        "wizard/wizard_run.xml",
        "view/fyc_view.xml",
        "view/hide_account_wizards.xml",
    ],
}
