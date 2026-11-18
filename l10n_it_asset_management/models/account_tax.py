# Copyright 2026 Luca Orioli <lucaorioli@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _prepare_base_line_tax_repartition_grouping_key(
        self, base_line, base_line_grouping_key, tax_data, tax_rep_data
    ):
        """Keep taxes charged to an asset account on a tax line for each line.

        A tax repartition line without account charges the tax to the account
        of the base line, e.g. for non deductible VAT. When that is an asset
        account, the tax is part of the cost of the asset of that line: the key
        of the line keeps it on its own tax line, as different analytic
        distributions do, so that each asset gets its own amount.
        """
        grouping_key = super()._prepare_base_line_tax_repartition_grouping_key(
            base_line, base_line_grouping_key, tax_data, tax_rep_data
        )
        asset_tax_key = False
        record = base_line.get("record")
        if (
            isinstance(record, models.BaseModel)
            and record._name == "account.move.line"
            and grouping_key["account_id"] == base_line_grouping_key["account_id"]
        ):
            asset_tax_key = record.l10n_it_asset_tax_key
        grouping_key["l10n_it_asset_tax_key"] = asset_tax_key or False
        return grouping_key

    @api.model
    def _prepare_tax_line_repartition_grouping_key(self, tax_line):
        grouping_key = super()._prepare_tax_line_repartition_grouping_key(tax_line)
        asset_tax_key = False
        record = tax_line.get("record")
        if isinstance(record, models.BaseModel) and record._name == "account.move.line":
            asset_tax_key = record.l10n_it_asset_tax_key
        grouping_key["l10n_it_asset_tax_key"] = asset_tax_key or False
        return grouping_key
