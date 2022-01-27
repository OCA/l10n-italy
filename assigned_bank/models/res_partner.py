#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _assigned_bank_set(self):
        return self.env['res.config.settings']._assigned_bank_get()

    def _assigned_income_bank_set(self):
        return self.env['res.config.settings']._assigned_income_bank_get()

    assigned_bank = fields.Many2one(
        'res.partner.bank', string='Assigned Bank for Payment',
        default=_assigned_bank_set,
        domain=lambda self:
            [('partner_id', '=', self.env.user.company_id.partner_id.id)])
    assigned_income_bank = fields.Many2one(
        'res.partner.bank', string='Assigned Bank for Incoming',
        default=_assigned_income_bank_set,
        domain=lambda self:
            [('partner_id', '=', self.env.user.company_id.partner_id.id)])
