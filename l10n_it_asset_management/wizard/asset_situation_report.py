# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AssetSituationReportWizard(models.TransientModel):
    _name = "asset.situation.report.wizard"
    _description = "Asset Situation Report Wizard"

    date = fields.Date(
        required=True,
        default=fields.Date.context_today,
        string="Report Date",
    )

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        string="Company",
    )

    category_ids = fields.Many2many(
        "asset.category",
        string="Categories",
        help="Leave empty to include all categories",
    )

    type_ids = fields.Many2many(
        "asset.depreciation.type",
        string="Depreciation Types",
        help="Leave empty to include all types",
    )

    show_dismissed_assets = fields.Boolean(
        string="Include Dismissed Assets",
        default=False,
    )

    show_sold_assets = fields.Boolean(
        string="Include Sold Assets",
        default=False,
    )

    purchase_date_from = fields.Date(
        string="Purchase Date From",
        help="Filter assets purchased from this date",
    )

    purchase_date_to = fields.Date(
        string="Purchase Date To",
        help="Filter assets purchased until this date",
    )

    show_category_totals = fields.Boolean(
        string="Show Category Totals",
        default=True,
    )

    show_totals = fields.Boolean(
        string="Show General Totals",
        default=True,
    )

    def _prepare_report_vals(self):
        self.ensure_one()

        # Build domain for assets
        domain = [("company_id", "=", self.company_id.id)]

        if self.category_ids:
            domain.append(("category_id", "in", self.category_ids.ids))

        if not self.show_dismissed_assets:
            domain.append(("dismissed", "=", False))

        if not self.show_sold_assets:
            domain.append(("sold", "=", False))

        if self.purchase_date_from:
            domain.append(("purchase_date", ">=", self.purchase_date_from))

        if self.purchase_date_to:
            domain.append(("purchase_date", "<=", self.purchase_date_to))

        # Get assets
        assets = self.env["asset.asset"].search(domain, order="category_id, name")

        # Filter depreciations by type if specified
        if self.type_ids:
            depreciation_domain = [
                ("l10n_it_asset_id", "in", assets.ids),
                ("type_id", "in", self.type_ids.ids),
            ]
        else:
            depreciation_domain = [("l10n_it_asset_id", "in", assets.ids)]

        depreciations = self.env["asset.depreciation"].search(depreciation_domain)

        return {
            "date": self.date,
            "company_id": self.company_id.id,
            "category_ids": self.category_ids.ids or [],
            "type_ids": self.type_ids.ids or [],
            "l10n_it_asset_ids": assets.ids,
            "depreciation_ids": depreciations.ids,
            "show_dismissed_assets": self.show_dismissed_assets,
            "show_sold_assets": self.show_sold_assets,
            "show_category_totals": self.show_category_totals,
            "show_totals": self.show_totals,
            "purchase_date_from": self.purchase_date_from,
            "purchase_date_to": self.purchase_date_to,
            "report_name": self._get_report_name(),
        }

    def _get_report_name(self):
        self.ensure_one()
        return f"Situazione Cespiti al {self.date.strftime('%d/%m/%Y')}"

    def generate_report(self):
        self.ensure_one()
        report = self.env["report.asset.situation"].create(self._prepare_report_vals())
        report.compute_data_for_report()

        return {
            "type": "ir.actions.act_window",
            "name": "Situazione Cespiti",
            "res_model": "report.asset.situation",
            "res_id": report.id,
            "view_mode": "form",
            "target": "current",
        }
