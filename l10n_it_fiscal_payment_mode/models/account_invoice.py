# -*- coding: utf-8 -*-

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def _compute_fatturapa_pm_id(self):
        if self.payment_mode_id and self.payment_mode_id.fatturapa_pm_id:
            self.fatturapa_pm_id = self.payment_mode_id.fatturapa_pm_id
        else:
            super(AccountInvoice, self)._compute_fatturapa_pm_id()
