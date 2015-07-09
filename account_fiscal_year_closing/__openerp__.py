# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2009 Zikzakmedia S.L. (http://zikzakmedia.com)
#                       Jordi Esteve <jesteve@zikzakmedia.com>
#    Copyright (c) 2008 ACYSOS S.L. (http://acysos.com)
#                       Pedro Tarrafeta <pedro@acysos.com>
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    "name": "Fiscal Year Closing",
    "version": "1.0",
    "author": "OpenERP Italian Community,"
              "Pexego,"
              "Odoo Community Association (OCA)",
    "website": "http://www.openerp-italia.org",
    "category": "Generic Modules/Accounting",
    "description": """
Generalization of l10n_es_fiscal_year_closing
( http://apps.openerp.com/addon/4506 )

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
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "init_xml": [],
    "update_xml": [
        "security/ir.model.access.csv",
        "fyc_workflow.xml",
        "wizard/wizard_run.xml",
        "fyc_view.xml",
        "hide_account_wizards.xml",
    ],
    "active": False,
    "installable": True
}
