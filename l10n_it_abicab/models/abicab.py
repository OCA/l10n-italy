# -*- coding: utf-8 -*-
# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Davide Corio (Abstract)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResBank(models.Model):

    _inherit = "res.bank"

    abi = fields.Char(size=5, string='ABI')
    cab = fields.Char(size=5, string='CAB')


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    bank_abi = fields.Char(size=5, string='ABI')
    bank_cab = fields.Char(size=5, string='CAB')

    @api.onchange('bank_id')
    def onchange_bank_id(self):
        if self.bank_id:
            self.bank_abi = self.bank_id.abi
            self.bank_cab = self.bank_id.cab
