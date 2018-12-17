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
from openerp.osv.osv import except_osv


class ResCompany(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'fatturapa_fiscal_position_id': fields.many2one(
            'fatturapa.fiscal_position', 'Fiscal Position',
            help="Fiscal position used by FatturaPA",
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
            relation='res.province', string='REA office'),
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
    'fatturapa_stabile_organizzazione': fields.many2one(
        'res.partner', 'Stabile Organizzazione',
        help='Blocco da valorizzare nei casi di cedente / prestatore non '
             'residente, con stabile organizzazione in Italia'
        ),
    }

    def _check_fatturapa_sequence_id(self, cr, uid, ids, context=None):
        for company in self.browse(cr, uid, ids, context):
            if company.fatturapa_sequence_id:
                journal = self.pool.get('account.journal').search(cr, uid, [
                    ('sequence_id', '=', company.fatturapa_sequence_id.id)
                ], limit=1)
                if journal:
                    return False
        return True

    _constraints = [
        (_check_fatturapa_sequence_id, 'Sequence already used by journal. Please select another one.', ['fatturapa_sequence_id']),
    ]

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(account_config_settings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            default_sequence = self.pool.get('ir.sequence').search(cr, uid, [
                ('code', '=', 'account.invoice.fatturapa')
            ])
            default_sequence = (
                default_sequence[0] if default_sequence else False)
            res['value'].update({
                'fatturapa_fiscal_position_id': (
                    company.fatturapa_fiscal_position_id and
                    company.fatturapa_fiscal_position_id.id or False
                    ),
                'fatturapa_sequence_id': (
                    company.fatturapa_sequence_id and
                    company.fatturapa_sequence_id.id or default_sequence
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
                'fatturapa_stabile_organizzazione': (
                    company.fatturapa_stabile_organizzazione and
                    company.fatturapa_stabile_organizzazione.id or False
                    ),
                })
        else:
            res['value'].update({
                'fatturapa_fiscal_position_id': False,
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
                'fatturapa_stabile_organizzazione': False,
                })
        return res
