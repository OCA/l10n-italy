#  -*- coding: utf-8 -*-
#  Copyright 2019 Simone Rubino - Agile Business Group

from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class AccountMoveReversal(models.TransientModel):
    """
    Account move reversal wizard, it cancel an account move by reversing it.
    """
    _inherit = 'account.move.reversal'


    def reverse_moves(self):
        res = super(AccountMoveReversal, self).reverse_moves()
        if isinstance(res, dict):
            if self.refund_method == 'modify':
                invoice_ids_domain = ('id', 'in', [res['res_id']])
            else:
                invoice_ids_domain = res['domain'][-1] if 'domain' in res else ('id', 'in', [res['res_id']])
            invoices = self.env['account.move'].search([invoice_ids_domain])
            if all(not inv.corrispettivo for inv in invoices):
                return res

            # Some of the created refunds are corrispettivi:
            # show the corrispettivi tree view
            # corr_action = self.env.ref(
            #     'l10n_it_corrispettivi.action_corrispettivi_tree1').read()[0]
            # corr_domain = safe_eval(corr_action['domain'])
            # corr_domain.append(invoice_ids_domain)
            # corr_action['domain'] = corr_domain
            # return corr_action
        return res
