# Copyright 2022 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountGroup(models.Model):
    _inherit = "account.group"

    account_ids = fields.One2many(
        comodel_name="account.account",
        inverse_name="group_id",
        string="Accounts",
    )
    account_balance_sign = fields.Integer(
        compute="_compute_account_balance_sign",
        string="Balance sign",
    )

    @api.constrains("account_ids", "parent_id")
    def check_balance_sign_coherence(self):
        """
        Checks whether every group (plus parents and subgroups) have the same
        balance sign. This is done by first retrieving every group's progenitor
        and then checking, for each of them, the account types' for accounts
        linked to such progenitor group and its subgroups.
        """
        if self.env.context.get("skip_check_balance_sign_coherence"):
            return
        done_group_ids, progenitor_ids = [], []
        for group in self:
            if group.id in done_group_ids:
                continue
            progenitor = group.get_group_progenitor()
            progenitor_ids.extend(progenitor.ids)
            done_group_ids.extend(progenitor.get_group_subgroups().ids)

        progenitors = self.browse(tuple(set(progenitor_ids)))
        for progenitor in progenitors:
            accounts = progenitor.get_group_accounts()
            if not accounts.have_same_sign():
                raise ValidationError(
                    _("Incoherent balance signs for '{}' and its subgroups.").format(
                        progenitor.name_get()[0][-1]
                    )
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
