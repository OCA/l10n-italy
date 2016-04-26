# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2016 Alessandro Camilli (<alessandrocamilli@openforce.it>)
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
    'name': 'Banking SEPA Italian Credit Transfer CBI',
    'version': '0.2',
    'category': 'Banking',
    'description': """ 
     le specifiche CBI del
bonifico XML SEPA (versione 00.03.09) si basano sul messaggio ISO20022 
pain.001.001.03 e sono compliant al Rulebook SEPA. Come su riportato, il 
messaggio pain.001.001.03 non è stato utilizzato integralmente, essendo 
strutturato in maniera tale da poter essere applicabile ad una pletora molto 
estesa di casistiche e di soggetti. 
Ne consegue che, al fine di implementare le regole di comunità, il tracciato 
SEPA Credit Transfer CBI preso ad esempio è un sottoinsieme del succitato 
messaggio ISO e raccoglie i requisiti necessari alla corretta esecuzione di un
 bonifico in Italia, come ad esempio la presenza obbligatoria dell’ABI della 
 banca di addebito contenuto nel campo “MmbId” che è invece facoltativo
nel tracciato ISO. 
""",
    'author': 'Openforce di Alessandro Camilli',
    'website': 'http://www.openforce.it',
    'license': 'AGPL-3',
    "depends" : [
                 'account_banking_pain_base',
                 ],
    "data" : [
        'wizard/export_sepa_cbi_view.xml',
        'data/payment_type_sepa_cbi.xml',
        ],
    "demo" : [],
    "active": False,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

