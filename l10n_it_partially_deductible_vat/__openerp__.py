# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
    "depends" : ['l10n_it','account_invoice_tax_by_column'],
    "author" : "OpenERP Italian Community",
    "description": """
    Calcoli aggiuntivi per la gestione dell'IVA parzialmente detraibile. Senza questo modulo non è possibile calcolare correttamente imponibili, imposte e conti imposte relativi all'IVA parzialmente detraibile
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
    'installable': True,
    'active': False,
}
