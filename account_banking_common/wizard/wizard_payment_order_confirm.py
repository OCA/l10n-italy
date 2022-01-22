#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


class WizardPaymentOrderConfirm(models.TransientModel):
    _name = 'wizard.payment.order.confirm'
    _description = 'Create confirm payment wizard from due dates tree view'

    def _set_default_mode(self):
        active_ids = self._context.get('active_ids')

        payment_order = False

        if len(active_ids) > 0:
            lines = self.env['account.move.line'].browse(active_ids)
            for line in lines:
                payment_order = line.payment_order
                break

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
    def registra_incasso(self):
        model = self.env['account.move.line']
        recordset = model.browse(self._context['active_ids'])
        recordset.with_context({
            'expenses_account_id': self.account_expense.id,
            'expenses_amount': self.amount_expense,
        }).registra_incasso()

        return {'type': 'ir.actions.act_window_close'}

