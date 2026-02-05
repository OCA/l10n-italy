# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import fields, models
from odoo.exceptions import ValidationError


def format_date(rec, field_name, fmt):
    """Formats record's field value according to given format `fmt`"""
    if not rec[field_name]:
        return ""
    return rec._fields[field_name].from_string(rec[field_name]).strftime(fmt)


class ReportAssetSituation(models.TransientModel):
    """
    This report has the following structure:
        * Report (which is just a data container)
        ** Category
        *** Asset
        **** Depreciation
    Each class is set to be linked via a M2O to its parent class, and via
    a O2M to its child class.
    Each class is linked to Report via `report_id` field.
    """

    _name = "report.asset.situation"
    _description = "Report Asset Situation"
    _inherit = "report.account_financial_report.abstract_report"

    # Data fields
    date = fields.Date()

    l10n_it_asset_ids = fields.Many2many(
        "asset.asset",
    )

    depreciation_ids = fields.Many2many(
        "asset.depreciation",
    )

    category_ids = fields.Many2many(
        "asset.category",
    )

    company_id = fields.Many2one(
        "res.company",
    )

    show_totals = fields.Boolean()

    show_category_totals = fields.Boolean()
    show_sold_assets = fields.Boolean()
    show_dismissed_assets = fields.Boolean()

    type_ids = fields.Many2many(
        "asset.depreciation.type",
    )

    purchase_date_from = fields.Date()
    purchase_date_to = fields.Date()

    # Report structure fields
    report_category_ids = fields.One2many(
        "report.asset.situation.category", "report_id"
    )

    report_total_ids = fields.One2many("report.asset.situation.totals", "report_id")

    # Fields to be printed
    report_name = fields.Char()

    ############################
    #                          #
    # REPORT RENDERING METHODS #
    #                          #
    ############################

    def print_report(self, report_type=None):
        """
        This method is called from the JS widget buttons 'Print'
        and 'Export' in the HTML view.
        Prints PDF and XLSX reports.
        :param report_type: string that represents the report type
        """
        self.ensure_one()
        report_type = report_type or "qweb-pdf"
        if report_type in ("qweb-pdf", "xlsx", "qweb-html"):
            res = self.do_print(report_type)
        elif report_type:
            raise ValidationError(
                self.env._("Report type %s is not supported.", report_type)
            )
        else:
            res = False
        return res

    def do_print(self, report_type):
        self.ensure_one()
        if report_type == "xlsx":
            report_name = "l10n_it_asset_management.report_asset_situation_xlsx"
        elif report_type == "qweb-html":
            report_name = "l10n_it_asset_management.report_asset_situation_html"
        else:
            report_name = "l10n_it_asset_management.report_asset_situation_pdf"

        return (
            self.env["ir.actions.report"]
            .search([("report_name", "=", report_name)], limit=1)
            .report_action(self, config=False)
        )

    def compute_data_for_report(self):
        self.ensure_one()
        self._inject_category_values()
        if self.show_totals:
            self._inject_totals_values()

    def _inject_category_values(self):
        """Create category sections with their assets and depreciations"""
        categories_data = OrderedDict()

        # Group depreciations by category
        for depreciation in self.depreciation_ids:
            asset = depreciation.l10n_it_asset_id
            category = asset.category_id

            if category not in categories_data:
                categories_data[category] = {
                    "category": category,
                    "depreciations": [],
                }

            categories_data[category]["depreciations"].append(
                {
                    "depreciation": depreciation,
                    "asset": asset,
                }
            )

        # Create report records
        for category_data in categories_data.values():
            self._create_category_section(category_data)

    def _create_category_section(self, category_data):
        """Create a category section with its data"""
        category = category_data["category"]

        # Calculate category totals
        total_depreciable = sum(
            d["depreciation"].amount_depreciable_updated
            for d in category_data["depreciations"]
        )
        total_depreciated = sum(
            d["depreciation"].amount_depreciated for d in category_data["depreciations"]
        )
        total_residual = sum(
            d["depreciation"].amount_residual for d in category_data["depreciations"]
        )

        # Create category record
        category_vals = {
            "report_id": self.id,
            "category_id": category.id,
            "category_name": category.name,
            "total_amount_depreciable_updated": total_depreciable,
            "total_amount_depreciated": total_depreciated,
            "total_amount_residual": total_residual,
        }

        category_record = self.env["report.asset.situation.category"].create(
            category_vals
        )

        # Create asset depreciation lines
        for dep_data in category_data["depreciations"]:
            depreciation = dep_data["depreciation"]
            asset = dep_data["asset"]

            line_vals = {
                "report_id": self.id,
                "category_id": category_record.id,
                "asset_id": asset.id,
                "asset_name": asset.make_name(),
                "depreciation_id": depreciation.id,
                "depreciation_type": depreciation.type_id.name,
                "amount_depreciable_updated": depreciation.amount_depreciable_updated,
                "amount_depreciated": depreciation.amount_depreciated,
                "amount_residual": depreciation.amount_residual,
                "last_depreciation_date": depreciation.last_depreciation_date,
                "purchase_date": asset.purchase_date,
                "dismissed": asset.dismissed,
                "sold": asset.sold,
            }

            self.env["report.asset.situation.line"].create(line_vals)

    def _inject_totals_values(self):
        """Create general totals"""
        total_depreciable = sum(
            self.report_category_ids.mapped("total_amount_depreciable_updated")
        )
        total_depreciated = sum(
            self.report_category_ids.mapped("total_amount_depreciated")
        )
        total_residual = sum(self.report_category_ids.mapped("total_amount_residual"))

        totals_vals = {
            "report_id": self.id,
            "total_amount_depreciable_updated": total_depreciable,
            "total_amount_depreciated": total_depreciated,
            "total_amount_residual": total_residual,
        }

        self.env["report.asset.situation.totals"].create(totals_vals)


