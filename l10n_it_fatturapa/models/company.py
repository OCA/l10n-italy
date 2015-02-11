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

from openerp import models, fields


class res_company(models.Model):
    _inherit = 'res.company'

    fatturapa_fiscal_position_id = fields.Many2one(
        'fatturapa.fiscal_position', 'Fiscal Position',
        help="Fiscal position used by FatturaPA",
        )
    fatturapa_format_id = fields.Many2one(
        'fatturapa.format', 'Format',
        help="FatturaPA Format",
        )
    fatturapa_sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence',
        help="il progressivo univoco del file è rappresentato da una "
             "stringa alfanumerica di lunghezza massima di 5 caratteri "
             "e con valori ammessi da “A” a “Z” e da “0” a “9”.",
        )
    fatturapa_art73 = fields.Boolean(
        'Art73', help="FatturaPA Art73",
        )


class account_config_settings(models.TransientModel):
    _inherit = 'account.config.settings'

    fatturapa_fiscal_position_id = fields.Many2one(
        related='company_id.fatturapa_fiscal_position_id',
        string="Fiscal Position",
        help='Fiscal position used by FatturaPA'
        )
    fatturapa_format_id = fields.Many2one(
        related='company_id.fatturapa_format_id',
        string="Format",
        help='FatturaPA Format'
        )
    fatturapa_sequence_id = fields.Many2one(
        related='company_id.fatturapa_sequence_id',
        string="Sequence",
        help='FatturaPA Sequence'
        )
    fatturapa_art73 = fields.Boolean(
        related='company_id.fatturapa_art73',
        string="Art73",
        help="Documento emesso secondo modalità e termini stabiliti con DM"
             "ai sensi dell'art. 73 DPR 633/72"
        )

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
                'fatturapa_art73': (
                    company.fatturapa_art73 or False,
                    ),
                })
        else:
            res['value'].update({
                'fatturapa_fiscal_position_id': False,
                'fatturapa_format_id': False,
                'fatturapa_sequence_id': False,
                'fatturapa_art73': False,
                })
        return res
