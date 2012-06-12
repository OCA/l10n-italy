# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    All Rights Reserved
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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
    'name': "Italian Localisation - Ritenute d'acconto",
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """
    Modulo per le ritenute d'acconto sulle fatture fornitore
    
    http://wiki.openerp-italia.org/doku.php/area_utente/requisiti/ritenuta_d_acconto
""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends" : ['account_invoice_template'],
    "init_xml" : [
        'account_view.xml',
        ],
    "update_xml" : [],
    "demo_xml" : [],
    "active": False,
    "installable": True
}
