#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import fields, models, api
from odoo.exceptions import UserError


class AccountPaymentMethod(models.Model):
    _inherit = 'account.payment.method'

    debit_credit = fields.Selection(
        string='Debit / Credit',
        selection=[
            ('credit', 'Credit'),
            ('debit', 'Debit'),
        ],
        default=''
    )

    @api.model
    def get_payment_method_tax(self):
        res = self.search([('code', '=', 'tax')])

        if not res:
            raise UserError("'tax' payment method not found!")

        return res[0]