class ReportAssetSituationCategory(models.TransientModel):
    _name = "report.asset.situation.category"
    _description = "Asset Situation Report Category"

    report_id = fields.Many2one(
        "report.asset.situation",
        required=True,
        ondelete="cascade",
    )

    category_id = fields.Many2one("asset.category")
    category_name = fields.Char()

    line_ids = fields.One2many(
        "report.asset.situation.line",
        "category_id",
    )

    total_amount_depreciable_updated = fields.Monetary(
        currency_field="currency_id",
    )
    total_amount_depreciated = fields.Monetary(
        currency_field="currency_id",
    )
    total_amount_residual = fields.Monetary(
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        related="report_id.company_id.currency_id",
    )


class ReportAssetSituationLine(models.TransientModel):
    _name = "report.asset.situation.line"
    _description = "Asset Situation Report Line"

    report_id = fields.Many2one(
        "report.asset.situation",
        required=True,
        ondelete="cascade",
    )

    category_id = fields.Many2one(
        "report.asset.situation.category",
        required=True,
        ondelete="cascade",
    )

    asset_id = fields.Many2one("asset.asset")
    asset_name = fields.Char()

    depreciation_id = fields.Many2one("asset.depreciation")
    depreciation_type = fields.Char()

    amount_depreciable_updated = fields.Monetary(
        string="Depreciable Amount",
        currency_field="currency_id",
    )
    amount_depreciated = fields.Monetary(
        string="Depreciated Amount",
        currency_field="currency_id",
    )
    amount_residual = fields.Monetary(
        string="Residual Amount",
        currency_field="currency_id",
    )
    last_depreciation_date = fields.Date(
        string="Last Depreciation Date",
    )

    purchase_date = fields.Date()
    dismissed = fields.Boolean()
    sold = fields.Boolean()

    currency_id = fields.Many2one(
        "res.currency",
        related="report_id.company_id.currency_id",
    )


class ReportAssetSituationTotals(models.TransientModel):
    _name = "report.asset.situation.totals"
    _description = "Asset Situation Report Totals"

    report_id = fields.Many2one(
        "report.asset.situation",
        required=True,
        ondelete="cascade",
    )

    total_amount_depreciable_updated = fields.Monetary(
        currency_field="currency_id",
    )
    total_amount_depreciated = fields.Monetary(
        currency_field="currency_id",
    )
    total_amount_residual = fields.Monetary(
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        related="report_id.company_id.currency_id",
    )
