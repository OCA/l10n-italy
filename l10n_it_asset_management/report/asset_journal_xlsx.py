# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class AssetJournalXslx(models.AbstractModel):
    _name = "report.l10n_it_asset_management.report_asset_journal_xlsx"
    _description = "Report Asset Journal Xlsx"
    _inherit = "report.account_financial_report.abstract_report_xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        """Set wb, data and report attributes"""
        # Initialize report variables
        report_data = {
            "workbook": None,
            "sheet": None,  # main sheet which will contains report
            "columns": None,  # columns of the report
            "row_pos": None,  # row_pos must be incremented at each writing lines
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

        # 1- Category formats

        report_data["formats"]["format_category_name"] = workbook.add_format(
            {
                "align": "center",
                "bg_color": "#337AB7",
                "bold": True,
                "font_color": "#FFFFFF",
                "font_size": 16,
            }
        )

        # 2- Asset formats

        report_data["formats"]["format_asset_header"] = workbook.add_format(
            {
                "align": "center",
                "bold": True,
                "font_color": "#337AB7",
                "font_size": 14,
            }
        )

        report_data["formats"]["format_asset_value"] = workbook.add_format(
            {
                "align": "center",
                "font_color": "#337AB7",
                "font_size": 14,
            }
        )

        # 3- Depreciations formats

        report_data["formats"]["format_depreciation_header"] = workbook.add_format(
            {
                "align": "center",
                "bold": True,
                "font_size": 12,
            }
        )

        report_data["formats"]["format_depreciation_value"] = workbook.add_format(
            {
                "align": "center",
                "font_size": 12,
            }
        )

        # 4- Depreciation yearly and amount details formats

        report_data["formats"][
            "format_depreciation_year_line_header"
        ] = workbook.add_format(
            {
                "align": "center",
                "bold": True,
                "font_size": 12,
            }
        )

        report_data["formats"][
            "format_depreciation_year_line_value_center"
        ] = workbook.add_format(
            {
                "align": "center",
                "font_size": 12,
            }
        )

        report_data["formats"][
            "format_depreciation_year_line_value_right"
        ] = workbook.add_format(
            {
                "align": "right",
                "font_size": 12,
            }
        )

        # 5- Report title
        report_data["formats"]["format_title"] = workbook.add_format(
            {
                "align": "center",
                "bg_color": "#337AB7",
                "bold": True,
                "font_color": "white",
                "font_size": 20,
            }
        )

    def set_report_data(self, report_data):
        self.set_category_data(report_data)
        self.set_asset_data(report_data)
        self.set_asset_accounting_doc_data(report_data)
        self.set_depreciation_data(report_data)
        self.set_depreciation_line_year_data(report_data)
        self.set_depreciation_line_amount_detail_data(report_data)
        self.set_depreciation_line_accounting_doc_data(report_data)
        self.set_totals_data(report_data)

    def set_category_data(self, report_data):
        report_data["category_data"] = self.generate_category_data(report_data)

    def generate_category_data(self, report_data):
        data = (
            {
                "title": _("Category"),
                "field": "category_name",
                "tstyle": report_data["formats"]["format_category_name"],
                "vstyle": report_data["formats"]["format_category_name"],
            },
        )
        return dict(enumerate(data))

    def set_asset_data(self, report_data):
        report_data["asset_data"] = self.generate_asset_data(report_data)

    def generate_asset_data(self, report_data):
        data = (
            {
                "title": _("Asset"),
                "field": "asset_name",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Code"),
                "field": "asset_code",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Purchase Amount"),
                "field": "asset_purchase_amount",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Purchased as New / Used"),
                "field": "asset_used",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Status"),
                "field": "asset_state",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
        )
        return dict(enumerate(data))

    def set_asset_accounting_doc_data(self, report_data):
        report_data[
            "asset_accounting_doc_data"
        ] = self.generate_asset_accounting_doc_data(report_data)

    def generate_asset_accounting_doc_data(self, report_data):
        data = (
            {
                "title": _("Partner"),
                "field": "partner_name",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("VAT"),
                "field": "partner_vat",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Document Nr"),
                "field": "document_nr",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Document Date"),
                "field": "document_date",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Supplier Ref"),
                "field": "partner_ref",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_data(self, report_data):
        report_data["depreciation_data"] = self.generate_depreciation_data(report_data)

    def generate_depreciation_data(self, report_data):
        data = (
            {
                "title": _("Depreciation Type"),
                "field": "type_name",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
            {
                "title": _("Depreciation Mode"),
                "field": "mode_name",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
            {
                "title": _("Initial Depreciable Amount"),
                "field": "dep_amount_depreciable",
                "type": "amount",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
            {
                "title": _("Starting From"),
                "field": "dep_date_start",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
            {
                "title": _("Dep. Percentage (%)"),
                "field": "dep_percentage",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
            {
                "title": _("Pro Rata Temporis"),
                "field": "dep_pro_rata_temporis",
                "tstyle": report_data["formats"]["format_depreciation_header"],
                "vstyle": report_data["formats"]["format_depreciation_value"],
            },
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_line_year_data(self, report_data):
        report_data[
            "depreciation_line_year_data"
        ] = self.generate_depreciation_line_year_data(report_data)

    def generate_depreciation_line_year_data(self, report_data):
        formatd = report_data["formats"]
        data = (
            {
                "title": _("Year"),
                "field": "year",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("Amount"),
                "field": "amount_depreciable_updated",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("In Amount"),
                "field": "amount_in",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Out Amount"),
                "field": "amount_out",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Prev. Year Dep. Fund"),
                "field": "amount_depreciation_fund_prev_year",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Depreciation"),
                "field": "amount_depreciated",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Curr. Year Dep. Fund"),
                "field": "amount_depreciation_fund_curr_year",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Gain / Loss"),
                "field": "gain_loss",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
            {
                "title": _("Residual"),
                "field": "amount_residual",
                "type": "amount",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_right"],
            },
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_line_amount_detail_data(self, report_data):
        report_data[
            "depreciation_line_amount_detail_data"
        ] = self.generate_depreciation_line_amount_detail_data(report_data)

    def generate_depreciation_line_amount_detail_data(self, report_data):
        formatd = report_data["formats"]
        data = (
            {
                "title": _("In Amount - Detail"),
                "field": "amount_in_detail",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("Out Amount - Detail"),
                "field": "amount_out_detail",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
        )
        return {n + 3: d for n, d in enumerate(data)}

    def set_depreciation_line_accounting_doc_data(self, report_data):
        report_data[
            "depreciation_line_accounting_doc_data"
        ] = self.generate_depreciation_line_accounting_doc_data(report_data)

    def generate_depreciation_line_accounting_doc_data(self, report_data):
        formatd = report_data["formats"]
        data = (
            {
                "title": _("Partner"),
                "field": "partner_name",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("VAT"),
                "field": "partner_vat",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("Document Nr"),
                "field": "document_nr",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("Document Date"),
                "field": "document_date",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
            {
                "title": _("Supplier Ref"),
                "field": "partner_ref",
                "tstyle": formatd["format_depreciation_year_line_header"],
                "vstyle": formatd["format_depreciation_year_line_value_center"],
            },
        )
        return {n + 3: d for n, d in enumerate(data)}

    def set_totals_data(self, report_data):
        report_data["totals_data"] = self.get_totals_data(report_data)

    def get_totals_data(self, report_data):
        data = (
            {
                "title": _("Total"),
                "field": "name",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Type"),
                "field": "type_name",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Amount"),
                "field": "amount_depreciable_updated",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("In Amount"),
                "field": "amount_in_total",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Out Amount"),
                "field": "amount_out_total",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Prev. Year Dep. Fund"),
                "field": "amount_depreciation_fund_prev_year",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Depreciation"),
                "field": "amount_depreciated",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Curr. Year Dep. Fund"),
                "field": "amount_depreciation_fund_curr_year",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Gain / Loss"),
                "field": "gain_loss_total",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
            {
                "title": _("Residual"),
                "field": "amount_residual",
                "type": "amount",
                "tstyle": report_data["formats"]["format_asset_header"],
                "vstyle": report_data["formats"]["format_asset_value"],
            },
        )
        return {n: d for n, d in enumerate(data)}

    def _set_column_width(self, report_data):
        """Override to force every column to width 25 at least"""
        max_width = self.get_max_width_dict(report_data)
        for col, width in max_width.items():
            report_data["sheet"].set_column(col, col, max(width, 25))

    def get_max_width_dict(self, report_data):
        min_col = min(
            [
                min(report_data["category_data"].keys()),
                min(report_data["asset_data"].keys()),
                min(report_data["asset_accounting_doc_data"].keys()),
                min(report_data["depreciation_data"].keys()),
                min(report_data["depreciation_line_year_data"].keys()),
                min(report_data["depreciation_line_amount_detail_data"].keys()),
                min(report_data["depreciation_line_accounting_doc_data"].keys()),
                min(report_data["totals_data"].keys()),
            ]
        )
        max_col = max(
            [
                max(report_data["category_data"].keys()),
                max(report_data["asset_data"].keys()),
                max(report_data["asset_accounting_doc_data"].keys()),
                max(report_data["depreciation_data"].keys()),
                max(report_data["depreciation_line_year_data"].keys()),
                max(report_data["depreciation_line_amount_detail_data"].keys()),
                max(report_data["depreciation_line_accounting_doc_data"].keys()),
                max(report_data["totals_data"].keys()),
            ]
        )

        return {
            col: max(
                [
                    report_data["category_data"].get(col, {}).get("width") or 0,
                    report_data["asset_data"].get(col, {}).get("width") or 0,
                    report_data["asset_accounting_doc_data"].get(col, {}).get("width")
                    or 0,
                    report_data["depreciation_data"].get(col, {}).get("width") or 0,
                    report_data["depreciation_line_year_data"].get(col, {}).get("width")
                    or 0,
                    report_data["depreciation_line_amount_detail_data"]
                    .get(col, {})
                    .get("width")
                    or 0,
                    report_data["depreciation_line_accounting_doc_data"]
                    .get(col, {})
                    .get("width")
                    or 0,
                    report_data["totals_data"].get(col, {}).get("width") or 0,
                ]
            )
            for col in range(min_col, max_col + 1)
        }

    def _get_report_name(self, report, data=False):
        report_name = _("Asset Journal")
        return self._get_report_complete_name(report, report_name)

    def _write_report_title(self, title, report_data):
        """
        * Overrides standard method *
        Writes report title on current line using all defined columns width
        """
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            0,
            report_data["row_pos"] + 1,
            9,
            title,
            report_data["formats"]["format_title"],
        )
        report_data["row_pos"] += 5

    def _generate_report_content(self, workbook, objects, data, report_data):
        """Creates actual xls report"""
        report = objects
        for categ_section in report.report_category_ids:
            self.write_all(report_data, categ_section, "category_data")

            for asset_section in categ_section.report_asset_ids:
                self.write_all(report_data, asset_section, "asset_data")

                if asset_section.report_purchase_doc_id:
                    self.write_all(
                        report_data,
                        asset_section.report_purchase_doc_id,
                        "asset_accounting_doc_data",
                    )

                for dep_section in asset_section.report_depreciation_ids:
                    self.write_all(report_data, dep_section, "depreciation_data")

                    self.write_header(report_data, "depreciation_line_year_data")
                    for year in dep_section.report_depreciation_year_line_ids:
                        self.write_value(
                            report_data, year, "depreciation_line_year_data"
                        )
                        if year.has_amount_detail:
                            self.write_value(
                                report_data,
                                year,
                                "depreciation_line_amount_detail_data",
                            )
                        for doc in year.report_accounting_doc_ids:
                            self.write_value(
                                report_data,
                                doc,
                                "depreciation_line_accounting_doc_data",
                            )

                if asset_section.report_sale_doc_id:
                    self.write_all(
                        report_data,
                        asset_section.report_sale_doc_id,
                        "asset_accounting_doc_data",
                    )
                report_data["row_pos"] += 1

            if report.show_category_totals:
                self.write_header(report_data, "totals_data")
                for total_section in categ_section.report_total_ids:
                    self.write_value(report_data, total_section, "totals_data")
                report_data["row_pos"] += 1

            report_data["row_pos"] += 1

        if report.show_totals:
            self.write_header(report_data, "totals_data")
            for total_section in report.report_total_ids:
                self.write_value(report_data, total_section, "totals_data")
            report_data["row_pos"] += 1

    def _define_formats(self, workbook, report_data):
        """Add cell formats to current workbook.
        Those formats can be used on all cell.
        Available formats are :
         * format_bold
         * format_right
         * format_right_bold_italic
         * format_header_left
         * format_header_center
         * format_header_right
         * format_header_amount
         * format_amount
         * format_percent_bold_italic
        """
        currency_id = self.env["res.company"]._default_currency_id()
        report_data["formats"] = {
            "format_bold": workbook.add_format({"bold": True}),
            "format_right": workbook.add_format({"align": "right"}),
            "format_left": workbook.add_format({"align": "left"}),
            "format_right_bold_italic": workbook.add_format(
                {"align": "right", "bold": True, "italic": True}
            ),
            "format_header_left": workbook.add_format(
                {"bold": True, "border": True, "bg_color": "#FFFFCC"}
            ),
            "format_header_center": workbook.add_format(
                {"bold": True, "align": "center", "border": True, "bg_color": "#FFFFCC"}
            ),
            "format_header_right": workbook.add_format(
                {"bold": True, "align": "right", "border": True, "bg_color": "#FFFFCC"}
            ),
            "format_header_amount": workbook.add_format(
                {"bold": True, "border": True, "bg_color": "#FFFFCC"}
            ),
            "format_amount": workbook.add_format(),
            "format_amount_bold": workbook.add_format({"bold": True}).set_num_format(
                "#,##0." + "0" * currency_id.decimal_places
            ),
            "format_percent_bold_italic": workbook.add_format(
                {"bold": True, "italic": True}
            ),
        }
        report_data["formats"]["format_amount"].set_num_format(
            "#,##0." + "0" * currency_id.decimal_places
        )
        report_data["formats"]["format_header_amount"].set_num_format(
            "#,##0." + "0" * currency_id.decimal_places
        )
        report_data["formats"]["format_percent_bold_italic"].set_num_format("#,##0.00%")

    def write_all(self, report_data, obj, index):
        self.write_header(report_data, index)
        self.write_value(report_data, obj, index)

    def write_header(self, report_data, index):
        pos = report_data["row_pos"]
        for col, data in report_data[index].items():
            report_data["sheet"].write(pos, col, data["title"], data["tstyle"])
        report_data["row_pos"] += 1

    def write_value(self, report_data, obj, index):
        pos = report_data["row_pos"]
        for col, data in report_data[index].items():
            value, style = getattr(obj, data["field"]), data["vstyle"]
            if data.get("type") == "amount":
                value = obj.format_amount(value)
            if value in (False, None):
                value = "/"
            report_data["sheet"].write(pos, col, value, style)
        report_data["row_pos"] += 1

    ########################################################
    #                                                      #
    # UNUSED METHODS, OVERRIDDEN FOR COMPATIBILITY REASONS #
    #                                                      #
    ########################################################

    def _get_report_filters(self, report):
        """Override original method even if not used to avoid errors"""
        return []

    def _get_report_columns(self, report):
        """Override original method even if not used to avoid errors"""
        return {}

    def _get_col_count_filter_name(self):
        """Override original method even if not used to avoid errors"""

    def _get_col_count_filter_value(self):
        """Override original method even if not used to avoid errors"""

    def _write_filters(self, filters, data):
        """Override original method even if not used to avoid errors"""
