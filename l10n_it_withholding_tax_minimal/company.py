# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012-2013 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#    Copyright (C) 2012-2015 Agile Business Group sagl
#    (<http://www.agilebg.com>)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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
#

from openerp.osv import fields, orm


class ResCompany(orm.Model):
    _inherit = 'res.company'
    _columns = {
        'withholding_payment_term_id': fields.many2one(
            'account.payment.term',
            'Withholding tax Payment Term',
            help="The withholding tax will have to be paid within this term"),
        'withholding_account_id': fields.many2one(
            'account.account', 'Withholding account',
            help='Payable account used for amount due to tax authority',
            domain=[('type', '=', 'payable')]),
        'withholding_journal_id': fields.many2one(
            'account.journal', 'Withholding journal',
            help="Journal used for registration of witholding amounts to be "
                 "paid"),
        'authority_partner_id': fields.many2one(
            'res.partner', 'Tax Authority Partner'),
    }


class AccountConfigSettings(orm.TransientModel):
    _inherit = 'account.config.settings'
    _columns = {
        'withholding_payment_term_id': fields.related(
            'company_id', 'withholding_payment_term_id',
            type='many2one',
            relation="account.payment.term",
            string="Withholding tax Payment Term"),
        'withholding_account_id': fields.related(
            'company_id', 'withholding_account_id',
            type='many2one',
            relation="account.account",
            string="Withholding account",
            help='Payable account used for amount due to tax authority',
            domain=[('type', '=', 'payable')]),
        'withholding_journal_id': fields.related(
            'company_id', 'withholding_journal_id',
            type='many2one',
            relation="account.journal",
            string="Withholding journal",
            help='Journal used for registration of witholding amounts to be '
                 'paid'),
        'authority_partner_id': fields.related(
            'company_id', 'authority_partner_id',
            type='many2one',
            relation="res.partner",
            string="Tax Authority Partner"),
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'withholding_payment_term_id': (
                    company.withholding_payment_term_id
                    and company.withholding_payment_term_id.id or False),
                'withholding_account_id': (
                    company.withholding_account_id
                    and company.withholding_account_id.id or False),
                'withholding_journal_id': (
                    company.withholding_journal_id
                    and company.withholding_journal_id.id or False),
                'authority_partner_id': (
                    company.authority_partner_id
                    and company.authority_partner_id.id or False),
            })
        else:
            res['value'].update({
                'withholding_payment_term_id': False,
                'withholding_account_id': False,
                'withholding_journal_id': False,
                'authority_partner_id': False,
            })
        return res
