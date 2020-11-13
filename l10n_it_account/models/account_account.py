# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class Account(models.Model):
    _inherit = "account.account"

    @api.constrains("code")
    def check_balance_sign_coherence(self):
        """
        Checks whether adding an account to (or removing it from) a group
        creates incoherencies in account groups' balance signs.
        """
        groups = self.mapped("group_id")
        # Avoid check upon empty recordset to make it faster
        if groups:
            groups.check_balance_sign_coherence()
