# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict
from datetime import timedelta

from odoo import api, models
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import format_date
from odoo.tools.float_utils import float_compare, float_is_zero

# Analytic distribution not set in journal item values
NO_ANALYTIC = "no_analytic"


class AssetDepreciation(models.Model):
    _inherit = "asset.depreciation"

    def _get_interim_fiscal_year(self, interim_date):
        self.ensure_one()
        return self.env["account.fiscal.year"].get_fiscal_year_by_date(
            interim_date, company=self.company_id
        )

    def _needs_previous_depreciation(self, interim_date):
        """Whether the fiscal year before `interim_date` is not depreciated yet."""
        self.ensure_one()
        fiscal_year = self._get_interim_fiscal_year(interim_date)
        previous_year_end = fiscal_year.date_from - timedelta(days=1)
        if self.date_start > previous_year_end:
            return False
        zero_dep_date = self.zero_depreciation_until
        if zero_dep_date and zero_dep_date >= previous_year_end:
            return False
        last_dep_date = self.last_depreciation_date
        return not last_dep_date or last_dep_date < previous_year_end

    def get_interim_depreciation_amount(self, interim_date):
        """Depreciation of the fiscal year of `interim_date`, until that date.

        It is the depreciation that the previsional report computes
        at `interim_date`, with pro rata temporis forced until that date
        (see `get_depreciation_amount_multiplier`).
        Depreciation lines of the same fiscal year
        until `interim_date` are subtracted.
        """
        self.ensure_one()
        zero_dep_date = self.zero_depreciation_until
        if zero_dep_date and interim_date <= zero_dep_date:
            return 0
        if self.date_start > interim_date:
            return 0

        asset = self.l10n_it_asset_id
        dep = self.with_context(
            force_prorata=True,
            passed_fiscal_years=self.env["account.fiscal.year"]._get_passed_years(
                asset.purchase_date, interim_date
            ),
            used_asset=asset.used,
        )
        amount = dep.get_depreciable_amount(
            interim_date
        ) * dep.get_depreciation_amount_multiplier(interim_date)

        fiscal_year = self._get_interim_fiscal_year(interim_date)
        amount -= sum(
            line.amount
            for line in self.line_ids
            if line.move_type == "depreciated"
            and not line.partial_dismissal
            and fiscal_year.date_from <= line.date <= interim_date
        )
        digits = self.env["decimal.precision"].precision_get("Account")
        amount = round(amount, digits)
        if float_compare(amount, 0, precision_digits=digits) <= 0:
            return 0
        if float_compare(self.amount_residual, amount, precision_digits=digits) < 0:
            amount = self.amount_residual
        return 0 if float_is_zero(amount, precision_digits=digits) else amount

    def get_interim_account_move_line_vals(self, interim_date):
        """Journal items of the interim depreciation of this depreciation.

        They are the journal items that a depreciation line would have,
        so that accounts (and other values, e.g. analytic) are the same.
        """
        self.ensure_one()
        amount = self.get_interim_depreciation_amount(interim_date)
        if not amount:
            return []
        line = self.env["asset.depreciation.line"].new(
            {
                "amount": amount,
                "date": interim_date,
                "depreciation_id": self.id,
                "move_type": "depreciated",
                "name": self.env._("Interim depreciation"),
            }
        )
        return line.get_depreciated_account_move_line_vals()

    def _get_interim_depreciations(self, interim_date, company):
        return self.filtered(
            lambda dep: dep.company_id == company
            and dep.requires_account_move
            and (
                not dep.last_depreciation_date
                or dep.last_depreciation_date < interim_date
            )
        )

    def get_interim_account_move_vals(self, interim_date, journal):
        """Values of the interim entry of these depreciations,
        with journal items grouped by account and analytic distribution."""
        balances = defaultdict(float)
        for dep in self:
            for vals in dep.get_interim_account_move_line_vals(interim_date):
                if "analytic_distribution" in vals:
                    distribution = vals["analytic_distribution"]
                    analytic_key = tuple(sorted((distribution or {}).items()))
                else:
                    analytic_key = NO_ANALYTIC
                key = (vals["account_id"], vals.get("currency_id"), analytic_key)
                balances[key] += vals["debit"] - vals["credit"]

        name = self.env._(
            "Interim depreciation at %(date)s",
            date=format_date(self.env, interim_date),
        )
        currency = journal.company_id.currency_id
        line_vals_list = []
        for (account_id, currency_id, analytic_key), balance in balances.items():
            if currency.is_zero(balance):
                continue
            line_vals = {
                "account_id": account_id,
                "credit": -balance if balance < 0 else 0.0,
                "currency_id": currency_id,
                "debit": balance if balance > 0 else 0.0,
                "name": name,
            }
            if analytic_key != NO_ANALYTIC:
                line_vals["analytic_distribution"] = dict(analytic_key) or False
            line_vals_list.append(line_vals)
        return {
            "company_id": journal.company_id.id,
            "date": interim_date,
            "journal_id": journal.id,
            "line_ids": [Command.create(vals) for vals in line_vals_list],
            "move_type": "entry",
            "ref": name,
        }

    def create_interim_moves(self, interim_date, journal, reversal_date):
        """Create and post the interim depreciation entry of these depreciations
        at `interim_date`, and its reversal at `reversal_date`.

        Only depreciations of the company of `journal`
        that require journal entries are considered.
        """
        if not journal:
            raise UserError(self.env._("Choose a journal for interim depreciations."))
        if not interim_date:
            raise UserError(self.env._("Choose a date for interim depreciations."))
        if not reversal_date or reversal_date <= interim_date:
            raise UserError(
                self.env._(
                    "The reversal date must be later than the depreciation date."
                )
            )
        depreciations = self._get_interim_depreciations(
            interim_date, journal.company_id
        )
        not_depreciated = depreciations.filtered(
            lambda dep: dep._needs_previous_depreciation(interim_date)
        )
        if not_depreciated:
            raise UserError(
                self.env._(
                    "Depreciate the previous fiscal year before the interim"
                    " depreciation:\n%(depreciations)s",
                    depreciations="\n".join(not_depreciated.mapped("display_name")),
                )
            )

        move_vals = depreciations.get_interim_account_move_vals(interim_date, journal)
        if not move_vals["line_ids"]:
            raise UserError(self.env._("There is nothing to depreciate."))
        move = self.env["account.move"].create(move_vals)
        move.action_post()
        reversal = move._reverse_moves(
            [
                {
                    "date": reversal_date,
                    "ref": self.env._(
                        "Reversal of: %(ref)s",
                        ref=move.ref,
                    ),
                }
            ]
        )
        reversal.action_post()
        return move | reversal

    @api.model
    def get_interim_moves_action(self, moves):
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Interim Depreciation"),
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", moves.ids)],
        }
