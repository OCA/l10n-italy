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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Italian Localization - FatturaPA in Ingresso',
    'version': '0.1',
    'category': 'Localization/Italy',
    'summary': 'Fatturazione Elettronica per la Pubblica Amministrazione',
    'description': """
    Fatturazione Elettronica per la Pubblica Amministrazione.
    Gestione delle fatture in ingresso
    """,
    'author': 'Agile Business Group, Innoviu',
    'website': 'https://github.com/OCA/l10n-italy',
    'license': 'AGPL-3',
    "depends": [
        'l10n_it_fatturapa',
    ],
    "data": [
        'views/account_view.xml',
        'wizard/wizard_import_fatturapa_view.xml',
    ],
    "test": [],
    "demo": [],
    "installable": True
}
