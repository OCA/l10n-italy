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
            help="il progressivo univoco del file è rappresentato da una "
                 "stringa alfanumerica di lunghezza massima di 5 caratteri "
                 "e con valori ammessi da “A” a “Z” e da “0” a “9”.",
            ),
        'fatturapa_art73': fields.boolean('Art73'),
        'fatturapa_pub_administration_ref': fields.char(
            'Public Administration Reference Code', size=20,
            ),
        'fatturapa_rea_office': fields.related(
            'partner_id', 'rea_office', type='many2one',
            relation='res.country.state', string='REA office'),
        'fatturapa_rea_number': fields.related(
            'partner_id', 'rea_code', type='char',
            size=20, string='Rea Number'),
        'fatturapa_rea_capital': fields.related(
            'partner_id', 'rea_capital', type='float',
            string='Rea Capital'),
        'fatturapa_rea_partner': fields.related(
            'partner_id', 'rea_member_type', type='selection',
            selection=[
                ('SU', 'Unique Member'),
                ('SM', 'Multiple Members'),
                ],
            string='Member Type'),
        'fatturapa_rea_liquidation': fields.related(
            'partner_id', 'rea_liquidation_state', type='selection',
            selection=[
                ('LS', 'In liquidation'),
                ('LN', 'Not in liquidation'),
                ],
            string='Liquidation State'),
        'fatturapa_tax_representative': fields.many2one(
            'res.partner', 'Legal Tax Representative'
            ),
        'fatturapa_sender_partner': fields.many2one(
            'res.partner', 'Third Party/Sender'
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
            help="il progressivo univoco del file è rappresentato da una "
                 "stringa alfanumerica di lunghezza massima di 5 caratteri "
                 "e con valori ammessi da “A” a “Z” e da “0” a “9”.",
            ),
        'fatturapa_art73': fields.related(
            'company_id', 'fatturapa_art73',
            type='boolean',
            string="Art73",
            help="indicates whether the document has been issued in accordance"
                 " with the terms and conditions established by ministerial "
                 "decree in accordance with Article 73 of Presidential Decree"
                 ""
                 "633/72 (this allows the company to issue the same"
                 " year more documents with the same number)"
            ),
        'fatturapa_pub_administration_ref': fields.related(
            'company_id', 'fatturapa_pub_administration_ref',
            type='char',
            size=20,
            string="Public Administration Reference Code",
            ),
        'fatturapa_rea_office': fields.related(
            'company_id', 'fatturapa_rea_office',
            type='many2one',
            relation="res.country.state",
            string="Rea Office",
            ),
        'fatturapa_rea_number': fields.related(
            'company_id', 'fatturapa_rea_number',
            type='char',
            size=20,
            string="Rea Number",
            ),
        'fatturapa_rea_capital': fields.related(
            'company_id', 'fatturapa_rea_capital',
            type='float',
            string="Rea Capital",
            ),
        'fatturapa_rea_partner': fields.related(
            'company_id', 'fatturapa_rea_partner',
            type='selection',
            selection=[('SU', 'Single Partner'),
                       ('SM', 'Many Partners')],
            string="Rea Copartner",
            ),
        'fatturapa_rea_liquidation': fields.related(
            'company_id', 'fatturapa_rea_liquidation',
            type='selection',
            selection=[('LN', 'Company Not in Liquidation'),
                       ('LS', 'Company In Liquidation')],
            string="Rea Liquidation",
            ),
        'fatturapa_tax_representative': fields.related(
            'company_id', 'fatturapa_tax_representative',
            type='many2one',
            relation="res.partner",
            string="Legal Tax Representative",
            help="Used when a foreign company needs to send invoices to an"
                 "Italian PA and has a tax representative in Italy"
            ),
        'fatturapa_sender_partner': fields.related(
            'company_id', 'fatturapa_sender_partner',
            type='many2one',
            relation="res.partner",
            string="Third Party/Sender",
            help="Used when company sends invoices to a third party and they "
                 "send invoices to SDI"
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
                    company.fatturapa_fiscal_position_id.id or False
                    ),
                'fatturapa_format_id': (
                    company.fatturapa_format_id and
                    company.fatturapa_format_id.id or False
                    ),
                'fatturapa_sequence_id': (
                    company.fatturapa_sequence_id and
                    company.fatturapa_sequence_id.id or False
                    ),
                'fatturapa_art73': (
                    company.fatturapa_art73 or False
                    ),
                'fatturapa_pub_administration_ref': (
                    company.fatturapa_pub_administration_ref or False
                    ),
                'fatturapa_rea_office': (
                    company.fatturapa_rea_office and
                    company.fatturapa_rea_office.id or False
                    ),
                'fatturapa_rea_number': (
                    company.fatturapa_rea_number or False
                    ),
                'fatturapa_rea_capital': (
                    company.fatturapa_rea_capital or False
                    ),
                'fatturapa_rea_partner': (
                    company.fatturapa_rea_partner or False
                    ),
                'fatturapa_rea_liquidation': (
                    company.fatturapa_rea_liquidation or False
                    ),
                'fatturapa_tax_representative': (
                    company.fatturapa_tax_representative and
                    company.fatturapa_tax_representative.id or False
                    ),
                'fatturapa_sender_partner': (
                    company.fatturapa_sender_partner and
                    company.fatturapa_sender_partner.id or False
                    ),
                })
        else:
            res['value'].update({
                'fatturapa_fiscal_position_id': False,
                'fatturapa_format_id': False,
                'fatturapa_sequence_id': False,
                'fatturapa_art73': False,
                'fatturapa_pub_administration_ref': False,
                'fatturapa_rea_office': False,
                'fatturapa_rea_number': False,
                'fatturapa_rea_capital': False,
                'fatturapa_rea_partner': False,
                'fatturapa_rea_liquidation': False,
                'fatturapa_tax_representative': False,
                'fatturapa_sender_partner': False,
                })
        return res
