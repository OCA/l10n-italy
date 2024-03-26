#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging

from odoo import models, api, fields

from ..utils import domains

_logger = logging.getLogger(__name__)


class WizardInsoluto(models.TransientModel):
    
    _name = 'wizard.account.banking.common.insoluto'
    _description = 'Gestione insoluti'

    expenses_account = fields.Many2one(
        'account.account',
        string='Conto Spese',
        domain=lambda self: domains.get_bank_expenses_account(self.env),
    )
    
    expenses_amount = fields.Float(string='Importo spese')
    
    charge_client = fields.Boolean(
        string='Addebito spese a cliente',
        default=False,
    )
    
    @api.multi
    def registra_insoluto(self):
        '''Create on new account.move for each line of insoluto'''
        ids = self._context['active_ids']
        model = self.env['account.move.line']
        recordset = model.browse(ids)
        recordset.with_context({
            'expenses_account_id': self.expenses_account.id,
            'expenses_amount': self.expenses_amount,
            'charge_client': self.charge_client,
        }).registra_insoluto()
    # end registra_insoluto
    
