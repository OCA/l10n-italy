#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class WizardPaymentOrderCredit(models.TransientModel):
    _name = 'wizard.payment.order.credit'

    def _set_default_mode(self):

        payment_order = self.env['account.payment.order'].browse(
            self._context.get('active_id'))

        if payment_order and payment_order.id:
            cfg = payment_order.get_move_config()
            if 'conto_spese_bancarie' in cfg and cfg['conto_spese_bancarie'].id:
                return cfg['conto_spese_bancarie'].id
        return False

    account_expense = fields.Many2one(
        'account.account',
        string='Conto spese',
        domain=[(
            'internal_group', '=', 'expense')],
        default=_set_default_mode
    )

    amount_expense = fields.Float(string='Importo', )

    @api.multi
    def registra_accredito(self):
        '''Create on new account.move for each line of payment order'''

        model = self.env['account.payment.order']
        recordset = model.browse(self._context['active_id'])
        recordset.with_context({
            'expenses_account_id': self.account_expense.id,
            'expenses_amount': self.amount_expense,
        }).registra_accredito()

        return {'type': 'ir.actions.act_window_close'}

    # end registra_accredito

