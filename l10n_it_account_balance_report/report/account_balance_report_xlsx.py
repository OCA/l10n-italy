# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)


def order_currency_amount(curr, val):
    """Orders currency symbol and amount according to currency position"""
    if curr.position == "before":
        order = (curr.symbol, val)
    else:
        order = (val, curr.symbol)
    return order


class AccountBalanceReportXslx(models.AbstractModel):
    _name = "report.l10n_it_a_b_r.account_balance_report_xlsx"
    _description = "XLSX account balance report"
    _inherit = "report.account_financial_report.abstract_report_xlsx"

    def _get_report_name(self, report, data=False):
        """
        * Overrides standard method *
        Returns name for both sheet and report title
        """
        return self._get_report_complete_name(report, report.title)

    def _get_report_filters(self, report):
        """
        * Overrides standard method *.
        Creates a list of 2-elements tuples: [(title, value), ...]
        """
        date_from = report.date_from.strftime("%d-%m-%Y")
        date_to = report.date_to.strftime("%d-%m-%Y")
        return [
            (_("Date range filter"), _("From: {} To: {}".format(date_from, date_to))),
            (
                _("Target moves filter"),
                _("All posted entries")
                if report.only_posted_moves
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
                _("Level %s" % report.show_hierarchy_level)
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
                "header": _("Period balance"),
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
                        "field": "final_balance_foreign_currency",
                        "header": _("Ending balance in cur."),
                        "type": "amount_currency",
                        "width": 20,
                    },
                }
            )

        left_columns, right_columns = self.set_lr_cols(cols)
        dict_columns = {"left_columns": left_columns, "right_columns": right_columns}
        dict_partner = self.set_partner_columns({**cols, **dict_columns})
        dict_partner.update(dict_columns)
        return {**left_columns, **right_columns, **dict_partner}

    def set_lr_cols(self, cols):
        """Takes 'cols' as a template for column info, sets L/R columns"""
        return self.generate_section_cols(cols, "left"), self.generate_section_cols(
            cols, "right"
        )

    def generate_section_cols(self, cols, mode):
        """Takes 'cols' as a template for column info, returns L/R column"""
        section_cols = {}
        if mode == "left":
            section_cols = cols.copy()
        elif mode == "right":
            section_cols = {k + len(cols): v for k, v in cols.items()}
        return section_cols

    def set_partner_columns(self, cols):
        return {
            "left_partner_columns": self.generate_partner_columns(cols, "left"),
            "right_partner_columns": self.generate_partner_columns(cols, "right"),
        }

    def generate_partner_columns(self, cols, mode):
        if mode == "left":
            left_partner_cols = {k: {} for k in cols["left_columns"].keys()}
            left_partner_cols.update(
                {
                    1: {"field": "partner_id", "type": "many2one", "width": 60},
                    2: {"field": "ending_balance", "type": "amount", "width": 20},
                }
            )
            return left_partner_cols
        elif mode == "right":
            right_partner_cols = {k: {} for k in cols["right_columns"].keys()}
            right_partner_cols.update(
                {
                    1
                    + len(cols): {
                        "field": "partner_id",
                        "type": "many2one",
                        "width": 60,
                    },
                    2
                    + len(cols): {
                        "field": "ending_balance",
                        "type": "amount",
                        "width": 20,
                    },
                }
            )
            return right_partner_cols
        raise NotImplementedError

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
            report_data["workbook"].add_format(
                {
                    "align": "center",
                    "bg_color": "#337AB7",
                    "bold": True,
                    "border": True,
                    "font_color": "white",
                    "font_size": 16,
                }
            ),
        )
        report_data["row_pos"] += 3

    def _write_filters(self, filters, report_data):
        """
        * Overrides standard method *
        Writes filter info
        """
        title_format = report_data["workbook"].add_format(
            {
                "bg_color": "#337AB7",
                "bold": True,
                "border": True,
                "font_color": "white",
            }
        )
        value_format = report_data["workbook"].add_format(
            {
                "bg_color": "#337AB7",
                "border": True,
                "font_color": "white",
            }
        )
        for title, value in filters:
            report_data["sheet"].write_string(
                report_data["row_pos"], 0, title, title_format
            )
            report_data["sheet"].write_string(
                report_data["row_pos"], 1, value, value_format
            )
            report_data["row_pos"] += 1
        report_data["row_pos"] += 1

    def _generate_report_content(self, workbook, objects, data, report_data):
        """Creates actual xls report"""
        self.write_main_headers(objects, report_data)
        self.write_sub_headers(report_data)
        self.generate_table(objects, report_data)
        self.write_sections_balance(objects, report_data)
        self.write_total_balance(objects, report_data)

    def write_main_headers(self, objects, report_data):
        """Writes main left and right section names"""
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(report_data["left_columns"].keys()),
            report_data["row_pos"],
            max(report_data["left_columns"].keys()),
            objects.left_col_name,
            report_data["formats"]["format_header_center"],
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(report_data["right_columns"].keys()),
            report_data["row_pos"],
            max(report_data["right_columns"].keys()),
            objects.right_col_name,
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

    def generate_table(self, objects, report_data):
        """Creates the table"""
        report = objects

        report_data["left_lines"] = self.get_report_lines(
            "section_debit_ids", objects=objects, report_data=report_data
        )
        report_data["right_lines"] = self.get_report_lines(
            "section_credit_ids", objects=objects, report_data=report_data
        )
        table = self.get_table_data(
            report_data["left_lines"], report_data["right_lines"], report_data
        )

        msg = ""
        if not table.get("row"):
            msg = _(
                "Could not retrieve table datas for report '{}': no lines"
                " found to be printed.".format(report.title)
            )
        elif not table.get("col"):
            msg = _(
                "Could not retrieve table datas for report '{}': unknown"
                " columns to be printed.".format(report.title)
            )
        if msg:
            _logger.warning(msg)
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                0,
                report_data["row_pos"],
                len(report_data["columns"]) - 1,
                msg,
                report_data["format_bold"],
            )
            report_data["row_pos"] += 2
            return

        for row in range(table["row"]["first"], table["row"]["last"] + 1):
            report_data["row_pos"] = row
            for (_l, cell), (val, style, allow) in self.get_line_info(
                objects=objects, report_data=report_data
            ).items():
                col, row = cell
                if allow:
                    report_data["sheet"].write(row, col, val, style)

        report_data["row_pos"] += 2

    def get_report_lines(self, field, func=None, objects=None, report_data=None):
        """
        Returns report's lines, enumerated by row, as assigned by field 'field'
        and filtered by 'func' (either a function or a dot-separated
        list of fields).
        """
        func = (
            func
            or self.get_default_line_filter_func(field=field, objects=objects)
            or False
        )
        enum_lines = {}
        report = objects

        lines = getattr(report, field, False)
        if lines and isinstance(lines, models.BaseModel) and func:
            try:
                lines = lines.filtered(func)
            except (AttributeError, KeyError, TypeError, ValueError):
                if callable(func):
                    fname = func.__name__
                    fvars = func.__code__.co_varnames
                    fvars_names = ", ".join(fvars) if fvars else ""
                    msg = _(
                        "Cannot filter lines with function `{}({})`.".format(
                            fname, fvars_names
                        )
                    )
                elif isinstance(func, str):
                    msg = _("Cannot filter lines with attribute `{}`.".format(func))
                else:
                    msg = _("Cannot filter lines with unknown parameter.")
                _logger.info(msg)

        if lines and report.show_partner_details:
            counter = 0
            for line in lines:
                enum_lines.update({counter: line})
                counter += 1
                for partner_line in line.report_partner_ids.filtered(func):
                    enum_lines.update({counter: partner_line})
                    counter += 1
        elif lines:
            enum_lines = dict(enumerate(lines))

        if enum_lines:
            # Shift line number to actual xls row
            enum_lines = {report_data["row_pos"] + k: v for k, v in enum_lines.items()}

        return enum_lines

    def get_default_line_filter_func(self, **kwargs):
        func = None
        field = kwargs.get("field")
        wizard = self.env["trial.balance.report.wizard"].browse(
            self.env.context["active_id"]
        )
        if wizard.hide_account_at_0 and field in (
            "section_credit_ids",
            "section_debit_ids",
        ):

            def show(line):
                return not line.hide_line

            func = show
        return func

    def get_table_data(self, left_lines=None, right_lines=None, report_data=None):
        if not left_lines:
            left_lines = report_data["left_lines"]
        if not right_lines:
            right_lines = report_data["right_lines"]
        table = {}
        rows = list(left_lines) + list(right_lines)
        cols = list(report_data["left_columns"]) + list(report_data["right_columns"])
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

    def get_line_info(self, row=None, objects=None, report_data=None):
        """Returns {col: (val, style)} for current row"""
        row = row or report_data["row_pos"]
        info = {}
        l, r = report_data["left_lines"].get(row), report_data["right_lines"].get(row)

        cols_dict = {}
        if l:
            if l._name == "account_balance_report_account":
                cols_dict = report_data["left_columns"]
            elif l._name == "account_balance_report_partner":
                cols_dict = report_data["left_partner_columns"]
            info.update(
                {
                    (l, (c, row)): self.get_write_data(
                        l, cols_dict[c], objects, report_data
                    )
                    for c in cols_dict
                    if cols_dict[c]
                }
            )

        if r:
            if r._name == "account_balance_report_account":
                cols_dict = report_data["right_columns"]
            elif r._name == "account_balance_report_partner":
                cols_dict = report_data["right_partner_columns"]
            info.update(
                {
                    (r, (c, row)): self.get_write_data(
                        r, cols_dict[c], objects, report_data
                    )
                    for c in cols_dict
                    if cols_dict[c]
                }
            )

        return info

    def get_write_data(self, line, col_dict, objects, report_data):
        """Returns value and style for cell"""
        cell_type = col_dict.get("type", "string")
        field = col_dict.get("field")
        decimals = objects.company_id.currency_id.decimal_places

        value = getattr(line, field, False)
        style = None
        allow = False

        if cell_type == "many2one":
            val_name = getattr(value, "name", "")
            val_display = getattr(value, "display_name", "")
            if val_name:
                value = val_name
            elif val_display:
                value = val_display
            elif line._name == "account_balance_report_partner":
                value = _("No partner allocated")
        elif cell_type == "string":
            if getattr(line, "account_group_id", False):
                style = self.format_bold
            else:
                style = None
        elif cell_type == "amount":
            value = float_round(float(value), decimals)
            if getattr(line, "account_group_id", False):
                style = self.format_amount_bold_right
            else:
                style = report_data["formats"]["format_amount"]
            allow = True
        elif cell_type == "amount_currency":
            currency = (
                getattr(line, "currency_id", False)
                or getattr(line, "company_currency_id", False)
                or self.currency
            )
            decimals = currency.decimal_places
            value = float_round(float(value), decimals)
            if getattr(line, "account_group_id", False):
                style = self.format_amount_bold_right
            else:
                style = report_data["formats"]["format_amount"]
            allow = True

        if value:
            if isinstance(value, (int, float)) and cell_type not in (
                "amount",
                "amount_currency",
            ):
                value = format(value, ".{}f".format(decimals))
            if not isinstance(value, str) and cell_type not in (
                "amount",
                "amount_currency",
            ):
                value = str(value)
            indent_field, indent_unit = self.get_indent_data(line, col_dict)
            if indent_field and indent_unit and hasattr(line, indent_field):
                indent = " " * getattr(line, indent_field, 0) * indent_unit
                value = indent + value
            allow = True

        if allow and isinstance(value, float) and float_is_zero(value, decimals):
            value = format(value, ".{}f".format(decimals))

        return value, style, allow

    def format_value_by_lang(self, value=None, decimals=None):
        """Mimics `res.lang` model's `format` method"""
        percent = "%.{}f".format(decimals or 2)
        value = value or 0
        return (
            self.env["res.lang"]
            ._lang_get(self.env.user.lang)
            .format(percent, value, grouping=True, monetary=True)
        )

    def get_indent_data(self, line=None, col_dict=None):
        return col_dict.get("indent_field"), col_dict.get("indent_unit")

    def write_sections_balance(self, objects, report_data):
        """Writes balances rows for left and right sections"""
        report = objects
        curr = objects.company_id.currency_id
        decimals = curr.decimal_places
        credit = self.format_value_by_lang(report.total_credit, decimals)
        credit_data = order_currency_amount(curr, credit)
        debit = self.format_value_by_lang(report.total_debit, decimals)
        debit_data = order_currency_amount(curr, debit)

        left_str = "{} BALANCE: {} {}".format(
            report.left_col_name, debit_data[0], debit_data[1]
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(report_data["left_columns"].keys()),
            report_data["row_pos"],
            max(report_data["left_columns"].keys()),
            left_str,
            report_data["formats"]["format_header_right"],
        )

        right_str = "{} BALANCE: {} {}".format(
            report.right_col_name, credit_data[0], credit_data[1]
        )
        report_data["sheet"].merge_range(
            report_data["row_pos"],
            min(report_data["right_columns"].keys()),
            report_data["row_pos"],
            max(report_data["right_columns"].keys()),
            right_str,
            report_data["formats"]["format_header_right"],
        )

        report_data["row_pos"] += 1

    def write_total_balance(self, objects, report_data):
        """Writes total balance row"""
        report = objects
        curr = objects.company_id.currency_id
        decimals = curr.decimal_places
        balance = self.format_value_by_lang(report.total_balance, decimals)
        total_credit = report.total_credit
        total_debit = report.total_debit
        surplus = float_compare(total_credit, total_debit, decimals) == 1
        deficit = float_compare(total_credit, total_debit, decimals) == -1
        if surplus or deficit:
            title = _("SURPLUS") if surplus else _("DEFICIT")
            bal_data = order_currency_amount(curr, balance)
            balance_str = "{}: {} {}".format(title, bal_data[0], bal_data[1])
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                min(report_data["left_columns"].keys()),
                report_data["row_pos"],
                max(report_data["left_columns"].keys()),
                balance_str if surplus else "",
                report_data["formats"]["format_header_right"],
            )
            report_data["sheet"].merge_range(
                report_data["row_pos"],
                min(report_data["right_columns"].keys()),
                report_data["row_pos"],
                max(report_data["right_columns"].keys()),
                balance_str if deficit else "",
                report_data["formats"]["format_header_right"],
            )
            report_data["row_pos"] += 1

    def _set_column_width(self, report_data):
        report_data.update(
            {
                "left_partner_columns": report_data["columns"].pop(
                    "left_partner_columns"
                ),
                "right_partner_columns": report_data["columns"].pop(
                    "right_partner_columns"
                ),
                "left_columns": report_data["columns"].pop("left_columns"),
                "right_columns": report_data["columns"].pop("right_columns"),
            }
        )

        result = super()._set_column_width(report_data)
        return result
