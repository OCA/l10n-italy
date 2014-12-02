# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
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

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    rc_partner_id = fields.Many2one(
        'res.partner',
        string='RC Sale Invoice Partner',
        help="Partner used on RC sale invoices.")
    rc_journal_id = fields.Many2one(
        'account.journal',
        string='RC Journal',
        help="Journal used on RC sale invoices.")
    rc_payment_journal_id = fields.Many2one(
        'account.journal',
        string='RC Payment Journal',
        help="Journal used to pay RC sale invoices.")
    rc_transitory_account_id = fields.Many2one(
        'account.account',
        string='RC Transitory Account',
        help="Transitory account used on reverse invoice.")
    rc_auto_invoice = fields.Boolean(
        string='RC Auto Invoice',
        help="Automatically create the corresponding customer invoice."),


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    rc_partner_id = fields.Many2one(
        'res.partner',
        string='RC Sale Invoice Partner',
        related='company_id.rc_partner_id',
        help='Partner used on RC sale invoices.',)
    rc_journal_id = fields.Many2one(
        'account.journal',
        string="RC Journal",
        related='company_id.rc_journal_id',
        help='Journal used on RC sale invoices.')
    rc_payment_journal_id = fields.Many2one(
        'account.journal',
        string="RC Payment Journal",
        related='company_id.rc_payment_journal_id',
        help='Journal used to pay RC sale invoices.')
    rc_transitory_account_id = fields.Many2one(
        'account.account',
        string="RC Transitory Account",
        related='company_id.rc_transitory_account_id',
        help='Transitory account used on reverse invoice.')
    rc_auto_invoice = fields.Boolean(
        string="RC Auto Invoice",
        related='company_id.rc_auto_invoice',
        help="Automatically create the corresponding customer invoice.")

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        if not context:
            context = {}
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'rc_partner_id': company.rc_partner_id and
                company.rc_partner_id.id or False,
                'rc_journal_id': company.rc_journal_id and
                company.rc_journal_id.id or False,
                'rc_payment_journal_id': company.rc_payment_journal_id and
                company.rc_payment_journal_id.id or False,
                'rc_transitory_account_id': company.rc_transitory_account_id and
                company.rc_transitory_account_id.id or False,
                'rc_auto_invoice': company.rc_auto_invoice,
                })
        else:
            res['value'].update({
                'rc_partner_id': False,
                'rc_journal_id': False,
                'rc_payment_journal_id': False,
                'rc_transitory_account_id': False,
                'rc_auto_invoice': False,
                })
        return res
