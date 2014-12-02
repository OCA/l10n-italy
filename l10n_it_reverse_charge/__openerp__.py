# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
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
    'name': 'Italian Localization - Reverse Charge',
    'version': '1.0',
    'category': 'Localization/Italy',
    'description': """Modulo di ausilio alle operazioni Reverse Charge.
Su ogni fattura di acquisto è presente un'azione per creare l'autofattura
usando un partner ed un sezionale configurabili globalmente.

Ulteriori dettagli della fattura, così come le righe, sono da definire
manualmente per il momento.
""",
    'author': 'Abstract',
    'website': 'http://www.abstract.it',
    'license': 'AGPL-3',
    "depends": [
        'base', 'account', 'account_voucher',
        'account_invoice_entry_date'],
    "data": [
        'views/account_view.xml',
        'views/company_view.xml',
    ],
    "demo": [],
    "installable": True
}
