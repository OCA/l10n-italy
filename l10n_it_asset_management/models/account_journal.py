# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.ondelete(
        at_uninstall=False,
    )
    def _unlink_except_in_asset_category(self):
        if (
            self.env["asset.category"]
            .sudo()
            .search(
                [
                    ("journal_id", "in", self.ids),
                ]
            )
        ):
            raise UserError(
                _(
                    "Cannot delete journals while they're still used"
                    " by asset categories."
                )
            )
