# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
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

from openerp.osv import fields, orm


class res_partner(orm.Model):
    _inherit = "res.partner"

    _columns = {
        'eori_code': fields.char('EORI Code', size=20),
        'license_number': fields.char('License Code', size=20),
        # 1.2.6 RiferimentoAmministrazione
        'pa_partner_code': fields.char('PA Code for partner', size=20),
        # 1.2.1.4
        'register': fields.char('Professional Register', size=60),
        # 1.2.1.5
        'register_province': fields.many2one(
            'res.country.state', string='Register Province'),
        # 1.2.1.6
        'register_code': fields.char('Register Code', size=60),
        # 1.2.1.7
        'register_regdate': fields.date('Register Registration Date'),
        # 1.2.1.8
        'register_fiscalpos': fields.many2one(
            'fatturapa.fiscal_position',
            string="Register Fiscal Position"),
    }
