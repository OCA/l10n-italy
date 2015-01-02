# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.openerp-italia.org>).
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

from openerp.osv import fields, orm


class L10nItConfigSettings(orm.TransientModel):
    _name = 'l10n_it.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'module_l10n_it_pec': fields.boolean(
            'Use Pec Mail in Partner Profile',
            help="""Install l10n_it_pec module for pec mail management"""
        ),
        'module_l10n_it_fiscalcode': fields.boolean(
            'Use fiscal code in Partner Profile',
            help="""Install l10n_it_fiscalcode module for fiscal
code management"""
        ),
    }
