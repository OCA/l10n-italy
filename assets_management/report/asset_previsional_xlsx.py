# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, models

_logger = logging.getLogger(__name__)


class AssetJournalXslx(models.AbstractModel):
    _name = 'report.assets_management.report_asset_previsional_xlsx'
    _inherit = 'report.account_financial_report.abstract_report_xlsx'

    def __init__(self, pool, cr):
        """ Adds new attributes """
        super().__init__(pool, cr)

        # Add report objects
        self.workbook = None
        self.data = None
        self.report = None

        # These `_data`s here are made as dict of dicts, the key being the
        # column number to be printed into, the second one the field datas for
        # the print itself
        self.category_data = None
        self.asset_data = None
        self.asset_accounting_doc_data = None
        self.depreciation_data = None
        self.depreciation_line_year_data = None
        self.depreciation_line_amount_detail_data = None
        self.totals_data = None

        # 1- Category formats
        self.format_category_name = None

        # 2- Asset formats (purchase and sale docs will use the same format)
        self.format_asset_header = None
        self.format_asset_value = None

        # 3- Depreciations formats
        self.format_depreciation_header = None
        self.format_depreciation_value = None

        # 4- Depreciation yearly and amount details formats
        self.format_depreciation_year_line_header = None
        self.format_depreciation_year_line_value_center = None
        self.format_depreciation_year_line_value_right = None

        # 5- Report title
        self.format_title = None

    def generate_xlsx_report(self, workbook, data, objects):
        """ Set wb, data and report attributes """
        self.workbook = workbook
        self.data = data
        self.report = objects
        self.set_formats()
        self.set_report_data()
        super().generate_xlsx_report(workbook, data, objects)

    def set_formats(self):
        """ Defines custom formats """

        # 1- Category formats
        self.format_category_name = self.workbook.add_format({
            'align': 'center',
            'bg_color': '#337AB7',
            'bold': True,
            'font_color': '#FFFFFF',
            'font_size': 16,
        })

        # 2- Asset formats
        self.format_asset_header = self.workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_color': '#337AB7',
            'font_size': 14,
        })
        self.format_asset_value = self.workbook.add_format({
            'align': 'center',
            'font_color': '#337AB7',
            'font_size': 14,
        })

        # 3- Depreciations formats
        self.format_depreciation_header = self.workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': 12,
        })
        self.format_depreciation_value = self.workbook.add_format({
            'align': 'center',
            'font_size': 12,
        })

        # 4- Depreciation yearly and amount details formats
        self.format_depreciation_year_line_header = self.workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': 12,
        })
        self.format_depreciation_year_line_value_center = self.workbook \
            .add_format({
                'align': 'center',
                'font_size': 12,
            })
        self.format_depreciation_year_line_value_right = self.workbook \
            .add_format({
                'align': 'right',
                'font_size': 12,
            })

        # 5- Report title
        self.format_title = self.workbook.add_format({
            'align': 'center',
            'bg_color': '#337AB7',
            'bold': True,
            'font_color': 'white',
            'font_size': 20,
        })

    def set_report_data(self):
        self.set_category_data()
        self.set_asset_data()
        self.set_asset_accounting_doc_data()
        self.set_depreciation_data()
        self.set_depreciation_line_year_data()
        self.set_depreciation_line_amount_detail_data()
        self.set_totals_data()

    def set_category_data(self):
        self.category_data = self.generate_category_data()

    def generate_category_data(self):
        data = (
            {'title': _("Category"),
             'field': 'category_name',
             'tstyle': self.format_category_name,
             'vstyle': self.format_category_name},
        )
        return dict(enumerate(data))

    def set_asset_data(self):
        self.asset_data = self.generate_asset_data()

    def generate_asset_data(self):
        data = (
            {'title': _("Asset"),
             'field': 'asset_name',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Code"),
             'field': 'asset_code',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Purchase Amount"),
             'field': 'asset_purchase_amount',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Purchased as New / Used"),
             'field': 'asset_used',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Status"),
             'field': 'asset_state',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
        )
        return dict(enumerate(data))

    def set_asset_accounting_doc_data(self):
        self.asset_accounting_doc_data = \
            self.generate_asset_accounting_doc_data()

    def generate_asset_accounting_doc_data(self):
        data = (
            {'title': _("Partner"),
             'field': 'partner_name',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("VAT"),
             'field': 'partner_vat',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Document Nr"),
             'field': 'document_nr',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Document Date"),
             'field': 'document_date',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Supplier Ref"),
             'field': 'partner_ref',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_data(self):
        self.depreciation_data = self.generate_depreciation_data()

    def generate_depreciation_data(self):
        data = (
            {'title': _("Depreciation Type"),
             'field': 'type_name',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
            {'title': _("Depreciation Mode"),
             'field': 'mode_name',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
            {'title': _("Depreciable Amount"),
             'field': 'dep_amount_depreciable',
             'type': 'amount',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
            {'title': _("Starting From"),
             'field': 'dep_date_start',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
            {'title': _("Dep. Percentage (%)"),
             'field': 'dep_percentage',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
            {'title': _("Pro Rata Temporis"),
             'field': 'dep_pro_rata_temporis',
             'tstyle': self.format_depreciation_header,
             'vstyle': self.format_depreciation_value},
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_line_year_data(self):
        self.depreciation_line_year_data = \
            self.generate_depreciation_line_year_data()

    def generate_depreciation_line_year_data(self):
        data = (
            {'title': _("Year"),
             'field': 'year',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_center},
            {'title': _("Amount"),
             'field': 'amount_depreciable_updated',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("In Amount"),
             'field': 'amount_in',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Out Amount"),
             'field': 'amount_out',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Prev. Year Dep. Fund"),
             'field': 'amount_depreciation_fund_prev_year',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Depreciation"),
             'field': 'amount_depreciated',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Curr. Year Dep. Fund"),
             'field': 'amount_depreciation_fund_curr_year',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Gain / Loss"),
             'field': 'gain_loss',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
            {'title': _("Residual"),
             'field': 'amount_residual',
             'type': 'amount',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_right},
        )
        return {n + 1: d for n, d in enumerate(data)}

    def set_depreciation_line_amount_detail_data(self):
        self.depreciation_line_amount_detail_data = \
            self.generate_depreciation_line_amount_detail_data()

    def generate_depreciation_line_amount_detail_data(self):
        data = (
            {'title': _("In Amount - Detail"),
             'field': 'amount_in_detail',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_center},
            {'title': _("Out Amount - Detail"),
             'field': 'amount_out_detail',
             'tstyle': self.format_depreciation_year_line_header,
             'vstyle': self.format_depreciation_year_line_value_center},
        )
        return {n + 3: d for n, d in enumerate(data)}

    def set_totals_data(self):
        self.totals_data = self.get_totals_data()

    def get_totals_data(self):
        data = (
            {'title': _("Total"),
             'field': 'name',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Type"),
             'field': 'type_name',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Amount"),
             'field': 'amount_depreciable_updated',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("In Amount"),
             'field': 'amount_in_total',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Out Amount"),
             'field': 'amount_out_total',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Prev. Year Dep. Fund"),
             'field': 'amount_depreciation_fund_prev_year',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Depreciation"),
             'field': 'amount_depreciated',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Curr. Year Dep. Fund"),
             'field': 'amount_depreciation_fund_curr_year',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Gain / Loss"),
             'field': 'gain_loss_total',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
            {'title': _("Residual"),
             'field': 'amount_residual',
             'type': 'amount',
             'tstyle': self.format_asset_header,
             'vstyle': self.format_asset_value},
        )
        return {n: d for n, d in enumerate(data)}

    def _set_column_width(self):
        """ Override to force every column to width 25 at least """
        max_width = self.get_max_width_dict()
        for col, width in max_width.items():
            self.sheet.set_column(col, col, max(width, 25))

    def get_max_width_dict(self):
        min_col = min([
            min(self.category_data.keys()),
            min(self.asset_data.keys()),
            min(self.asset_accounting_doc_data.keys()),
            min(self.depreciation_data.keys()),
            min(self.depreciation_line_year_data.keys()),
            min(self.depreciation_line_amount_detail_data.keys()),
            min(self.totals_data.keys()),
        ])
        max_col = max([
            max(self.category_data.keys()),
            max(self.asset_data.keys()),
            max(self.asset_accounting_doc_data.keys()),
            max(self.depreciation_data.keys()),
            max(self.depreciation_line_year_data.keys()),
            max(self.depreciation_line_amount_detail_data.keys()),
            max(self.totals_data.keys()),
        ])

        return {
            col: max([
                self.category_data.get(col, {}).get('width') or 0,
                self.asset_data.get(col, {}).get('width') or 0,
                self.asset_accounting_doc_data.get(col, {}).get('width') or 0,
                self.depreciation_data.get(col, {}).get('width') or 0,
                self.depreciation_line_year_data.get(col, {})
                .get('width') or 0,
                self.depreciation_line_amount_detail_data.get(col, {})
                .get('width') or 0,
                self.totals_data.get(col, {}).get('width') or 0,
            ])
            for col in range(min_col, max_col + 1)
        }

    def _get_report_name(self, report):
        """
        * Overrides standard method *
        Returns name for both sheet and report title
        """
        return self._get_report_complete_name(report, report.report_name)

    def _write_report_title(self, title):
        """
        * Overrides standard method *
        Writes report title on current line using all defined columns width
        """
        self.sheet.merge_range(
            self.row_pos, 0, self.row_pos, 9,
            title, self.format_title
        )
        self.row_pos += 3

    def _generate_report_content(self, workbook, report):
        """ Creates actual xls report """
        for categ_section in report.report_category_ids:
            self.write_all(self.category_data, categ_section)

            for asset_section in categ_section.report_asset_ids:
                self.write_all(self.asset_data, asset_section)

                if asset_section.report_purchase_doc_id:
                    self.write_all(
                        self.asset_accounting_doc_data,
                        asset_section.report_purchase_doc_id
                    )

                for dep_section in asset_section.report_depreciation_ids:
                    self.write_all(self.depreciation_data, dep_section)

                    self.write_header(self.depreciation_line_year_data)
                    for year in dep_section.report_depreciation_year_line_ids:
                        self.write_value(
                            self.depreciation_line_year_data, year
                        )
                        if year.has_amount_detail:
                            self.write_value(
                                self.depreciation_line_amount_detail_data, year
                            )

                if asset_section.report_sale_doc_id:
                    self.write_all(
                        self.asset_accounting_doc_data,
                        asset_section.report_sale_doc_id
                    )
                self.row_pos += 1

            if report.show_category_totals:
                self.write_header(self.totals_data)
                for total_section in categ_section.report_total_ids:
                    self.write_value(self.totals_data, total_section)
                self.row_pos += 1

            self.row_pos += 1

        if report.show_totals:
            self.write_header(self.totals_data)
            for total_section in report.report_total_ids:
                self.write_value(self.totals_data, total_section)
            self.row_pos += 1

    def write_all(self, data, obj):
        self.write_header(data)
        self.write_value(data, obj)

    def write_header(self, data):
        pos = self.row_pos
        for col, data in data.items():
            self.sheet.write(pos, col, data['title'], data['tstyle'])
        self.row_pos += 1

    def write_value(self, data, obj):
        pos = self.row_pos
        for col, data in data.items():
            value, style = getattr(obj, data['field']), data['vstyle']
            if data.get('type') == 'amount':
                value = getattr(obj, 'format_amount')(value)
            if value in (False, None):
                value = '/'
            self.sheet.write(pos, col, value, style)
        self.row_pos += 1

    ########################################################
    #                                                      #
    # UNUSED METHODS, OVERRIDDEN FOR COMPATIBILITY REASONS #
    #                                                      #
    ########################################################

    def _get_report_filters(self, report):
        """ Override original method even if not used to avoid errors """
        return []

    def _get_report_columns(self, report):
        """ Override original method even if not used to avoid errors """
        return {}

    def _get_col_count_filter_name(self):
        """ Override original method even if not used to avoid errors """
        pass

    def _get_col_count_filter_value(self):
        """ Override original method even if not used to avoid errors """
        pass

    def _write_filters(self, filters):
        """ Override original method even if not used to avoid errors """
        pass
