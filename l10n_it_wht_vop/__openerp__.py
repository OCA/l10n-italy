# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2014 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2014 L.S. Advanced Software srl (<http://www.lsweb.it>)
#    Copyright (C) 2014 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
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
    'name': "Italian Localisation - Withholding tax + VAT on payment handling",
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """
Ritenute d'acconto più IVA per cassa
====================================

Questo modulo permette di generare le corrette registrazioni contabili quando si utilizzano entrambi i moduli di IVA per cassa (account_vat_on_payment) e ritenute d'acconto (l10n_it_withholding_tax)


Contributors
------------

 - Lorenzo Battistini <lorenzo.battistini@agilebg.com>
 - Davide Corio <davide.corio@lsweb.it>
""",
    'author': 'OpenERP Italian Community',
    'website': 'http://www.openerp-italia.org',
    'license': 'AGPL-3',
    "depends" : [
        'account_vat_on_payment',
        'l10n_it_withholding_tax'
        ],
    "data" : [],
    "demo" : [
        ],
    'test' : [
        ],
    "active": False,
    "installable": True
}
