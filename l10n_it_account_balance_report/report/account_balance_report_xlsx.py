# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

_logger = logging.getLogger(__name__)


def order_currency_amount(curr, val):
    """ Orders currency symbol and amount according to currency position """
    if curr.position == 'before':
        order = (curr.symbol, val)
    else:
        order = (val, curr.symbol)
    return order


class AccountBalanceReportXslx(models.AbstractModel):
    _name = 'report.l10n_it_a_b_r.account_balance_report_xlsx'
    _inherit = 'report.account_financial_report.abstract_report_xlsx'

    def __init__(self, pool, cr):
        """ Adds new attributes """
        super().__init__(pool, cr)

        # Add report data
        self.workbook = None
        self.data = None
        self.report = None
        self.lang = None
        self.currency = None

        # Add table data
        self.left_columns = None
        self.right_columns = None
        self.left_partner_columns = None
        self.right_partner_columns = None
        self.left_lines = None
        self.right_lines = None

        # Add formats
        self.format_amount_right = None
        self.format_amount_bold_right = None
        self.format_header_amount_right = None
        self.format_title = None
        self.format_filter_title = None
        self.format_filter_value = None

    def generate_xlsx_report(self, workbook, data, objects):
        """ Set wb, data and report attributes """
        self.workbook = workbook
        self.data = data
        self.report = objects
        self.lang = self.env['res.lang']._lang_get(self.env.user.lang)
        self.currency = self.report.company_id.currency_id \
            or self.report.company_id._get_euro() \
            or self.env['res.currency'].search(
                [('active', '=', True)], limit=1)
        super().generate_xlsx_report(workbook, data, objects)

    def _define_formats(self, workbook):
        """ Defines new formats """
        super()._define_formats(workbook)
        self.format_amount_right = self.format_amount
        self.format_amount_right.set_align('right')
        self.format_amount_bold_right = self.format_amount_bold
        self.format_amount_bold_right.set_align('right')
        # '#875a7b' is Odoo default purple color
        self.format_title = workbook.add_format({
            'align': 'center',
            'bg_color': '#337AB7',
            'bold': True,
            'border': True,
            'font_color': 'white',
            'font_size': 16,
        })
        self.format_filter_title = workbook.add_format({
            'bg_color': '#337AB7',
            'bold': True,
            'border': True,
            'font_color': 'white',
        })
        self.format_filter_value = workbook.add_format({
            'bg_color': '#337AB7',
            'border': True,
            'font_color': 'white',
        })
        # Change background and font color for header formats
        self.format_header_center.set_bg_color('#337AB7')
        self.format_header_center.set_font_color('#FFFFFF')
        self.format_header_right.set_bg_color('#337AB7')
        self.format_header_right.set_font_color('#FFFFFF')
        self.format_header_amount_right = self.format_header_right
        self.format_header_amount_right.set_num_format(
            '#,##0.' + '0' * self.currency.decimal_places)

    def _get_report_name(self, report):
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
        date_from = report.date_from.strftime('%d-%m-%Y')
        date_to = report.date_to.strftime('%d-%m-%Y')
        return [
            (_("Date range filter"),
             _("From: {} To: {}".format(date_from, date_to))),
            (_("Target moves filter"),
             _("All posted entries")
             if report.only_posted_moves
             else _("All entries")),
            (_("Account at 0 filter"),
             _("Hide")
             if report.hide_account_at_0
             else _("Show")),
            (_("Show foreign currency"),
             _("Yes")
             if report.foreign_currency
             else _("No")),
            (_("Limit hierarchy levels"),
             _("Level %s" % report.show_hierarchy_level)
             if report.limit_hierarchy_level
             else _("No limit")),
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
            0: {'field': 'code',
                'header': _("Code"),
                'indent_field': 'level',
                'indent_unit': 2,
                'width': 20},
            1: {'field': 'name',
                'header': _("Account"),
                'indent_field': 'level',
                'indent_unit': 2,
                'width': 60},
            2: {'field': 'final_balance',
                'header': _("Final balance"),
                'type': 'amount',
                'width': 20}
        }
        if report.foreign_currency:
            cols.update({
                3: {'field': 'currency_id',
                    'field_currency_balance': 'currency_id',
                    'header': _("Cur."),
                    'type': 'many2one',
                    'width': 10},
                4: {'field': 'final_balance_foreign_currency',
                    'header': _("Ending balance in cur."),
                    'type': 'amount_currency',
                    'width': 20}
            })

        self.set_lr_cols(cols)
        self.set_partner_columns(cols)
        return {**self.left_columns, **self.right_columns}

    def set_lr_cols(self, cols):
        """ Takes 'cols' as a template for column info, sets L/R columns """
        self.left_columns = self.generate_section_cols(cols, 'left')
        self.right_columns = self.generate_section_cols(cols, 'right')

    def generate_section_cols(self, cols, mode):
        """ Takes 'cols' as a template for column info, returns L/R column """
        section_cols = {}
        if mode == 'left':
            section_cols = cols.copy()
        elif mode == 'right':
            section_cols = {k + len(cols): v for k, v in cols.items()}
        return section_cols

    def set_partner_columns(self, cols):
        self.left_partner_columns = self.generate_partner_columns(cols, 'left')
        self.right_partner_columns = self.generate_partner_columns(
            cols, 'right')

    def generate_partner_columns(self, cols, mode):
        if mode == 'left':
            left_partner_cols = {k: {} for k in self.left_columns.keys()}
            left_partner_cols.update({
                1: {'field': 'partner_id',
                    'type': 'many2one',
                    'width': 60},
                2: {'field': 'final_balance',
                    'type': 'amount',
                    'width': 20}
            })
            return left_partner_cols
        elif mode == 'right':
            right_partner_cols = {k: {} for k in self.right_columns.keys()}
            right_partner_cols.update({
                1 + len(cols): {'field': 'partner_id',
                                'type': 'many2one',
                                'width': 60},
                2 + len(cols): {'field': 'final_balance',
                                'type': 'amount',
                                'width': 20}
            })
            return right_partner_cols
        raise NotImplementedError

    def _write_report_title(self, title):
        """
        * Overrides standard method *
        Writes report title on current line using all defined columns width
        """
        self.sheet.merge_range(
            self.row_pos, 0, self.row_pos, len(self.columns) - 1,
            title, self.format_title
        )
        self.row_pos += 3

    def _write_filters(self, filters):
        """
        * Overrides standard method *
        Writes filter info
        """
        title_format = self.format_filter_title
        value_format = self.format_filter_value
        for title, value in filters:
            self.sheet.write_string(self.row_pos, 0, title, title_format)
            self.sheet.write_string(self.row_pos, 1, value, value_format)
            self.row_pos += 1
        self.row_pos += 1

    def _generate_report_content(self, workbook, report):
        """ Creates actual xls report """
        self.write_main_headers()
        self.write_sub_headers()
        self.generate_table()
        self.write_sections_balance()
        self.write_total_balance()

    def write_main_headers(self):
        """ Writes main left and right section names """
        self.sheet.merge_range(
            self.row_pos, min(self.left_columns.keys()),
            self.row_pos, max(self.left_columns.keys()),
            self.report.left_col_name, self.format_header_center
        )
        self.sheet.merge_range(
            self.row_pos, min(self.right_columns.keys()),
            self.row_pos, max(self.right_columns.keys()),
            self.report.right_col_name, self.format_header_center
        )
        self.row_pos += 1

    def write_sub_headers(self):
        """ Writes single headers names """
        row, style = self.row_pos, self.format_header_center
        for col, val_dict in self.columns.items():
            value = val_dict.get('header', '')
            self.sheet.write_string(row, col, value, style)
        self.row_pos += 1

    def generate_table(self):
        """ Creates the table """
        report = self.report

        self.left_lines = self.get_report_lines('section_debit_ids')
        self.right_lines = self.get_report_lines('section_credit_ids')
        table = self.get_table_data()

        msg = ""
        if not table.get('row'):
            msg = _(
                "Could not retrieve table datas for report '{}': no lines"
                " found to be printed.".format(report.title)
            )
        elif not table.get('col'):
            msg = _(
                "Could not retrieve table datas for report '{}': unknown"
                " columns to be printed.".format(report.title)
            )
        if msg:
            _logger.warning(msg)
            self.sheet.merge_range(
                self.row_pos, 0, self.row_pos, len(self.columns) - 1,
                msg, self.format_bold
            )
            self.row_pos += 2
            return

        for row in range(table['row']['first'], table['row']['last'] + 1):
            self.row_pos = row
            for (l, cell), (val, style, allow) in self.get_line_info().items():
                col, row = cell
                if allow:
                    self.sheet.write(row, col, val, style)

        self.row_pos += 2

    def get_report_lines(self, field, func=None):
        """
        Returns report's lines, enumerated by row, as assigned by field 'field'
        and filtered by 'func' (either a function or a dot-separated
        list of fields).
        """
        func = func or self.get_default_line_filter_func(field=field) or False
        enum_lines = {}
        report = self.report

        lines = getattr(report, field, False)
        if lines and isinstance(lines, models.BaseModel) and func:
            try:
                lines = lines.filtered(func)
            except (AttributeError, KeyError, TypeError, ValueError):
                if callable(func):
                    fname = func.__name__
                    fvars = func.__code__.co_varnames
                    fvars_names = ', '.join(fvars) if fvars else ''
                    msg = _(
                        "Cannot filter lines with function `{}({})`."
                        .format(fname, fvars_names)
                    )
                elif isinstance(func, str):
                    msg = _(
                        "Cannot filter lines with attribute `{}`."
                        .format(func)
                    )
                else:
                    msg = _(
                        "Cannot filter lines with unknown parameter."
                    )
                _logger.info(msg)

        if lines and self.report.show_partner_details:
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
            enum_lines = {self.row_pos + k: v for k, v in enum_lines.items()}

        return enum_lines

    def get_default_line_filter_func(self, **kwargs):
        func = None
        field = kwargs.get('field')
        if self.report.hide_account_at_0 \
                and field in ('section_credit_ids', 'section_debit_ids'):
            def show(line):
                return not line.hide_line
            func = show
        return func

    def get_table_data(self, left_lines=None, right_lines=None):
        if not left_lines:
            left_lines = self.left_lines
        if not right_lines:
            right_lines = self.right_lines
        table = {}
        rows = list(left_lines) + list(right_lines)
        cols = list(self.left_columns) + list(self.right_columns)
        if rows:
            table.update({
                'row': {
                    'first': min(rows),
                    'last': max(rows),
                }
            })
        if cols:
            table.update({
                'col': {
                    'first': min(cols),
                    'last': max(cols),
                }
            })
        return table

    def get_line_info(self, row=None):
        """ Returns {col: (val, style)} for current row """
        row = row or self.row_pos
        info = {}
        l, r = self.left_lines.get(row), self.right_lines.get(row)

        cols_dict = {}
        if l:
            if l._name == 'account_balance_report_account':
                cols_dict = self.left_columns
            elif l._name == 'account_balance_report_partner':
                cols_dict = self.left_partner_columns
            info.update({
                (l, (c, row)): self.get_write_data(l, cols_dict[c])
                for c in cols_dict
                if cols_dict[c]
            })

        if r:
            if r._name == 'account_balance_report_account':
                cols_dict = self.right_columns
            elif r._name == 'account_balance_report_partner':
                cols_dict = self.right_partner_columns
            info.update({
                (r, (c, row)): self.get_write_data(r, cols_dict[c])
                for c in cols_dict
                if cols_dict[c]
            })

        return info

    def get_write_data(self, line, col_dict):
        """ Returns value and style for cell """
        cell_type = col_dict.get('type', 'string')
        field = col_dict.get('field')
        decimals = self.currency.decimal_places

        value = getattr(line, field, False)
        style = None
        allow = False

        if cell_type == 'many2one':
            val_name = getattr(value, 'name', '')
            val_display = getattr(value, 'display_name', '')
            if val_name:
                value = val_name
            elif val_display:
                value = val_display
            elif line._name == 'account_balance_report_partner':
                value = _("No partner allocated")
        elif cell_type == 'string':
            if getattr(line, 'account_group_id', False):
                style = self.format_bold
            else:
                style = None
        elif cell_type == 'amount':
            value = float_round(float(value), decimals)
            if getattr(line, 'account_group_id', False):
                style = self.format_amount_bold_right
            else:
                style = self.format_amount_right
            allow = True
        elif cell_type == 'amount_currency':
            currency = getattr(line, 'currency_id', False) \
                or getattr(line, 'company_currency_id', False) \
                or self.currency
            decimals = currency.decimal_places
            value = float_round(float(value), decimals)
            if getattr(line, 'account_group_id', False):
                style = self.format_amount_bold_right
            else:
                style = self.format_amount_right
            allow = True

        if value:
            if isinstance(value, (int, float)) \
                    and cell_type not in ('amount', 'amount_currency'):
                value = format(value, '.{}f'.format(decimals))
            if not isinstance(value, str) \
                    and cell_type not in ('amount', 'amount_currency'):
                value = str(value)
            indent_field, indent_unit = self.get_indent_data(line, col_dict)
            if self.report.hierarchy_on != 'none' \
                    and indent_field and indent_unit \
                    and hasattr(line, indent_field):
                indent = ' ' * getattr(line, indent_field, 0) * indent_unit
                value = indent + value
            allow = True

        if allow and isinstance(value, float) \
                and float_is_zero(value, decimals):
            value = format(value, '.{}f'.format(decimals))

        return value, style, allow

    def format_value_by_lang(self, value=None, decimals=None):
        """ Mimics `res.lang` model's `format` method """
        percent = '%.{}f'.format(decimals or 2)
        value = value or 0
        return self.lang.format(percent, value, grouping=True, monetary=True)

    def get_indent_data(self, line=None, col_dict=None):
        return col_dict.get('indent_field'), col_dict.get('indent_unit')

    def write_sections_balance(self):
        """ Writes balances rows for left and right sections """
        report = self.report
        curr = self.currency
        decimals = curr.decimal_places
        credit = self.format_value_by_lang(report.total_credit, decimals)
        credit_data = order_currency_amount(curr, credit)
        debit = self.format_value_by_lang(report.total_debit, decimals)
        debit_data = order_currency_amount(curr, debit)

        left_str = "{} BALANCE: {} {}".format(
            report.left_col_name, debit_data[0], debit_data[1]
        )
        self.sheet.merge_range(
            self.row_pos, min(self.left_columns.keys()),
            self.row_pos, max(self.left_columns.keys()),
            left_str, self.format_header_right
        )

        right_str = "{} BALANCE: {} {}".format(
            report.right_col_name, credit_data[0], credit_data[1]
        )
        self.sheet.merge_range(
            self.row_pos, min(self.right_columns.keys()),
            self.row_pos, max(self.right_columns.keys()),
            right_str, self.format_header_right
        )

        self.row_pos += 1

    def write_total_balance(self):
        """ Writes total balance row """
        report = self.report
        curr = self.currency
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
            self.sheet.merge_range(
                self.row_pos, min(self.left_columns.keys()),
                self.row_pos, max(self.left_columns.keys()),
                balance_str if surplus else '', self.format_header_amount_right
            )
            self.sheet.merge_range(
                self.row_pos, min(self.right_columns.keys()),
                self.row_pos, max(self.right_columns.keys()),
                balance_str if deficit else '', self.format_header_amount_right
            )
            self.row_pos += 1
