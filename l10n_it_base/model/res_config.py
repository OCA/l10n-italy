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

from openerp import models
from openerp import fields


class L10nItConfigSettings(models.TransientModel):
    _name = 'l10n_it.config.settings'
    _inherit = 'res.config.settings'

    module_l10n_it_base_location_geonames_import = fields.Boolean(
        'Use Geonames.org to import Location',
        help="""Use Geonames.org to import Location in Partner Profile"""
    )
    module_l10n_it_pec = fields.Boolean(
        'Use Pec Mail in Partner Profile',
        help="""Install l10n_it_pec module for PEC mail management"""
    )
    module_l10n_it_ateco = fields.Boolean(
        'Use Ateco codes',
        help="""Install l10n_it_ateco module for Ateco code management"""
    )
