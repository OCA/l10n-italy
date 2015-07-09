# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#    Copyright 2014 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
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
##############################################################################

{
    "name": "Manage Folders for Pec Messages",
    "version": "1.0",
    "author": "Agile Business Group",
    "category": "Certified Mailing",
    "website": "http://www.agilebg.com",
    "description": """
Pec Messages Management
-----------------------

This module allows you to split the messages pec ,
in folders organized in hierarchical structures .
You can define and organize structures ,
for each type of server to which pec and ' enabled for reading.
for more information about the qualifications of a user to a server pec ,
see the module l10n_it_pec_messages


Configuration
-------------

no configuration is needed


Contributors
------------

 - Alessio Gerace <alessio.gerace@gmail.com>
 - Lorenzo Battistini <lorenzo.battistini@agilebg.com>

""",
    'images': [],
    'depends': [
        'l10n_it_pec_messages'
    ],
    'init_xml': [],
    'data': [
        "view/mail_view.xml",
        "security/ir.model.access.csv",
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
