# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Abstract (http://www.abstract.it)
#    Author: Davide Corio <davide.corio@abstract.it>
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Split Payment',
    'version': '8.0.1.0.0',
    'category': 'Localization/Italy',
    'summary': 'Split Payment',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Italian Localization - split payment
====================================

Law: http://goo.gl/1riAwt (Articolo 17 ter)

Module to generate Split Payment accounting entries

Configuration
=============

To configure this module, you need to:

* go to Settings, Configuration, Accounting and configure
'Split Payment Write-off account' (like 'IVA n/debito sospesa SP').
Write-off account should be different from standard debit VAT,
in order to separately add it in VAT statement.
* configure the fiscal position used for split payment, setting 'Split Payment'
flag. In fiscal position, map standard VAT with SP VAT, like the following:

.. image:: /l10n_it_split_payment/static/fiscal_position.png


-------------------------------------------------------------------------------

22SPL is configured like the following:


.. image:: /l10n_it_split_payment/static/SP.png

Credits
=======

Contributors
------------

* Davide Corio <davide.corio@abstract.it>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
""",
    'author': 'Abstract, Agile Business Group, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.abstract.it',
    'license': 'AGPL-3',
    'depends': [
        'account'],
    'data': [
        'views/account_view.xml',
        'views/config_view.xml',
    ],
    'installable': True,
}
