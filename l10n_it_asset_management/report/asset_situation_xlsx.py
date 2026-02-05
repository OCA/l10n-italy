# Copyright 2026 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AssetSituationXlsx(models.AbstractModel):
    _name = "report.l10n_it_asset_management.report_asset_situation_xlsx"
    _description = "Report Asset Situation Xlsx"
    _inherit = "report.account_financial_report.abstract_report_xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        """Set wb, data and report attributes"""
        # Initialize report variables
        report_data = {
            "workbook": None,
            "sheet": None,
            "columns": None,
            "row_pos": None,
            "formats": None,
        }
        report_name = self._get_report_name(objects, data=data)
        report_data["workbook"] = workbook
        report_data["sheet"] = workbook.add_worksheet(report_name[:31])
        report_data["row_pos"] = 0
        self._define_formats(workbook, report_data)
        self.set_formats(workbook, report_data)
        self.set_report_data(report_data)

        # Get report data
        report_footer = self._get_report_footer()
        filters = self._get_report_filters(objects)
        report_data["columns"] = self._get_report_columns(objects)
        self._set_column_width(report_data)

        # Fill report
        self._write_report_title(report_name, report_data)
        self._write_filters(filters, report_data)
        self._generate_report_content(workbook, objects, data, report_data)
        self._write_report_footer(report_footer, report_data)

    def set_formats(self, workbook, report_data):
        """Defines custom formats"""

        # Category formats
        report_data["formats"]["format_category_header"] = workbook.add_format(
            {
                "align": "center",
                "bg_color": "#337AB7",
                "bold": True,
                "font_color": "#FFFFFF",
                "font_size": 14,
            }
        )

        # Header formats
        report_data["formats"]["format_header_left"] = workbook.add_format(
            {
                "align": "left",
                "bold": True,
                "border": 1,
            }
        )

        report_data["formats"]["format_header_center"] = workbook.add_format(
            {
                "align": "center",
                "bold": True,
                "border": 1,
            }
        )

        report_data["formats"]["format_header_right"] = workbook.add_format(
            {
                "align": "right",
                "bold": True,
                "border": 1,
            }
        )

        # Data formats
        report_data["formats"]["format_data_left"] = workbook.add_format(
            {
                "align": "left",
                "border": 1,
            }
        )

        report_data["formats"]["format_data_center"] = workbook.add_format(
            {
                "align": "center",
                "border": 1,
            }
        )

        report_data["formats"]["format_data_amount"] = workbook.add_format(
            {
                "align": "right",
                "border": 1,
                "num_format": "#,##0.00",
            }
        )

        # Total formats
        report_data["formats"]["format_total_label"] = workbook.add_format(
            {
                "align": "left",
                "bold": True,
                "bg_color": "#E0E0E0",
                "border": 1,
            }
        )

        report_data["formats"]["format_total_amount"] = workbook.add_format(
            {
                "align": "right",
                "bold": True,
                "bg_color": "#E0E0E0",
                "border": 1,
                "num_format": "#,##0.00",
            }
        )

    def _get_report_name(self, objects, data=None):
        return objects.report_name if objects else "Situazione Cespiti"

    def _get_report_footer(self):
        return ""

    def _get_report_filters(self, objects):
        filters = []
        obj = objects[0] if objects else None
        if not obj:
            return filters

        if obj.purchase_date_from:
            filters.append(
                f"Purchase Date From: {obj.purchase_date_from.strftime('%d/%m/%Y')}"
            )

        if obj.purchase_date_to:
            filters.append(
                f"Purchase Date To: {obj.purchase_date_to.strftime('%d/%m/%Y')}"
            )

        if obj.show_dismissed_assets:
            filters.append("Including Dismissed Assets")

        if obj.show_sold_assets:
            filters.append("Including Sold Assets")

        return filters

    def _get_report_columns(self, objects):
        return {
            0: {
                "header": "Asset Name",
                "field": "asset_name",
                "width": 40,
            },
            1: {
                "header": "Depreciation Type",
                "field": "depreciation_type",
                "width": 20,
            },
            2: {
                "header": "Depreciable Amount",
                "field": "amount_depreciable_updated",
                "type": "amount",
                "width": 18,
            },
            3: {
                "header": "Depreciated Amount",
                "field": "amount_depreciated",
                "type": "amount",
                "width": 18,
            },
            4: {
                "header": "Residual Amount",
                "field": "amount_residual",
                "type": "amount",
                "width": 18,
            },
            5: {
                "header": "Last Depreciation Date",
                "field": "last_depreciation_date",
                "type": "date",
                "width": 18,
            },
        }

    def _generate_report_content(self, workbook, objects, data, report_data):
        obj = objects[0] if objects else None
        if not obj:
            return

        # Write column headers
        self._write_column_headers(report_data)

        # Write data by category
        for category in obj.report_category_ids:
            self._write_category_section(category, report_data)

        # Write general totals
        if obj.show_totals and obj.report_total_ids:
            self._write_totals(obj.report_total_ids[0], report_data)

    def _write_column_headers(self, report_data):
        """Write the column headers"""
        row_pos = report_data["row_pos"]
        sheet = report_data["sheet"]

        for col_pos, column in report_data["columns"].items():
            sheet.write(
                row_pos,
                col_pos,
                column["header"],
                report_data["formats"]["format_header_center"],
            )

        report_data["row_pos"] += 1

    def _write_category_section(self, category, report_data):
        """Write a category section with its lines"""
        row_pos = report_data["row_pos"]
        sheet = report_data["sheet"]

        # Write category header
        sheet.merge_range(
            row_pos,
            0,
            row_pos,
            len(report_data["columns"]) - 1,
            category.category_name,
            report_data["formats"]["format_category_header"],
        )
        report_data["row_pos"] += 1

        # Write category lines
        for line in category.line_ids:
            self._write_line(line, report_data)

        # Write category totals if enabled
        if category.report_id.show_category_totals:
            self._write_category_totals(category, report_data)

        report_data["row_pos"] += 1

    def _write_line(self, line, report_data):
        """Write a single asset line"""
        row_pos = report_data["row_pos"]
        sheet = report_data["sheet"]

        sheet.write(
            row_pos,
            0,
            line.asset_name,
            report_data["formats"]["format_data_left"],
        )
        sheet.write(
            row_pos,
            1,
            line.depreciation_type or "",
            report_data["formats"]["format_data_center"],
        )
        sheet.write(
            row_pos,
            2,
            line.amount_depreciable_updated,
            report_data["formats"]["format_data_amount"],
        )
        sheet.write(
            row_pos,
            3,
            line.amount_depreciated,
            report_data["formats"]["format_data_amount"],
        )
        sheet.write(
            row_pos,
            4,
            line.amount_residual,
            report_data["formats"]["format_data_amount"],
        )
        sheet.write(
            row_pos,
            5,
            line.last_depreciation_date.strftime("%d/%m/%Y")
            if line.last_depreciation_date
            else "",
            report_data["formats"]["format_data_center"],
        )

        report_data["row_pos"] += 1

    def _write_category_totals(self, category, report_data):
        """Write category totals"""
        row_pos = report_data["row_pos"]
        sheet = report_data["sheet"]

        sheet.write(
            row_pos,
            0,
            f"Total {category.category_name}",
            report_data["formats"]["format_total_label"],
        )
        sheet.write(
            row_pos,
            1,
            "",
            report_data["formats"]["format_total_label"],
        )
        sheet.write(
            row_pos,
            2,
            category.total_amount_depreciable_updated,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            3,
            category.total_amount_depreciated,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            4,
            category.total_amount_residual,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            5,
            "",
            report_data["formats"]["format_total_label"],
        )

        report_data["row_pos"] += 1

    def _write_totals(self, totals, report_data):
        """Write general totals"""
        row_pos = report_data["row_pos"]
        sheet = report_data["sheet"]

        report_data["row_pos"] += 1
        row_pos = report_data["row_pos"]

        sheet.write(
            row_pos,
            0,
            "GENERAL TOTALS",
            report_data["formats"]["format_total_label"],
        )
        sheet.write(
            row_pos,
            1,
            "",
            report_data["formats"]["format_total_label"],
        )
        sheet.write(
            row_pos,
            2,
            totals.total_amount_depreciable_updated,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            3,
            totals.total_amount_depreciated,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            4,
            totals.total_amount_residual,
            report_data["formats"]["format_total_amount"],
        )
        sheet.write(
            row_pos,
            5,
            "",
            report_data["formats"]["format_total_label"],
        )

        report_data["row_pos"] += 1
