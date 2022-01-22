#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def write(self, values):
        if 'company_bank_id' in values:
            lines = self.line_ids.filtered(
                lambda x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'company_bank_id': values['company_bank_id']
            })
        # end if

        if 'counterparty_bank_id' in values:
            lines = self.line_ids.filtered(
                lambda x: x.reconciled is False and x.payment_order.id is False
            )

            lines.write({
                'counterparty_bank_id': values['counterparty_bank_id']
            })
        # end if

        return super().write(values)

    # end write

