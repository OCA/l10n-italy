# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountGroup(models.Model):
    _inherit = "account.group"
    account_balance_sign = fields.Integer(
        compute="_compute_account_balance_sign",
        string="Balance sign",
    )

    def _compute_account_balance_sign(self):
        for group in self:
            group.account_balance_sign = group.get_account_balance_sign()

    def get_account_balance_sign(self):
        self.ensure_one()
        progenitor = self.get_group_progenitor()
        accounts = progenitor.get_group_accounts()
        if accounts:
            return accounts[0].account_balance_sign
        return 1

    def get_group_accounts(self):
        """Retrieves every account from `self` and `self`'s subgroups."""
        return (self + self.get_group_subgroups()).mapped("account_ids")

    def get_group_progenitor(self):
        self.ensure_one()
        if not self.parent_id:
            return self
        return self.get_group_parents().filtered(lambda g: not g.parent_id)

    def get_group_parents(self):
        """
        Retrieves every parent for group `self`.
        :return: group's parents as recordset, or empty recordset if `self`
        has no parents. If a recursion is found, an error is raised.
        """
        self.ensure_one()
        parent_ids = []
        parent = self.parent_id
        while parent:
            parent_ids.append(parent.id)
            parent = parent.parent_id
        return self.browse(parent_ids)

    def get_group_subgroups(self):
        """Retrieves every subgroup for groups `self`."""
        subgroups_ids = self.search([("id", "child_of", self.ids)])
        return subgroups_ids
