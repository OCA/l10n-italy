# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014-2015 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
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
    "name": "Pec Messages",
    "version": "1.0",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "category": "Certified Mailing",
    "website": "http://www.agilebg.com",
    "license": "AGPL-3",
    "description": """
Pec Messages Management
-----------------------

Read README.rst file for more details

Contributors
------------

 - Alessio Gerace <alessio.gerace@gmail.com>
 - Lorenzo Battistini <lorenzo.battistini@agilebg.com>
 - Roberto Onnis <roberto.onnis@innoviu.com>
""",
    'depends': [
        'fetchmail', 'mail', 'l10n_it_pec',
    ],
    'data': [
        "security/mail_data.xml",
        "view/fetchmail_view.xml",
        "view/ir_mail_server.xml",
        "wizard/mail_compose_message_view.xml",
        "view/mail_view.xml",
        "view/res_users.xml",
        "security/ir.model.access.csv",
    ],
    'demo': [
        'demo/pec_data.xml',
        ],
    'installable': True,
    'active': False,
}
