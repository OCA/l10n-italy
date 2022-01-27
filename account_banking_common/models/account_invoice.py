#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models
from odoo.addons.account_common_mixin.models.mixin_base import BaseMixin


class AccountInvoice(models.Model, BaseMixin):
    _inherit = "account.invoice"

    # override settings of the field
    # adding open state to modification
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Bank Account',
        readonly=True,
        states={'draft': [('readonly', False)], 'open': [('readonly', False)]},
    )

    company_partner_id = fields.Many2one(
        'res.partner',
        related='company_id.partner_id',
        string='Company partner',
        readonly=True,
        store=False,
    )

    @api.onchange('partner_bank_id', 'partner_id')
    def onchange_partner_bank_id(self):
        current_domain = [('bank_is_wallet', '=', False)]
        if self.type in ('out_invoice', 'out_refund'):
            current_domain.append(('partner_id', '=', self.company_id.partner_id.id))
        elif self.type in ('in_invoice', 'in_refund'):
            in_domain = list()
            in_domain.append('|')
            in_domain.append(('partner_id', '=', self.company_id.partner_id.id)),
            in_domain.append(('partner_id', '=', self.partner_id.id)),
            current_domain += in_domain
        # end if
        return {'domain': {'partner_bank_id': current_domain}}

    # end onchange_partner_bank_id

    def write(self, vals):
        if 'partner_bank_id' in vals:
            if self.state == 'open':
                self.move_id.write({
                        'partner_bank_id': vals['partner_bank_id']
                })
            # end if
        # end if
        # if 'company_bank_id' in vals:
        #     if self.state == 'open':
        #         self.move_id.write({
        #                 'company_bank_id': vals['company_bank_id'],
        #                 # 'bank_2_print_selector': 'company',
        #         })
        #     # end if
        # # end if
        # if 'counterparty_bank_id' in vals:
        #     if self.state == 'open':
        #         self.move_id.write({
        #                 'counterparty_bank_id': vals['counterparty_bank_id'],
        #                 # 'bank_2_print_selector': 'partner',
        #         })
        #     # end if
        # # end if

        return super().write(vals)
    # end write

