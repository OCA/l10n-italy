# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    date_vat_settlement = fields.Date("VAT Settlement Date")

    @api.multi
    def action_move_create(self):
        super().action_move_create()
        for invoice in self:
            if not invoice.date_vat_settlement:
                invoice.write({"date_vat_settlement": self.date or self.date_invoice or fields.Date.context_today(self)})
            for move in invoice.move_id:
                move.write({"date_vat_settlement": invoice.date_vat_settlement})

    @api.onchange("date_vat_settlement")
    def _onchange_date_vat_settlement(self):
        for move in self.move_id:
            move.write({"date_vat_settlement": self.date_vat_settlement})

    def rc_inv_vals(self, partner, account, rc_type, lines, currency):
        ret = super().rc_inv_vals(partner, account, rc_type, lines, currency)
        ret['date_vat_settlement'] = self.date_vat_settlement
        return ret
