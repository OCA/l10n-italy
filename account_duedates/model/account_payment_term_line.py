#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

from dateutil.relativedelta import relativedelta
from odoo import models, api, fields


class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"

    @api.model
    def compute_due_date(self, date_ref=False):
        date_ref = date_ref or fields.Date.today()
        next_date = fields.Date.from_string(date_ref)
        if self.option == 'day_after_invoice_date':
            next_date += relativedelta(days=self.days)
            if self.day_of_the_month > 0:
                months_delta = (self.day_of_the_month < next_date.day) \
                               and 1 or 0
                next_date += relativedelta(day=self.day_of_the_month,
                                           months=months_delta)
        elif self.option == 'after_invoice_month':
            next_first_date = next_date + relativedelta(day=1, months=1)
            next_date = next_first_date + relativedelta(days=self.days - 1)
        elif self.option == 'day_following_month':
            next_date += relativedelta(day=self.days, months=1)
        elif self.option == 'day_current_month':
            next_date += relativedelta(day=self.days, months=0)

        result = {
            'due_date': next_date,
            'credit': self.payment_method_credit,
            'debit': self.payment_method_debit,
        }
        return result
