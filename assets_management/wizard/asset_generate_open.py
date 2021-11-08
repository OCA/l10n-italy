# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizardAssetsGenerateOpen(models.TransientModel):
    _name = 'wizard.asset.generate.open'
    _description = "Generate Asset Open"

    @api.model
    def get_asset(self):
        active_id = self.env.context.get('active_id')
        if not active_id:
            return False
        asset = self.env['asset.asset'].browse(active_id)
        return asset

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_asset_id(self):
        asset = self.get_asset()
        return asset.id

    @api.model
    def get_default_account_id(self):
        asset = self.get_asset()
        return asset.category_id.gain_account_id.id

    @api.model
    def get_purchase_amount(self):
        asset = self.get_asset()
        return asset.purchase_amount

    asset_id = fields.Many2one(
        'asset.asset',
        string="Asset",
        default=get_asset_id,
        readonly=True,
    )

    company_id = fields.Many2one(
        'res.company',
        default=get_default_company_id,
        string="Company",
    )

    account_id = fields.Many2one(
        'account.account',
        default=get_default_account_id,
        string="Conto di ricavo",
    )

    currency_id = fields.Many2one(
        'res.currency',
        readonly=True,
        related='asset_id.currency_id',
        string="Currency"
    )

    amount = fields.Monetary(
        string="Purchase Value",
        default=get_purchase_amount,
        readonly=True,
    )

    @api.multi
    def do_generate(self):
        active_id = self.env.context.get('active_id')

        self.ensure_one()

