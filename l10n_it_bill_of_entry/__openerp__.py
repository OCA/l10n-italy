# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
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
#
{
    'name': 'Italian Localisation - Bill of Entry',
    'version': '0.1',
    'category': 'Localisation/Italy',
    'description': """
Bolle doganali
===============

Specifiche
----------

http://wiki.openerp-italia.org/doku.php/area_utente/requisiti/extraue

Ci sono 3 documenti coinvolti:

 - Fattura fornitore
 - Fattura spedizioniere
 - Bolla doganale

Le relazioni:

N bolle doganali -> N fatture fornitore
1 fattura spedizioniere -> N bolle doganali

Configurazione
--------------

E' necessario configurare in contabilità il sezionale da utilizzare per il
giroconto di chiusura.

Utilizzo
--------

Dalla bolla doganale è possibile collegare manualmente la (o le) fattura(e)
fornitore corrispondente.

Dalla fattura spedizioniere è possibile generare la (o le) bolla(e) doganale(i)
tramite il bottone 'genera bolla'. Per questa operazione bisogna prima
configurare un template di fattura (usato per la bolla doganale).

Nella fattura spedizioniere bisogna indicare quale (o quali) riga (righe)
rappresenti(no) l'IVA anticipata alla dogana.

Alla conferma della fattura spedizioniere, verrà generata la scrittura
contabile di giroconto per chiudere la bolla doganale.

""",
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": ['base', 'account_invoice_template'],
    "data": [
        'account_invoice_view.xml',
        'company_view.xml',
    ],
    "demo": [],
    "installable": True
}
