# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def unlink(self):
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
        return super().unlink()
