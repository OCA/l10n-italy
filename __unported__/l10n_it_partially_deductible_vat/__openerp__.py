# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#    Copyright (C) 2012-2014 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
    "name" : "Italy - Partially Deductible VAT",
    "version" : "0.1",
    "depends" : ['account'],
    "author" : "OpenERP Italian Community,Odoo Community Association (OCA)",
    "description": """
    Calcoli aggiuntivi per la gestione dell'IVA parzialmente detraibile. Senza questo modulo non è possibile calcolare correttamente imponibili, imposte e conti imposte relativi all'IVA parzialmente detraibile.
    La configurazione dell'IVA parzialmente detraibile deve essere quella utilizzata dal modulo 'l10n_it', anche se non viene usato tale modulo.
    """,
    "license": "AGPL-3",
    "category" : "Localisation/Italy",
    'website': 'http://www.openerp-italia.org/',
    'init_xml': [
        ],
    'update_xml': [
        ],
    'demo_xml': [
        ],
    'test': [
        'test/account_tax.xml',
        'test/tax_computation.yml',
        ],
    'installable': False,
    'active': False,
}
