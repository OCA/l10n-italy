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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm


class res_company(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'fatturapa_fiscal_position_id': fields.many2one(
            'fatturapa.fiscal_position', 'Fiscal Position',
            help="Fiscal position used by FatturaPA",
            ),
        'fatturapa_format_id': fields.many2one(
            'fatturapa.format', 'Format',
            help="FatturaPA Format",
            ),
        'fatturapa_sequence_id': fields.many2one(
            'ir.sequence', 'Sequence',
            help="FatturaPA Sequence",
            ),
    }


class account_config_settings(orm.TransientModel):
    _inherit = 'account.config.settings'
    _columns = {
        'fatturapa_fiscal_position_id': fields.related(
            'company_id', 'fatturapa_fiscal_position_id',
            type='many2one',
            relation="fatturapa.fiscal_position",
            string="Fiscal Position",
            help='Fiscal position used by FatturaPA'
            ),
        'fatturapa_format_id': fields.related(
            'company_id', 'fatturapa_format_id',
            type='many2one',
            relation="fatturapa.format",
            string="Format",
            help='FatturaPA Format'
            ),
        'fatturapa_sequence_id': fields.related(
            'company_id', 'fatturapa_sequence_id',
            type='many2one',
            relation="ir.sequence",
            string="Sequence",
            help='FatturaPA Sequence'
            ),
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(account_config_settings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'fatturapa_fiscal_position_id': (
                    company.fatturapa_fiscal_position_id and
                    company.fatturapa_fiscal_position_id.id or False,
                    ),
                'fatturapa_format_id': (
                    company.fatturapa_format_id and
                    company.fatturapa_format_id.id or False,
                    ),
                'fatturapa_sequence_id': (
                    company.fatturapa_sequence_id and
                    company.fatturapa_sequence_id.id or False,
                    ),
                })
        else:
            res['value'].update({
                'fatturapa_fiscal_position_id': False,
                'fatturapa_format_id': False,
                'fatturapa_sequence_id': False,
                })
        return res
