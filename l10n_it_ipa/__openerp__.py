# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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
    "name": "IPA Code (IndicePA)",
    "version": "1.0",
    "category": "Localisation/Italy",
    "author": "KTec S.r.l, Odoo Community Association (OCA)",
    "website": "http://www.ktec.it",
    "description": """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

IPA Code (IndicePA)
===================

This module adds IPA (IndicePA) field to partner
http://www.indicepa.gov.it


Credits
=======

Contributors
------------

* Luigi Di Naro <luigi.dinaro@ktec.it>
* Alex Comba <alex.comba@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

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
    "license": "AGPL-3",
    "depends": ['base'],
    "data": [
        'view/partner_view.xml',
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}
