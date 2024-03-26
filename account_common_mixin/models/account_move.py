#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import models, api
from .mixin_base import BaseMixin


class AccountMove(models.Model, BaseMixin):
    _inherit = 'account.move'

    @api.multi
    def post(self, invoice=False):
        for move in self:
            if invoice:
                move.company_bank_id = invoice.company_bank_id
                move.counterparty_bank_id = invoice.counterparty_bank_id
        return super().post(invoice=invoice)

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

    @api.multi
    def adapt_document(self):

        self.ensure_one()

        p_t_id = self.payment_term_id
        c_id = self.company_id
        c_banks = c_id and c_id.partner_id.bank_ids

        adapted_doc = {
            'model': 'account.move',
            'type': self.type,

            # Payment infos
            'fatturapa_pm_id': p_t_id and p_t_id.fatturapa_pm_id,
            'payment_mode_id': None,  # payment_mode_id does not exist in move

            # Default banks
            'default_company_bank': c_banks and c_banks[0],
        }

        # Update with counterparty data
        counterparty_bank_infos = self.partner_id.bank_infos()
        adapted_doc.update(counterparty_bank_infos)

        return adapted_doc
    # end adapt_document

    @api.multi
    def _get_doc_type(self):
        self.ensure_one()
        return self.type
    # end _get_doc_type
