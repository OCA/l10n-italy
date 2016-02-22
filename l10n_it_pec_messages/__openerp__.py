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

This module allows to correctly parse PEC messages.
According to 'daticert.xml' file, it identifies the message type and other
message data.
'consegna', 'accettazione' and the other notification messages are linked to
the original message that originated them.
It also correctly parses the mail attachments and attaches the original 'eml'
PEC message.
The module adds a 'PEC' menu where to handle PEC messages.


Configuration
-------------

Create a new user associated to the PEC mailbox.
Set 'Never' for 'Receive Messages by Email'.
Configure the fetchmail server (incoming mail server, IMAP or POP)
used to fetch PEC messages and set it as 'PEC'.
Set the users allowed to use that server.
Configure the 'outgoing mail server' (SMTP) used for PEC and set it as 'PEC'.
Link the outgoing mail server to the 'incoming PEC server'.
Add your user to 'PEC reader' group.


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
