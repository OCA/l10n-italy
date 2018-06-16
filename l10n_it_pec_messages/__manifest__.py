# -*- coding: utf-8 -*-
# Copyright 2014-2018 Agile Business Group http://www.agilebg.com
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Pec Messages",
    "summary": "Send and receive PEC messages",
    "version": "10.0.1.0.0",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    "category": "Certified Mailing",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "LGPL-3",
    'depends': [
        'fetchmail', 'mail', 'contacts', 'document'
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
    'installable': True
}
