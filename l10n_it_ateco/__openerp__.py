# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract
#    (<http://abstract.it>).
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
##############################################################################
{
    "name": "Ateco codes",
    "version": "8.0.1.0.1",
    "category": "Localisation/Italy",
    "description": """Italian Localisation module - Ateco codes

    Funcionalities:

    - Add Ateco codes model
    - Reference Ateco codes to partner model

    """,
    "author": "Abstract,Odoo Community Association (OCA)",
    "website": "http://abstract.it",
    "license": "AGPL-3",
    "depends": [
        "base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "view/ateco_view.xml",
        "view/partner_view.xml",
        "data/ateco_data.xml"
    ],
    "active": False,
    "installable": True
}
