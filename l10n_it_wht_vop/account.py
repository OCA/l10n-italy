# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2014 L.S. Advanced Software srl (<http://www.lsweb.it>)
#    Copyright (C) 2014 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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
from openerp.tools.translate import _


class account_voucher(orm.Model):
    _inherit = "account.voucher"

    """
                            dr  cr
    bank                        30.6
    IVA credito             6.60
    acquisti                30
    ritenute da versare         6


    acquisti                    30
    IVA sospesa                 6.60
    debiti                  36.60

    5.52 + 25.08 = 30.6
    25.08 / 30.6  = 0.82
    6 * 0.82 = 4.92
    25.08 + 4.92 = 30

    """

    def distribute_withholding_amount(
        self, cr, uid, move_lines, wh_amount, line_type='debit'
    ):
        lines = []
        for v_line in move_lines:
            if eval("v_line." + line_type):
                lines.append(v_line)
        total_lines = 0
        for line in lines:
            total_lines += eval("line." + line_type)
        for line in lines:
            new_amount = (
                (
                    (eval("line." + line_type) / total_lines)
                    * wh_amount
                )
                + eval("line." + line_type)
                )
            line.write({
                line_type: new_amount,
                }, update_check=False)
        return True

    def action_move_line_create(self, cr, uid, ids, context=None):
        res = super(account_voucher, self).action_move_line_create(
            cr, uid, ids, context)
        for voucher in self.browse(cr, uid, ids, context=context):
            if voucher.withholding_move_ids:
                if len(voucher.withholding_move_ids) > 1:
                    raise orm.except_orm(
                        _('Error'),
                        _("""Can't handle withholding tax + VAT on payment with
                        more than one withholding entry""")
                        )
                if len(voucher.withholding_move_ids[0].line_id) > 2:
                    raise orm.except_orm(
                        _('Error'),
                        _("""Can't handle withholding tax + VAT on payment with
                        more than two withholding items""")
                        )
                wh_move = voucher.withholding_move_ids[0]
                reconciled = False
                for move_line in wh_move.line_id:
                    if move_line.reconcile_id:
                        reconciled = True
                        break
                if reconciled:
                    wh_amount = 0
                    for move_line in wh_move.line_id:
                        if (
                            move_line.account_id.id
                            == voucher.company_id.withholding_account_id.id
                        ):
                            move_line.write({
                                'move_id': voucher.move_id.id,
                                }, update_check=False)
                            wh_amount = move_line.credit
                        else:
                            move_line.write({
                                'move_id': voucher.shadow_move_id.id,
                                }, update_check=False)
                    self.distribute_withholding_amount(
                        cr, uid, voucher.move_ids, wh_amount,
                        line_type='debit')
                    self.distribute_withholding_amount(
                        cr, uid, voucher.shadow_move_id.line_id, wh_amount,
                        line_type='credit')
                    super(account_voucher, self).balance_move(
                        cr, uid, voucher.move_id.id, context)
                    super(account_voucher, self).balance_move(
                        cr, uid, voucher.shadow_move_id.id, context)

                    if voucher.withholding_move_ids[0].amount != 0:
                        raise orm.except_orm(
                            _('Error'),
                            _('Withholding entry should have amount = 0'))
                    voucher.withholding_move_ids[0].unlink()
        return res
