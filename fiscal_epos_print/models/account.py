# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    fpdeptax = fields.Char(
        'Department on fiscal printer 1~99',
        size=1, default="1"
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.multi
    def write(self, vals):
        """If the move created by POS session is not balanced
        we add a line with the rounding"""
        pos_rounding = self._context.get('pos_rounding', False)
        all_lines = vals.get('line_ids', False)

        if not (pos_rounding and all_lines):
            return super(AccountMove, self).write(vals)

        currency = self.env.user.company_id.currency_id

        for move in self:
            total_credit = \
                currency.round(sum(x[2]['credit'] for x in all_lines))
            total_debit = currency.round(sum(x[2]['debit'] for x in all_lines))
            unbalance = total_debit - total_credit
            # if the move is not balanced we add a rounding
            if unbalance:
                all_lines.append((0, 0, {
                    'name': _("Rounding"),
                    'quantity': 1,
                    'account_id': move.company_id.transfer_account_id.id,
                    'credit': ((unbalance > 0) and unbalance) or 0.0,
                    'debit': ((unbalance < 0) and -unbalance) or 0.0,
                }))
            vals['line_ids'] = all_lines

        return super(AccountMove, self).write(vals)
