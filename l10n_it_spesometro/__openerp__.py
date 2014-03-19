# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Spesometro - Comunicazione art.21',
    'version': '0.2',
    'category': 'Localisation/Italy',
    'description': """Spesometro - Comunicazione art.21

Functionalities:
- Creazione comunicazione art.21 in forma Aggregata
- Export file per agenzia delle entrate

""",
    'author': 'Alessandro Camilli',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends" : ['account', 'l10n_it_base'],
    "data" : [
              'security/ir.model.access.csv',
              'spesometro_view.xml',
              'wizard/wizard_crea_comunicazione_view.xml',
              'wizard/wizard_default_view.xml',
              'wizard/wizard_export_view.xml',
        ],
    "demo" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

