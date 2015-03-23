# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Alessio Gerace <alessio.gerace@agilebg.com>
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
    'name': 'REA Register',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'summary': 'Manage fields for  Economic Administrative catalogue',
    'author': 'Agile Business Group, Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

REA Registration
=======================

The module implement fields of REA data in partner
http://www.registroimprese.it/il-registro-imprese-e-altre-banche-dati#page=registro-imprese

Usage
=====

The module adds fields in page Accounting of partner form, where you can
add data of registry of businesses


Credits
=======

Contributors
------------

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
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_base', 'account'
    ],
    "data": [
        'partner_view.xml',
    ],
    "test": [],
    "demo": [],
    "installable": True
}
