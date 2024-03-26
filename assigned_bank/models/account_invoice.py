#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.partner_bank_id = False
        if (self.type in ['out_invoice','in_refund'] and
                self.partner_id and self.partner_id.customer and 
                self.partner_id.commercial_partner_id and
                self.partner_id.commercial_partner_id.assigned_income_bank):
            self.partner_bank_id = self.\
                partner_id.commercial_partner_id.assigned_income_bank.id
        return super(AccountInvoice, self)._onchange_partner_id()
