# -*- coding: utf-8 -*-
# Copyright 2018 Giuseppe Stoduto
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from openerp import models, api


class AccountVoucher(models.Model):

    _inherit = 'account.voucher'

    @api.multi
    def action_move_line_create(self):
        so_obj = self.env['sale.order']

        res = super(AccountVoucher, self).action_move_line_create()
        for line in self.line_cr_ids:
            if line.reconcile:
                invoice = line.move_line_id.invoice
                so_ids = so_obj.search([('invoice_ids', '=', invoice.id)])
                for so_id in so_ids:
                    if so_id.ddt_ids and so_id.state != 'done':
                        so_id.action_done()
        return res

    @api.multi
    def cancel_voucher(self):
        inv_obj = self.env['account.invoice']
        res = super(AccountVoucher, self).cancel_voucher()
        for line in self.line_cr_ids:
            if line.reconcile:
                invoice = line.move_line_id.invoice
                inv_obj.set_so_state(invoice, 'progress')
        return res
