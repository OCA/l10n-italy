# -*- coding: utf-8 -*-
# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountConfigSettings(models.TransientModel):

    _inherit = 'account.config.settings'

    due_cost_service_id = fields.Many2one(
        related='company_id.due_cost_service_id',
        help='Default Service for RiBa Due Cost (collection fees) on invoice',
        domain=[('type', '=', 'service')])

    riba_payment_response = fields.Selection(
        [('1', 'Required'),
         ('2', 'Not Required'),
         (' ', 'Bank Agreement')],
        related='company_id.riba_payment_response',
        default=' ',
        string='Require to send back the response of the RiBa payment')

    @api.model
    def default_get(self, fields):
        res = super(AccountConfigSettings, self).default_get(fields)
        if res:
            res[
                'due_cost_service_id'
            ] = self.env.user.company_id.due_cost_service_id.id
            res[
                'riba_payment_response'
            ] = self.env.user.company_id.riba_payment_response
        return res


class ResCompany(models.Model):

    _inherit = 'res.company'

    due_cost_service_id = fields.Many2one('product.product')

    riba_payment_response = fields.Selection(
        [('1', 'Required'),
         ('2', 'Not Required'),
         (' ', 'Bank Agreement')],
        default=' ',
        string='Require to send back the response of the RiBa payment')
