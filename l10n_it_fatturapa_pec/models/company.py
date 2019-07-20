# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    e_invoice_user_id = fields.Many2one(
        "res.users", "E-invoice creator",
        help="This user will be used at supplier e-invoice creation.",
        default=lambda self: self.env.user.id
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    e_invoice_user_id = fields.Many2one(
        related='company_id.e_invoice_user_id',
        string="Supplier e-invoice creator",
        help="This user will be used at supplier e-invoice creation. "
             "This setting is relevant in multi-company environments",
        readonly=False
    )

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.e_invoice_user_id = (
                company.e_invoice_user_id and
                company.e_invoice_user_id.id or False
            )
        else:
            self.e_invoice_user_id = False
        return res
