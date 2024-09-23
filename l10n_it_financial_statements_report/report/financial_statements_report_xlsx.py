# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models
from odoo.tools import get_lang
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)


def order_currency_amount(curr, val):
    """Orders currency symbol and amount according to currency position"""
    if curr.position == "before":
        order = (curr.symbol, val)
    else:
        order = (val, curr.symbol)
    return order


def _extract_financial_statements_report_columns(columns, mode):
    return {
        col_index: col_values
        for col_index, col_values in columns.items()
        if mode in col_values["financial_statements_report_mode"]
    }


def _get_columns_offset(cols, mode):
    if mode == "left":
        offset = 0
    elif mode == "right":
        offset = len(cols)
    else:
        raise NotImplementedError()
    return offset


class FinancialStatementsReportXslx(models.AbstractModel):
    _name = "report.l10n_it_financial_statements_report.report_xlsx"
    _description = "Financial Statements XLSX Report"
    _inherit = "report.account_financial_report.abstract_report_xlsx"

    def _define_formats(self, workbook, report_data):
        """Defines new formats"""
        res = super()._define_formats(workbook, report_data)
        company_id = report_data.get("company_id")
        if company_id is not None:
            company = self.env["res.company"].browse(company_id)
            currency = company.currency_id
        else:
            currency = self.env["res.company"]._default_currency_id()
        report_data["financial_statements_report_currency"] = currency
        report_data["formats"]["format_amount_right"] = report_data["formats"][
            "format_amount"
        ]
        report_data["formats"]["format_amount_right"].set_align("right")
        report_data["formats"]["format_amount_bold_right"] = report_data["formats"][
            "format_amount_bold"
        ]
        report_data["formats"]["format_amount_bold_right"].set_align("right")
        # '#875a7b' is Odoo default purple color
        report_data["formats"]["format_title"] = workbook.add_format(
            {
                "align": "center",
                "bg_color": "#337AB7",
                "bold": True,
                "border": True,
                "font_color": "white",
                "font_size": 16,
            }
        )
        report_data["formats"]["format_filter_title"] = workbook.add_format(
            {
                "bg_color": "#337AB7",
                "bold": True,
                "border": True,
                "font_color": "white",
            }
        )
        report_data["formats"]["format_filter_value"] = workbook.add_format(
            {
                "bg_color": "#337AB7",
                "border": True,
                "font_color": "white",
            }
        )
        # Change background and font color for header formats
        report_data["formats"]["format_header_center"].set_bg_color("#337AB7")
        report_data["formats"]["format_header_center"].set_font_color("#FFFFFF")
        report_data["formats"]["format_header_right"].set_bg_color("#337AB7")
        report_data["formats"]["format_header_right"].set_font_color("#FFFFFF")
        report_data["formats"]["format_header_amount_right"] = report_data["formats"][
            "format_header_right"
        ]
        report_data["formats"]["format_header_amount_right"].set_num_format(
            "#,##0." + "0" * currency.decimal_places
        )
        return res

    def _get_report_name(self, report, data=False):
        """
        * Overrides standard method *
        Returns name for both sheet and report title
        """
        rep_type = data.get("financial_statements_report_type")
        cols = (
            self.env["report.l10n_it_financial_statements_report.report"]
            .get_column_data()
            .get(rep_type)
        )
        title = cols["title"]
        return self._get_report_complete_name(report, title, data=data)

    def _get_report_filters(self, report):
        """
        * Overrides standard method *.
        Creates a list of 2-elements tuples: [(title, value), ...]
        """
        date_from = report.date_from.strftime("%d-%m-%Y")
        date_to = report.date_to.strftime("%d-%m-%Y")
        return [
            (
                _("Date range filter"),
                _(
                    "From: %(from_)s To: %(to)s",
                    from_=date_from,
                    to=date_to,
                ),
            ),
            (
                _("Target moves filter"),
                _("All posted entries")
                if report.target_move == "posted"
                else _("All entries"),
            ),
            (
                _("Account at 0 filter"),
                _("Hide") if report.hide_account_at_0 else _("Show"),
            ),
            (
                _("Show foreign currency"),
                _("Yes") if report.foreign_currency else _("No"),
            ),
            (
                _("Limit hierarchy levels"),
                _("Level %s", report.show_hierarchy_level)
                if report.limit_hierarchy_level
                else _("No limit"),
            ),
        ]

    def _get_report_columns(self, report):
        """
        * Overrides standard method *.
        This method defines the report columns and their data, and assigns
        such info to attributes left_columns and right_columns

        :param report: the obj to be printed
        :return: columns as dict
        """
        cols = {
            0: {
                "field": "code",
                "header": _("Code"),
                "indent_field": "level",
                "indent_unit": 2,
                "width": 20,
            },
            1: {
                "field": "name",
                "header": _("Account"),
                "indent_field": "level",
                "indent_unit": 2,
                "width": 60,
            },
            2: {
                "field": "ending_balance",
                "header": _("Final balance"),
                "type": "amount",
                "width": 20,
            },
        }
        if report.foreign_currency:
            cols.update(
                {
                    3: {
                        "field": "currency_id",
                        "field_currency_balance": "currency_id",
                        "header": _("Cur."),
                        "type": "many2one",
                        "width": 10,
                    },
                    4: {
                        "field": "ending_balance_foreign_currency",
                        "header": _("Ending balance in cur."),
                        "type": "amount_currency",
                        "width": 20,
                    },
                }
            )

        left_columns, right_columns = self.set_lr_cols(cols)
        if report.show_partner_details:
            left_columns, right_columns = self.set_partner_columns(
                cols, left_columns, right_columns
            )
        return {**left_columns, **right_columns}

    def set_lr_cols(self, cols):
        """Takes 'cols' as a template for column info, sets L/R columns"""
        left_columns = self.generate_section_cols(cols, "left")
        right_columns = self.generate_section_cols(cols, "right")
        return left_columns, right_columns

    def generate_section_cols(self, cols, mode):
        """Takes 'cols' as a template for column info, returns L/R column"""
        section_cols = cols.copy()
        offset = _get_columns_offset(cols, mode)
        section_cols = {k + offset: v.copy() for k, v in section_cols.items()}
        for col_values in section_cols.values():
            col_values["financial_statements_report_mode"] = ("section", mode)
        return section_cols

    def set_partner_columns(self, cols, left_columns, right_columns):
        left_partner_columns = self.generate_partner_columns(cols, "left", left_columns)
        right_partner_columns = self.generate_partner_columns(
            cols, "right", right_columns
        )
        return left_partner_columns, right_partner_columns

    def generate_partner_columns(self, cols, mode, columns):
        """Partner Columns are ordinary Columns but with 'Partner' after Account."""
        partner_col = {
            "field": "partner_id",
            "header": _("Partner"),
            "type": "many2one",
            "width": 60,
        }

        partner_columns = []
        for column in columns.values():
            partner_columns.append(column.copy())
            if column["field"] == "name":
                # Inject partner after Account ("name") Column
                partner_columns.append(partner_col)

        # Reassign column indexes
        offset = _get_columns_offset(partner_columns, mode)
        partner_cols = {}
        for col_index, col_values in enumerate(partner_columns):
            col_values["financial_statements_report_mode"] = ("partner", mode)
            partner_cols[offset + col_index] = col_values
        return partner_cols

    def _write_report_title(self, title, report_data):
        """
        * Overrides standard method *
        Writes report title on current line using all defined columns width
        """
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            0,
            report_data["row_pos"],
            len(report_data["columns"]) - 1,
            title,
            report_data["formats"]["format_title"],
        )
        report_data["row_pos"] += 3

    def _write_filters(self, filters, report_data):
        """
        * Overrides standard method *
        Writes filter info
        """
        title_format = report_data["formats"]["format_filter_title"]
        value_format = report_data["formats"]["format_filter_value"]
        for title, value in filters:
            report_data["sheet"].write_string(
                report_data["row_pos"], 0, title, title_format
            )
            report_data["sheet"].write_string(
                report_data["row_pos"], 1, value, value_format
            )
            report_data["row_pos"] += 1
        report_data["row_pos"] += 1

    def _generate_report_content(self, workbook, report, data, report_data):
        """Creates actual xls report

        :param workbook: The XLSX file where to write
        :param report: The wizard record
        :param data: data passed from the wizard to the report
        :param report_data: formats, ...
        """
        report_result = self.env[
            "report.l10n_it_financial_statements_report.report"
        ]._get_report_values(report, data)

        rep_type = data.get("financial_statements_report_type")
        cols = (
            self.env["report.l10n_it_financial_statements_report.report"]
            .get_column_data()
            .get(rep_type)
        )
        report_data["financial_statements_report_cols"] = cols

        self.write_main_headers(report_data)
        self.write_sub_headers(report_data)
        self.generate_table(report, report_data, report_result)
        self.write_sections_balance(report, data, report_data, report_result)
        self.write_total_balance(report, data, report_data, report_result)

    def write_main_headers(self, report_data):
        """Writes main left and right section names"""
        left_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "left"
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(left_columns.keys()),
            report_data["row_pos"],
            max(left_columns.keys()),
            report_data["financial_statements_report_cols"]["left"]["name"],
            report_data["formats"]["format_header_center"],
        )
        right_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "right"
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(right_columns.keys()),
            report_data["row_pos"],
            max(right_columns.keys()),
            report_data["financial_statements_report_cols"]["right"]["name"],
            report_data["formats"]["format_header_center"],
        )
        report_data["row_pos"] += 1

    def write_sub_headers(self, report_data):
        """Writes single headers names"""
        row, style = (
            report_data["row_pos"],
            report_data["formats"]["format_header_center"],
        )
        for col, val_dict in report_data["columns"].items():
            value = val_dict.get("header", "")
            report_data["sheet"].write_string(row, col, value, style)
        report_data["row_pos"] += 1

    def generate_table(self, report, report_data, report_result):
        """Creates the table"""
        left_lines = self.get_report_lines(
            "section_debit_ids", report, report_data, report_result
        )
        report_data["financial_statements_report_left_lines"] = left_lines
        right_lines = self.get_report_lines(
            "section_credit_ids", report, report_data, report_result
        )
        report_data["financial_statements_report_right_lines"] = right_lines
        table = self.get_table_data(report_data)

        financial_statements_report_cols = report_data[
            "financial_statements_report_cols"
        ]

        msg = ""
        if not table.get("row"):
            msg = _(
                "Could not retrieve table datas for report '%s': no lines"
                " found to be printed.",
                financial_statements_report_cols["title"],
            )
        elif not table.get("col"):
            msg = _(
                "Could not retrieve table datas for report '%s': unknown"
                " columns to be printed.",
                financial_statements_report_cols["title"],
            )
        if msg:
            _logger.warning(msg)
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                0,
                report_data["row_pos"],
                len(report_data["columns"]) - 1,
                msg,
                report_data["formats"]["format_bold"],
            )
            report_data["row_pos"] += 2
            return

        for row in range(table["row"]["first"], table["row"]["last"] + 1):
            report_data["row_pos"] = row
            lines_info = self.get_line_info(report, report_data, report_result)
            for (_l, cell), (val, style, allow) in lines_info.items():
                col, row = cell
                if allow:
                    report_data["sheet"].write(row, col, val, style)

        report_data["row_pos"] += 2

    def get_report_lines(self, field, report, report_data, report_result, func=None):
        """
        Returns report's lines, enumerated by row, as assigned by field 'field'
        and filtered by 'func' (either a function or a dot-separated
        list of fields).
        """
        enum_lines = {}

        lines = report_result.get(field, False)
        if lines and isinstance(lines, list) and func:
            try:
                lines = list(filter(func, lines))
            except (AttributeError, KeyError, TypeError, ValueError):
                if callable(func):
                    fname = func.__name__
                    fvars = func.__code__.co_varnames
                    fvars_names = ", ".join(fvars) if fvars else ""
                    msg = _(
                        "Cannot filter lines with function "
                        "`%(function_name)s(%(function_args)s)`.",
                        function_name=fname,
                        function_args=fvars_names,
                    )
                elif isinstance(func, str):
                    msg = _("Cannot filter lines with attribute `%s`.", func)
                else:
                    msg = _("Cannot filter lines with unknown parameter.")
                _logger.info(msg)

        if lines and report.show_partner_details:
            counter = 0
            for line in lines:
                enum_lines.update({counter: line})
                counter += 1
                for partner_line in filter(func, line["report_partner_ids"]):
                    enum_lines.update({counter: partner_line})
                    counter += 1
        elif lines:
            enum_lines = dict(enumerate(lines))

        if enum_lines:
            # Shift line number to actual xls row
            enum_lines = {report_data["row_pos"] + k: v for k, v in enum_lines.items()}

        return enum_lines

    def get_table_data(self, report_data):
        table = {}
        left_lines = report_data["financial_statements_report_left_lines"]
        right_lines = report_data["financial_statements_report_right_lines"]
        rows = list(left_lines) + list(right_lines)
        left_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "left"
        )
        right_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "right"
        )
        cols = list(left_columns) + list(right_columns)
        if rows:
            table.update(
                {
                    "row": {
                        "first": min(rows),
                        "last": max(rows),
                    }
                }
            )
        if cols:
            table.update(
                {
                    "col": {
                        "first": min(cols),
                        "last": max(cols),
                    }
                }
            )
        return table

    def get_line_info(self, report, report_data, report_result, row=None):
        """Returns {col: (val, style)} for current row"""
        row = row or report_data["row_pos"]
        info = {}
        left_lines = report_data["financial_statements_report_left_lines"]
        right_lines = report_data["financial_statements_report_right_lines"]
        left, right = left_lines.get(row), right_lines.get(row)

        if left:
            cols_dict = _extract_financial_statements_report_columns(
                report_data["columns"], "left"
            )
            for c in cols_dict:
                value, style, allow = self.get_write_data(
                    left, cols_dict[c], report, report_data, report_result
                )
                info[(left["account_id"], (c, row))] = value, style, allow

        if right:
            cols_dict = _extract_financial_statements_report_columns(
                report_data["columns"], "right"
            )
            for c in cols_dict:
                value, style, allow = self.get_write_data(
                    right, cols_dict[c], report, report_data, report_result
                )
                info[(right["account_id"], (c, row))] = value, style, allow

        return info

    def get_write_data(self, line, col_dict, report, report_data, report_result):
        """Returns value and style for cell"""
        cell_type = col_dict.get("type", "string")
        field = col_dict.get("field", "")
        currency = report_data["financial_statements_report_currency"]
        decimals = currency.decimal_places

        value = line.get(field)
        if value is None:
            # Field is not a field of the line directly,
            # it might be part of its account.
            account_id = line["account_id"]
            accounts_data = report_result["accounts_data"]
            account_data = accounts_data[account_id]
            value = account_data.get(field)

        style = None
        allow = False

        if cell_type == "many2one":
            record_id = value

            if field == "partner_id":
                if record_id:
                    partners_data = report_result["partners_data"]
                    value = partners_data[record_id]["name"]
                else:
                    value = _("No partner allocated")
            else:
                value = _("Field %s not set", field)
        elif cell_type == "string":
            if line.get("group_id", False):
                style = report_data["formats"]["format_bold"]
            else:
                style = None
        elif cell_type == "amount":
            value = float_round(float(value), decimals)
            if line.get("group_id", False):
                style = report_data["formats"]["format_amount_bold_right"]
            else:
                style = report_data["formats"]["format_amount_right"]
            allow = True
        elif cell_type == "amount_currency":
            currency = (
                line.get("currency_id", False)
                or line.get("company_currency_id", False)
                or currency
            )
            decimals = currency.decimal_places
            value = float_round(float(value), decimals)
            if line.get("group_id", False):
                style = report_data["formats"]["format_amount_bold_right"]
            else:
                style = report_data["formats"]["format_amount_right"]
            allow = True

        if value:
            if (
                isinstance(value, int) or isinstance(value, float)
            ) and cell_type not in (
                "amount",
                "amount_currency",
            ):
                value = format(value, f".{decimals}f")
            if not isinstance(value, str) and cell_type not in (
                "amount",
                "amount_currency",
            ):
                value = str(value)
            indent_field, indent_unit = self.get_indent_data(line, col_dict)
            if (
                report["show_hierarchy"]
                and indent_field
                and indent_unit
                and hasattr(line, indent_field)
            ):
                indent = " " * line.get(indent_field, 0) * indent_unit
                value = indent + value
            allow = True

        if allow and isinstance(value, float) and float_is_zero(value, decimals):
            value = format(value, f".{decimals}f")

        return value, style, allow

    def format_value_by_lang(self, lang, value=None, decimals=None):
        """Mimics `res.lang` model's `format` method"""
        percent = f"%.{decimals or 2}f"
        value = value or 0
        return lang.format(percent, value, grouping=True, monetary=True)

    def get_indent_data(self, line=None, col_dict=None):
        return col_dict.get("indent_field"), col_dict.get("indent_unit")

    def write_sections_balance(self, report, data, report_data, report_result):
        """Writes balances rows for left and right sections"""
        lang_code = data["account_financial_report_lang"]
        lang = get_lang(self.env, lang_code=lang_code)
        currency = report_data["financial_statements_report_currency"]
        decimals = currency.decimal_places
        credit = self.format_value_by_lang(
            lang, report_result["total_credit"], decimals
        )
        credit_data = order_currency_amount(currency, credit)
        debit = self.format_value_by_lang(lang, report_result["total_debit"], decimals)
        debit_data = order_currency_amount(currency, debit)

        left_str = _(
            "%(column)s BALANCE: %(curr_or_amount)s %(amount_or_curr)s",
            column=report_data["financial_statements_report_cols"]["left"]["name"],
            curr_or_amount=debit_data[0],
            amount_or_curr=debit_data[1],
        )
        left_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "left"
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(left_columns.keys()),
            report_data["row_pos"],
            max(left_columns.keys()),
            left_str,
            report_data["formats"]["format_header_right"],
        )

        right_str = _(
            "%(column)s BALANCE: %(curr_or_amount)s %(amount_or_curr)s",
            column=report_data["financial_statements_report_cols"]["right"]["name"],
            curr_or_amount=credit_data[0],
            amount_or_curr=credit_data[1],
        )
        right_columns = _extract_financial_statements_report_columns(
            report_data["columns"], "right"
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(right_columns.keys()),
            report_data["row_pos"],
            max(right_columns.keys()),
            right_str,
            report_data["formats"]["format_header_right"],
        )

        report_data["row_pos"] += 1

    def write_total_balance(self, report, data, report_data, report_result):
        """Writes total balance row"""
        lang_code = data["account_financial_report_lang"]
        lang = get_lang(self.env, lang_code=lang_code)
        currency = report_data["financial_statements_report_currency"]
        decimals = currency.decimal_places
        balance = self.format_value_by_lang(
            lang, report_result["total_balance"], decimals
        )
        total_credit = report_result["total_credit"]
        total_debit = report_result["total_debit"]
        surplus = float_compare(total_credit, total_debit, decimals) == 1
        deficit = float_compare(total_credit, total_debit, decimals) == -1
        if surplus or deficit:
            title = _("SURPLUS") if surplus else _("DEFICIT")
            bal_data = order_currency_amount(currency, balance)
            balance_str = f"{title}: {bal_data[0]} {bal_data[1]}"
            left_columns = _extract_financial_statements_report_columns(
                report_data["columns"], "left"
            )
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                min(left_columns.keys()),
                report_data["row_pos"],
                max(left_columns.keys()),
                balance_str if surplus else "",
                report_data["formats"]["format_header_amount_right"],
            )
            right_columns = _extract_financial_statements_report_columns(
                report_data["columns"], "right"
            )
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                min(right_columns.keys()),
                report_data["row_pos"],
                max(right_columns.keys()),
                balance_str if deficit else "",
                report_data["formats"]["format_header_amount_right"],
            )
            report_data["row_pos"] += 1
