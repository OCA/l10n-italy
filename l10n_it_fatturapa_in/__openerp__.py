# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 AgileBG SAGL <http://www.agilebg.com>
#    Copyright (C) 2015 innoviu Srl <http://www.innoviu.com>
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
##############################################################################
{
    'name': 'Italian Localization - FatturaPA reception',
    'version': '0.1',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices reception',
    'author': 'Agile Business Group, Innoviu, '
              'Odoo Community Association (OCA)',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License


Italian Localization - FatturaPA - Reception
============================================

This module allows you to receive and parse the fatturaPA XML file version 1.1
http://www.fatturapa.gov.it/export/fatturazione/en/normativa/f-2.htm
received from the Exchange System
http://www.fatturapa.gov.it/export/fatturazione/en/sdi.htm


Configuration
=============

See l10n_it_fatturapa

Usage
=====

 * Go to knowledge -> Documents
 * Create a Incoming fatturaPA file
 * Run Import FatturaPA wizard

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Roberto Onnis <roberto.onnis@innoviu.com>
* Alessio Gerace <alessio.gerace@agilebg.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
""",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa',
        'partner_firstname',
        'stock_invoice_picking_incoterm',
        'l10n_it_withholding_tax',
        ],
    "data": [
        'views/account_view.xml',
        'views/partner_view.xml',
        'wizard/wizard_import_fatturapa_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True
}
