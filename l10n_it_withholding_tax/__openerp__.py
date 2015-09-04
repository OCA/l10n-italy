# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
#
{
    'name': "Italian Localisation - Withholding tax",
    'version': '0.2',
    'category': 'Localisation/Italy',
    'description': """
Ritenute d'acconto sulle fatture fornitore
==========================================

Per utilizzare il modulo bisogna configurare i campi associati alla company:
 - Termine di pagamento della ritenuta
 - Conto di debito per le ritenute da versare
 - Sezionale che conterrà le registrazioni legate alla ritenuta

Durante la compilazione di una fattura fornitore con ritenuta d'acconto,
l'utente dovrà specificare l'importo della ritenuta.

Requisiti
---------
http://wiki.odoo-italia.org/doku.php/area_utente/requisiti/ritenuta_d_acconto

Howto
-----
http://goo.gl/Mt1j7L
""",
    'author': "OpenERP Italian Community,Odoo Community Association (OCA)",
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends": ['account_voucher_cash_basis'],
    "data": [
        'account_view.xml', ],
    "demo": [
        'account_demo.xml',
    ],
    'test': [
        'test/purchase_payment.yml',
    ],
    "active": False,
    "installable": True
}
