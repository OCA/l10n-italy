# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) SHS-AV s.r.l. (<http://www.zeroincombenze.it>)
#    All Rights Reserved
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


from openerp.tests.common import SingleTransactionCase
import logging

__version__ = "0.0.1"
_logger = logging.getLogger(__name__)
INIT_PARTY_ISSUE = '1234567A'


class TestAccountMoves(SingleTransactionCase):

    def setup_invoice_date(self):
        """Acquire first invoice date
        """
        self.invoice_date = self.env['account.invoice'].search(
            [('date_invoice', '!=', False)],
            order='date_invoice desc',
            limit=1).date_invoice

    def setup_company(self):
        """Setup company
        """
        pass

    def create_invoice_1(self):
        partner_id = self.ref('base.res_partner_9')
        journal_id = self.ref('account.sales_journal')
        payment_term_id = self.ref('account.account_payment_term')
        account_receivable_id = self.ref('account.a_recv')
        account_revenue_id = self.ref('account.rev')
        return self.env['account.invoice'].create({
            'date_invoice': self.invoice_date,
            'type': 'out_invoice',
            'journal_id': journal_id,
            'partner_id': partner_id,
            'payment_term': payment_term_id,
            'account_id': account_receivable_id,
            'invoice_line': [(
                0, 0, {
                    'name': 'test',
                    'quantity': 1.0,
                    'price_unit': 100.00,
                    'account_id': account_revenue_id
                }
            )]
        })

    def setUp(self):
        self.setup_company()
        self.setup_invoice_date()
        self.create_invoice_1()
