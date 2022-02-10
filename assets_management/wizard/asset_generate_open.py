# Copyright 2021-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2021-22 Didotech s.r.l. <https://www.didotech.com>
# Copyright 2021-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
from odoo import api, fields, models, _


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
        self.ensure_one()
        asset = self.get_asset()
        am_obj = self.env['account.move']
        vals = {
            'company_id': self.company_id.id,
            'date': asset.purchase_date,
            'journal_id': asset.category_id.journal_id.id,
            'line_ids': [],
            'ref': _("Apertura Bene: ") + asset.make_name(),
        }

        credit_line_vals = {
            'account_id': self.account_id.id,
            'credit': self.amount,
            'debit': 0.0,
            'currency_id': self.currency_id.id,
            'name': " - ".join((asset.make_name(), asset.name)),
        }
        debit_line_vals = {
            'account_id': asset.category_id.asset_account_id.id,
            'credit': 0.0,
            'debit': self.amount,
            'currency_id': self.currency_id.id,
            'name': " - ".join((asset.make_name(), asset.name)),
        }

        for v in [credit_line_vals, debit_line_vals]:
            vals['line_ids'].append((0, 0, v))

        asset.move_id = am_obj.create(vals)

        asset.is_open = True

        return {
                'type': 'ir.actions.client',
                'tag': 'reload'
            }
