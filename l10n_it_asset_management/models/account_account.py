# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.ondelete(
        at_uninstall=False,
    )
    def _unlink_except_in_asset_category(self):
        if (
            self.env["asset.category"]
            .sudo()
            .search(
                [
                    "|",
                    "|",
                    "|",
                    "|",
                    ("asset_account_id", "in", self.ids),
                    ("depreciation_account_id", "in", self.ids),
                    ("fund_account_id", "in", self.ids),
                    ("gain_account_id", "in", self.ids),
                    ("loss_account_id", "in", self.ids),
                ]
            )
        ):
            raise UserError(
                _(
                    "Cannot delete accounts while they're still used"
                    " by asset categories."
                )
            )
