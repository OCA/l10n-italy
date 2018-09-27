# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
#
#    Copyright © 2018 Openforce Srls Unipersonale (www.openforce.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or (at
#    your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/lgpl-3.0.txt.
#
##############################################################################

{
    'name': 'Italian Localization - FatturaPA - Emission - PEC Support',
    'version': '10.0.1.0.3',
    'category': 'Localization/Italy',
    'summary': "Send electronic invoices via PEC",
    'author': 'Openforce Srls Unipersonale',
    'website': 'http://www.openforce.it',
    'license': 'LGPL-3',
    "depends": ['fetchmail',
                'l10n_it_fatturapa_out', ],
    "data": [
        'views/fatturapa_attachment_out.xml',
        'views/fetchmail_server.xml',
        'views/ir_mail_server.xml',
    ],
    "installable": True
}
