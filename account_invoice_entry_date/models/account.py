# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2004-2010 ISA srl (<http://www.isa.it>).
#    Copyright (C) 2014 Associazione Odoo Italia
#    http://www.openerp-italia.org>
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

import time
from openerp import fields, models
from openerp.tools.translate import _
from openerp.exceptions import Warning


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    registration_date = fields.Date(
        'Registration Date',
        states={
            'paid': [('readonly', True)],
            'open': [('readonly', True)],
            'close': [('readonly', True)]
            },
        select=True,
        help="Keep empty to use the current date")

    def action_move_create(self, cr, uid, ids, context=None):

        if not context:
            context = {}

        super(AccountInvoice, self).action_move_create(
            cr, uid, ids, context=context)

        for inv in self.browse(cr, uid, ids):
            date_invoice = inv.date_invoice
            reg_date = inv.registration_date
            if not inv.registration_date:
                if not inv.date_invoice:
                    reg_date = time.strftime('%Y-%m-%d')
                else:
                    reg_date = inv.date_invoice

            if date_invoice and reg_date:
                if (date_invoice > reg_date):
                    raise Warning(_("The invoice date cannot be later than the"
                                    " date of registration!"))

            date_start = inv.registration_date or inv.date_invoice \
                or time.strftime('%Y-%m-%d')
            date_stop = inv.registration_date or inv.date_invoice \
                or time.strftime('%Y-%m-%d')

            period_ids = self.pool.get('account.period').search(
                cr, uid,
                [
                    ('date_start', '<=', date_start),
                    ('date_stop', '>=', date_stop),
                    ('company_id', '=', inv.company_id.id)
                    ])
            if period_ids:
                period_id = period_ids[0]

            self.write(
                cr, uid, [inv.id], {
                    'registration_date': reg_date, 'period_id': period_id})

            mov_date = reg_date or inv.date_invoice or time.strftime(
                '%Y-%m-%d')

            self.pool.get('account.move').write(
                cr, uid, [inv.move_id.id], {'state': 'draft'})

            sql = "update account_move_line set period_id="+str(
                period_id) + ",date='" + mov_date + "' where move_id = " + str(
                inv.move_id.id)

            cr.execute(sql)

            self.pool.get('account.move').write(
                cr, uid, [inv.move_id.id],
                {'period_id': period_id, 'date': mov_date})

            self.pool.get('account.move').write(
                cr, uid, [inv.move_id.id], {'state': 'posted'})

        self._log_event(cr, uid, ids)
        return True
