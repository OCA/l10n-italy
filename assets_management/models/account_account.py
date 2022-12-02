# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountAccount(models.Model):
    _inherit = "account.account"

    def unlink(self):
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
        return super().unlink()
