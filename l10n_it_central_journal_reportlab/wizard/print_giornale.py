# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)
# Copyright 2022 Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# Copyright 2024 Simone Rubino - Aion Tech
# Copyright 2025 Michele Di Croce - Stesi Consulting
# Copyright 2025 Nextev Srl (odoo@nextev.it)

import base64
import io
import logging
import threading
import time
from datetime import timedelta
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.platypus.paragraph import Paragraph

from odoo import _, api, fields, models, registry
from odoo.exceptions import UserError
from odoo.tools.misc import flatten, format_date, formatLang

_logger = logging.getLogger(__name__)

gap = 1 * cm  # gap between header/footer and page content
gap_text = 0.5 * cm  # gap between text
margin_left = 0.5 * cm  # layout margin left
margin_bottom = 0.5 * cm  # layout margin bottom
footer_height = 2 * gap_text + 12  # layout footer height


class WizardGiornaleReportlab(models.TransientModel):
    @api.model
    def _get_journal(self):
        journal_obj = self.env["account.journal"]
        journal_ids = journal_obj.search(
            [
                ("central_journal_exclude", "=", False),
            ]
        )
        return journal_ids

    _name = "wizard.giornale.reportlab"
    _description = "Wizard journal report with reportlab"

    date_move_line_from = fields.Date(required=True)
    date_move_line_from_view = fields.Date("From date")
    last_def_date_print = fields.Date("Last definitive date print")
    date_move_line_to = fields.Date("To date", required=True)
    daterange_id = fields.Many2one("date.range", "Date Range", required=True)
    company_id = fields.Many2one(
        related="daterange_id.company_id", readonly=True, store=True
    )
    progressive_credit = fields.Float()
    progressive_debit2 = fields.Float("Progressive Debit")
    print_state = fields.Selection(
        [("print", "Ready for printing"), ("printed", "Printed")],
        "State",
        default="print",
        readonly=True,
    )
    journal_ids = fields.Many2many(
        "account.journal",
        "giornale_reportlab_journals_rel",
        "journal_id",
        "giornale_reportlab_id",
        default=_get_journal,
        string="Journals",
        required=True,
    )
    target_move = fields.Selection(
        [("all", "All"), ("posted", "Posted"), ("draft", "Draft")],
        default="all",
    )
    fiscal_page_base = fields.Integer("Last printed page", required=True)
    start_row = fields.Integer("Start row", required=True)
    year_footer = fields.Char(
        string="Year for Footer",
        help="Value printed near number of page in the footer",
    )
    report_giornale = fields.Binary()
    attachment_id = fields.Many2one(
        "ir.attachment",
        string="Generated Report",
        readonly=True,
        help="Attachment containing the generated PDF report",
    )
    group_by_account = fields.Boolean(default=False)

    # Background processing fields
    generation_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("processing", "Processing"),
            ("done", "Done"),
            ("failed", "Failed"),
        ],
        string="Generation Status",
        default="draft",
        readonly=True,
    )
    generation_error = fields.Text(readonly=True)
    generation_progress = fields.Integer(
        string="Progress (%)", readonly=True, default=0
    )

    def unlink(self):
        """Delete associated attachments when wizard is deleted"""
        # Get all attachments before deleting the wizard
        attachment = self.attachment_id
        result = super().unlink()
        # Delete attachments after wizard deletion
        if attachment:
            attachment.unlink()
        return result

    @api.onchange("date_move_line_from_view")
    def get_year_footer_reportlab(self):
        if self.date_move_line_from_view:
            self.year_footer = fields.Date.to_date(self.date_move_line_from_view).year

    @api.onchange("daterange_id")
    def on_change_daterange_reportlab(self):
        if self.daterange_id:
            date_start = fields.Date.to_date(self.daterange_id.date_start)
            date_end = fields.Date.to_date(self.daterange_id.date_end)

            if self.daterange_id.date_last_print:
                date_last_print = fields.Date.to_date(self.daterange_id.date_last_print)
                self.last_def_date_print = date_last_print
                date_start = (date_last_print + timedelta(days=1)).__str__()
            else:
                self.last_def_date_print = None
            self.date_move_line_from = date_start
            self.date_move_line_from_view = date_start
            self.date_move_line_to = date_end
            if self.daterange_id.progressive_line_number != 0:
                self.start_row = self.daterange_id.progressive_line_number + 1
            else:
                self.start_row = self.daterange_id.progressive_line_number
            self.progressive_debit2 = self.daterange_id.progressive_debit
            self.progressive_credit = self.daterange_id.progressive_credit

            if self.last_def_date_print == self.daterange_id.date_end:
                self.date_move_line_from_view = self.last_def_date_print

    def get_grupped_line_reportlab_ids(self):
        wizard = self
        if wizard.target_move == "all":
            target_type = ["posted", "draft"]
        else:
            target_type = [wizard.target_move]
        sql = """
            SELECT
                am.date,
                am.name AS move_name,
                aa.code AS account_code,
                aa.name AS account_name,
                COALESCE(am.ref, '') AS name,
                SUM(aml.debit) AS debit,
                SUM(aml.credit) AS credit
            FROM
                account_move_line aml
                LEFT JOIN account_move am ON (am.id = aml.move_id)
                LEFT JOIN account_account aa ON (aa.id = aml.account_id)
            WHERE
                aml.date >= %(date_from)s
                AND aml.date <= %(date_to)s
                AND am.state in %(target_type)s
                AND aml.journal_id in %(journal_ids)s
            GROUP BY
                am.date,
                am.name,
                aa.code,
                aa.name,
                am.ref
            ORDER BY
                am.date,
                am.name,
                aa.code
        """
        params = {
            "date_from": wizard.date_move_line_from,
            "date_to": wizard.date_move_line_to,
            "target_type": tuple(target_type),
            "journal_ids": tuple(self.journal_ids.ids),
        }
        self.env.cr.execute(sql, params)
        list_grupped_line = self.env.cr.dictfetchall()
        return list_grupped_line

    def get_line_reportlab_ids(self):
        if self.target_move == "all":
            target_type = ["posted", "draft"]
        else:
            target_type = [self.target_move]
        sql = """
            SELECT aml.id FROM account_move_line aml
            LEFT JOIN account_move am ON (am.id = aml.move_id)
            LEFT JOIN account_account aa ON (aa.id = aml.account_id)
            WHERE
            aml.date >= %(date_from)s
            AND aml.date <= %(date_to)s
            AND am.state in %(target_type)s
            AND aml.journal_id in %(journal_ids)s
            AND aml.account_id IS NOT NULL
            AND aml.display_type NOT IN ('line_note','line_section')
            ORDER BY am.date, am.name, aa.code
        """
        params = {
            "date_from": self.date_move_line_from,
            "date_to": self.date_move_line_to,
            "target_type": tuple(target_type),
            "journal_ids": tuple(self.journal_ids.ids),
        }
        self.env.cr.execute(sql, params)
        res = self.env.cr.fetchall()
        move_line_ids = flatten(res)
        return move_line_ids

    def _update_batch_progress(self, batch_idx, total_batches, batch_size, message):
        """
        Common method to update progress during batch processing.

        :param batch_idx: current batch index (0-based)
        :param total_batches: total number of batches
        :param batch_size: size of current batch
        :param message: progress message to display
        """
        progress = int((batch_idx + 1) / total_batches * 100)
        _logger.info(
            "Processing batch %d/%d (%d lines, %d%% complete)",
            batch_idx + 1,
            total_batches,
            batch_size,
            progress,
        )

        # Update progress in wizard
        self.write({"generation_progress": progress})

        # Skip commit and notifications in test mode
        if not self.env.context.get("test_mode"):
            # pylint: disable=invalid-commit
            self.env.cr.commit()

            # Send progress notification
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "l10n_it_central_journal.report_progress",
                {
                    "title": _("Generating Central Journal"),
                    "message": message,
                    "progress": progress,
                },
            )

    def _handle_page_break(
        self,
        report,
        height_available,
        width_available,
        colwidths,
        tot_debit,
        tot_credit,
    ):
        """
        Common method to handle page breaks with balance carry-forward.

        :param report: reportlab canvas object
        :param height_available: current height position
        :param width_available: available width for tables
        :param colwidths: pre-calculated column widths
        :param tot_debit: current total debit
        :param tot_credit: current total credit
        :return: new height_available after page break
        """
        HEIGHT = A4[1]
        style_table = self.get_styles_report_giornale_line()["style_table"]
        style_table_line_above = self.get_styles_report_giornale_line()[
            "style_table_line_above"
        ]

        # Add balance at bottom of current page
        balance_data = self.get_balance_data_report_giornale(
            tot_debit, tot_credit, final=False
        )
        balance_table = Table(
            balance_data,
            colWidths=colwidths,
            style=style_table_line_above,
        )
        balance_height = balance_table.wrapOn(report, width_available, HEIGHT)[1]
        height_available -= balance_height
        balance_table.drawOn(report, margin_left, height_available)

        # Page break
        self.get_template_footer_report_giornale(report)
        report.showPage()
        height_available = self.get_template_header_report_giornale(report, HEIGHT)
        height_available -= gap

        # Add header on new page
        data_header = self.get_data_header_report_giornale()
        header_table = Table(data_header, colWidths=colwidths, style=style_table)
        header_height = header_table.wrapOn(report, width_available, HEIGHT)[1]
        height_available -= header_height
        header_table.drawOn(report, margin_left, height_available)

        # Add balance at top of new page
        balance_table = Table(balance_data, colWidths=colwidths, style=style_table)
        balance_height = balance_table.wrapOn(report, width_available, HEIGHT)[1]
        height_available -= balance_height
        balance_table.drawOn(report, margin_left, height_available)

        return height_available

    def _process_lines_in_batches(
        self,
        move_line_ids,
        report,
        height_available,
        width_available,
        colwidths,
        batch_size=500,
    ):
        """
        Process account move lines in batches to avoid timeout and memory issues.
        Commits after each batch to keep the connection alive.

        :param move_line_ids: list of account.move.line IDs to process
        :param report: reportlab canvas object
        :param height_available: current height position on page
        :param width_available: available width for tables
        :param colwidths: pre-calculated column widths
        :param batch_size: number of lines to process per batch
        :return: tuple (start_row, tot_debit, tot_credit, height_available)
        """
        batches = [
            move_line_ids[i : i + batch_size]
            for i in range(0, len(move_line_ids), batch_size)
        ]

        start_row = self.start_row
        tot_debit = self.progressive_debit2
        tot_credit = self.progressive_credit
        previous_move_name = ""

        for batch_idx, batch_ids in enumerate(batches):
            self._update_batch_progress(
                batch_idx, len(batches), len(batch_ids), _("Processing report...")
            )

            # Process batch
            (
                start_row,
                tot_debit,
                tot_credit,
                height_available,
                previous_move_name,
            ) = self._process_single_batch(
                batch_ids,
                report,
                height_available,
                width_available,
                colwidths,
                start_row,
                tot_debit,
                tot_credit,
                previous_move_name,
            )

        return start_row, tot_debit, tot_credit, height_available

    def _process_single_batch(
        self,
        line_ids,
        report,
        height_available,
        width_available,
        colwidths,
        start_row,
        tot_debit,
        tot_credit,
        previous_move_name,
    ):
        """
        Process a single batch of account move lines.

        :param width_available: available width for tables
        :param colwidths: pre-calculated column widths
        :return: tuple (start_row, tot_debit, tot_credit, height_available,
                        previous_move_name)
        """
        # Use SQL query for maximum performance and minimal memory usage
        # This avoids loading entire recordsets into memory
        self.env.cr.execute(
            """
            SELECT
                aml.id,
                aml.date,
                aml.ref,
                aml.name as line_name,
                aml.debit,
                aml.credit,
                am.name as move_name,
                aa.code as account_code,
                aa.name as account_name,
                aa.account_type,
                rp.name as partner_name,
                COALESCE(aml.ref, '') as ref_safe,
                COALESCE(am.name, '') as move_name_safe
            FROM account_move_line aml
            LEFT JOIN account_move am ON am.id = aml.move_id
            LEFT JOIN account_account aa ON aa.id = aml.account_id
            LEFT JOIN res_partner rp ON rp.id = aml.partner_id
            WHERE aml.id IN %s
            ORDER BY am.date, am.name, aa.code
        """,
            (tuple(line_ids),),
        )

        lines_data = self.env.cr.dictfetchall()

        # Cache styles to avoid recreating objects for each line
        styles = self.get_styles_report_giornale_line()
        style_name = styles["style_name"]
        style_number = styles["style_number"]
        style_table = styles["style_table"]
        style_table_line_above = styles["style_table_line_above"]

        # Cache for formatted dates to avoid repeated formatting
        date_cache = {}
        # Cache for monetary formatting to speed up repeated values
        zero_debit = formatLang(self.env, 0.0, monetary=True)
        zero_credit = zero_debit

        for line_data in lines_data:
            start_row += 1

            # Build account name from SQL data
            account_code = line_data.get("account_code")
            account_name_field = line_data.get("account_name")
            if account_code and account_name_field:
                account_name = f"{account_code} - {account_name_field}"
            else:
                account_name = account_name_field or account_code or ""

            # Determine display name for partner/description
            if line_data.get("account_type") in [
                "asset_receivable",
                "liability_payable",
            ]:
                display_name = escape(line_data.get("partner_name") or "")
            else:
                display_name = escape(line_data.get("line_name") or "")

            # Format date with caching (same dates appear multiple times)
            line_date = line_data["date"]
            if line_date not in date_cache:
                date_cache[line_date] = format_date(self.env, line_date)
            formatted_date = date_cache[line_date]

            # Format monetary values (use cached zeros for performance)
            debit_val = line_data["debit"]
            credit_val = line_data["credit"]
            debit_formatted = (
                formatLang(self.env, debit_val, monetary=True)
                if debit_val != 0
                else zero_debit
            )
            credit_formatted = (
                formatLang(self.env, credit_val, monetary=True)
                if credit_val != 0
                else zero_credit
            )

            # Create row data (using pre-computed values and SQL-safe fields)
            row_data = [
                [
                    Paragraph(str(start_row), style_name),
                    Paragraph(formatted_date, style_name),
                    Paragraph(escape(line_data["ref_safe"]), style_name),
                    Paragraph(escape(line_data["move_name_safe"]), style_name),
                    Paragraph(escape(account_name), style_name),
                    Paragraph(display_name, style_name),
                    Paragraph(debit_formatted, style_number),
                    Paragraph(credit_formatted, style_number),
                ]
            ]

            # Use line above style when move name changes (to group counterparts)
            move_name = line_data["move_name_safe"]
            if previous_move_name != move_name:
                previous_move_name = move_name
                table = Table(
                    row_data, colWidths=colwidths, style=style_table_line_above
                )
            else:
                table = Table(row_data, colWidths=colwidths, style=style_table)

            HEIGHT = A4[1]
            height_table = table.wrapOn(report, width_available, HEIGHT)[1]

            if (height_available - height_table) < footer_height:
                # Handle page break with balance carry-forward
                height_available = self._handle_page_break(
                    report,
                    height_available,
                    width_available,
                    colwidths,
                    tot_debit,
                    tot_credit,
                )

            height_available -= height_table
            table.drawOn(report, margin_left, height_available)

            tot_debit += line_data["debit"]
            tot_credit += line_data["credit"]
            previous_move_name = move_name

        return start_row, tot_debit, tot_credit, height_available, previous_move_name

    def _get_account_name_reportlab(self, line):
        return " - ".join(filter(None, [line.account_id.code, line.account_id.name]))

    def get_template_header_report_giornale(self, report, height_available):
        report.setFont("Helvetica-Bold", 12)
        height_available -= gap
        report.drawString(
            margin_left,
            height_available,
            self.company_id.name + _(" - Account Central Journal"),
        )
        report.setFont("Helvetica", 10)
        text = ""
        if self.company_id.street:
            text += self.company_id.street
        if self.company_id.zip:
            text += " " + self.company_id.zip
        if self.company_id.city:
            text += " - " + self.company_id.city
        if self.company_id.state_id.code:
            text += " - " + self.company_id.state_id.code
        if self.company_id.vat:
            text += " IVA: " + self.company_id.vat
        height_available -= gap_text
        report.drawString(margin_left, height_available, text)
        return height_available

    def get_template_footer_report_giornale(self, report):
        page_num = report.getPageNumber() + self.fiscal_page_base
        page_text = _("Page: %(year_footer)s / %(page_num)s") % {
            "year_footer": self.year_footer,
            "page_num": page_num,
        }
        report.drawString(margin_left, margin_bottom + 12, page_text)

    def get_styles_report_giornale_line(self):
        style_header = ParagraphStyle("style_header")
        style_header.fontSize = 10
        style_header.fontName = "Helvetica-Bold"

        style_header_number = ParagraphStyle("style_header_number")
        style_header_number.alignment = TA_RIGHT
        style_header_number.fontSize = 10
        style_header_number.fontName = "Helvetica-Bold"

        style_name = ParagraphStyle("style_name")
        style_name.fontSize = 6.5
        style_name.fontName = "Helvetica"

        style_number = ParagraphStyle("style_number")
        style_number.fontSize = 6.5
        style_number.alignment = TA_RIGHT
        style_number.fontName = "Helvetica"

        style_table = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
        ]
        style_table_line_above = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 1),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1),
            ("TOPPADDING", (0, 0), (-1, -1), 1),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ("LINEABOVE", (0, 0), (-1, -1), 1, colors.black),
        ]
        return {
            "style_header": style_header,
            "style_header_number": style_header_number,
            "style_name": style_name,
            "style_number": style_number,
            "style_table": style_table,
            "style_table_line_above": style_table_line_above,
        }

    def get_colwidths_report_giornale(self, width_available):
        # Row, Date, Ref, Number, Account, Name, Debit, Credit
        colwidths = [32, 40, 100, 70, 130, 100, 50, 50]
        total = sum(colwidths)
        return [c / total * width_available for c in colwidths]

    def get_data_header_report_giornale(self):
        style_header = self.get_styles_report_giornale_line()["style_header"]
        style_header_number = self.get_styles_report_giornale_line()[
            "style_header_number"
        ]

        data_header = [
            [
                Paragraph(_("Row"), style_header),
                Paragraph(_("Date"), style_header),
                Paragraph(_("Ref"), style_header),
                Paragraph(_("Number"), style_header),
                Paragraph(_("Account"), style_header),
                Paragraph(_("Name"), style_header),
                Paragraph(_("Debit"), style_header_number),
                Paragraph(_("Credit"), style_header_number),
            ]
        ]
        return data_header

    def get_initial_balance_data_report_giornale(self):
        style_name = self.get_styles_report_giornale_line()["style_name"]
        style_number = self.get_styles_report_giornale_line()["style_number"]

        initial_balance_data = [
            [
                "",
                "",
                "",
                "",
                "",
                Paragraph(_("Initial Balance"), style_name),
                Paragraph(
                    escape(formatLang(self.env, self.progressive_debit2)), style_number
                ),
                Paragraph(
                    escape(formatLang(self.env, self.progressive_credit)), style_number
                ),
            ]
        ]
        return initial_balance_data

    def _process_grouped_lines_in_batches(
        self,
        grouped_lines_data,
        report,
        height_available,
        width_available,
        colwidths,
        batch_size=500,
    ):
        """
        Process grouped account move lines in batches.
        Similar to _process_lines_in_batches but works with SQL aggregated data.

        :param grouped_lines_data: list of dictionaries from SQL GROUP BY query
        :param report: reportlab canvas object
        :param height_available: current height position on page
        :param width_available: available width for tables
        :param colwidths: pre-calculated column widths
        :param batch_size: number of lines to process per batch
        :return: tuple (start_row, tot_debit, tot_credit, height_available)
        """
        batches = [
            grouped_lines_data[i : i + batch_size]
            for i in range(0, len(grouped_lines_data), batch_size)
        ]

        start_row = self.start_row
        tot_debit = self.progressive_debit2
        tot_credit = self.progressive_credit
        previous_move_name = ""

        for batch_idx, batch_data in enumerate(batches):
            self._update_batch_progress(
                batch_idx,
                len(batches),
                len(batch_data),
                _("Processing grouped report..."),
            )

            # Process batch
            (
                start_row,
                tot_debit,
                tot_credit,
                height_available,
                previous_move_name,
            ) = self._process_single_grouped_batch(
                batch_data,
                report,
                height_available,
                width_available,
                colwidths,
                start_row,
                tot_debit,
                tot_credit,
                previous_move_name,
            )

        return start_row, tot_debit, tot_credit, height_available

    def _process_single_grouped_batch(
        self,
        grouped_data,
        report,
        height_available,
        width_available,
        colwidths,
        start_row,
        tot_debit,
        tot_credit,
        previous_move_name,
    ):
        """
        Process a single batch of grouped account move lines.

        :return: tuple (start_row, tot_debit, tot_credit, height_available,
                        previous_move_name)
        """
        # Cache styles
        styles = self.get_styles_report_giornale_line()
        style_name = styles["style_name"]
        style_number = styles["style_number"]
        style_table = styles["style_table"]
        style_table_line_above = styles["style_table_line_above"]

        HEIGHT = A4[1]

        # Cache for formatted dates to avoid repeated formatting
        date_cache = {}
        # Cache for monetary formatting - zeros are very common in grouped reports
        zero_formatted = formatLang(self.env, 0.0)

        for line in grouped_data:
            # Build account name
            account_code = line.get("account_code", "")
            account_name_field = line.get("account_name", "")
            account_name = (
                f"{account_code} - {account_name_field}"
                if account_code
                else account_name_field
            )
            if not account_name:
                continue

            move_name = line.get("move_name", "")

            # Format date with caching
            line_date = line["date"]
            if line_date not in date_cache:
                date_cache[line_date] = format_date(self.env, line_date)
            formatted_date = date_cache[line_date]

            # In grouped mode, a single account line may have both debit and credit
            # so we need to create separate rows for each
            lines_to_add = []
            if line.get("debit", 0) > 0:
                lines_to_add.append(("debit", line["debit"], 0))
            if line.get("credit", 0) > 0:
                lines_to_add.append(("credit", 0, line["credit"]))

            for _line_type, debit_val, credit_val in lines_to_add:
                start_row += 1

                # Format monetary values with caching for zeros
                debit_formatted = (
                    formatLang(self.env, debit_val)
                    if debit_val != 0
                    else zero_formatted
                )
                credit_formatted = (
                    formatLang(self.env, credit_val)
                    if credit_val != 0
                    else zero_formatted
                )

                row_data = [
                    [
                        Paragraph(str(start_row), style_name),
                        Paragraph(formatted_date, style_name),
                        Paragraph(escape(line.get("ref", "") or ""), style_name),
                        Paragraph(escape(move_name), style_name),
                        Paragraph(escape(account_name), style_name),
                        Paragraph(escape(line.get("name", "") or ""), style_name),
                        Paragraph(debit_formatted, style_number),
                        Paragraph(credit_formatted, style_number),
                    ]
                ]

                # Update totals
                tot_debit += debit_val
                tot_credit += credit_val

                # Apply line above style when move changes
                if previous_move_name != move_name:
                    previous_move_name = move_name
                    table = Table(
                        row_data, colWidths=colwidths, style=style_table_line_above
                    )
                else:
                    table = Table(row_data, colWidths=colwidths, style=style_table)

                height_table = table.wrapOn(report, width_available, HEIGHT)[1]

                # Check if we need a new page
                if (height_available - height_table) < footer_height:
                    # Handle page break with balance carry-forward
                    height_available = self._handle_page_break(
                        report,
                        height_available,
                        width_available,
                        colwidths,
                        tot_debit,
                        tot_credit,
                    )

                # Draw the line
                height_available -= height_table
                table.drawOn(report, margin_left, height_available)

        return start_row, tot_debit, tot_credit, height_available, previous_move_name

    def get_balance_data_report_giornale(self, tot_debit, tot_credit, final=False):
        style_name = self.get_styles_report_giornale_line()["style_name"]
        style_number = self.get_styles_report_giornale_line()["style_number"]

        if final:
            name = Paragraph(_("Final Balance"), style_name)
        else:
            name = Paragraph(_("Balance"), style_name)

        balance_data = [
            [
                "",
                "",
                "",
                "",
                "",
                name,
                Paragraph(escape(formatLang(self.env, tot_debit)), style_number),
                Paragraph(escape(formatLang(self.env, tot_credit)), style_number),
            ]
        ]
        return balance_data

    def create_report_giornale_reportlab(self):
        """
        Report creation method processing to avoid timeouts on large datasets
        """
        pdf_bytes = io.BytesIO()

        WIDTH, HEIGHT = A4
        width_available = WIDTH - (2 * margin_left)
        height_available = HEIGHT
        report = canvas.Canvas(pdf_bytes, pagesize=A4)
        height_available = self.get_template_header_report_giornale(
            report, height_available
        )

        colwidths = self.get_colwidths_report_giornale(width_available)
        style_table = self.get_styles_report_giornale_line()["style_table"]

        # Header
        data_header = self.get_data_header_report_giornale()
        header_table = Table(data_header, colWidths=colwidths, style=style_table)
        table_height = header_table.wrapOn(report, width_available, HEIGHT)[1]
        height_available -= gap
        height_available -= table_height
        header_table.drawOn(report, margin_left, height_available)

        # Initial balance
        initial_balance_data = self.get_initial_balance_data_report_giornale()
        initial_balance_table = Table(
            initial_balance_data, colWidths=colwidths, style=style_table
        )
        table_height = initial_balance_table.wrapOn(report, width_available, HEIGHT)[1]
        height_available -= table_height
        initial_balance_table.drawOn(report, margin_left, height_available)
        start_row = self.start_row
        if self.group_by_account:
            grouped_lines = self.get_grupped_line_reportlab_ids()
            if not grouped_lines:
                raise UserError(_("No documents found in the current selection"))

            _logger.info(
                "Starting batch processing of %d grouped account lines for journal "
                "report",
                len(grouped_lines),
            )

            # Process grouped lines in batches
            (
                start_row,
                tot_debit,
                tot_credit,
                height_available,
            ) = self._process_grouped_lines_in_batches(
                grouped_lines,
                report,
                height_available,
                width_available,
                colwidths,
                batch_size=500,
            )
        else:
            move_line_ids = self.get_line_reportlab_ids()
            if not move_line_ids:
                raise UserError(_("No documents found in the current selection"))

            _logger.info(
                "Starting batch processing of %d account move lines for journal "
                "report",
                len(move_line_ids),
            )

            # Process lines in batches
            # Batch size can be increased for better performance (500-1000)
            # but keep lower (250-500) for memory-constrained environments
            (
                start_row,
                tot_debit,
                tot_credit,
                height_available,
            ) = self._process_lines_in_batches(
                move_line_ids,
                report,
                height_available,
                width_available,
                colwidths,
                batch_size=500,
            )

        _logger.info(
            "All batches processed. Adding final balance and completing PDF..."
        )

        # Send notification that we're in final phase (if not in test mode)
        if not self.env.context.get("test_mode"):
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "l10n_it_central_journal.report_progress",
                {
                    "title": _("Generating Central Journal"),
                    "message": _("Finalizing PDF document..."),
                    "progress": 100,
                },
            )
            # Commit so notification is visible immediately
            # pylint: disable=invalid-commit
            self.env.cr.commit()

        # Add final balance
        style_table_line_above = self.get_styles_report_giornale_line()[
            "style_table_line_above"
        ]
        final_balance_data = self.get_balance_data_report_giornale(
            tot_debit, tot_credit, final=True
        )
        final_balance_table = Table(
            final_balance_data, colWidths=colwidths, style=style_table_line_above
        )
        final_balance_table_height = final_balance_table.wrapOn(
            report, width_available, HEIGHT
        )[1]

        # Check if final balance fits on current page
        if height_available - footer_height >= final_balance_table_height:
            height_available -= final_balance_table_height
            final_balance_table.drawOn(report, margin_left, height_available)
        else:
            # Need new page for final balance
            self.get_template_footer_report_giornale(report)
            report.showPage()
            height_available = self.get_template_header_report_giornale(report, HEIGHT)
            height_available -= gap

            # Add column header on new page
            style_table = self.get_styles_report_giornale_line()["style_table"]
            data_header = self.get_data_header_report_giornale()
            header_table = Table(data_header, colWidths=colwidths, style=style_table)
            header_table_height = header_table.wrapOn(report, width_available, HEIGHT)[
                1
            ]
            height_available -= header_table_height
            header_table.drawOn(report, margin_left, height_available)

            # Draw final balance
            height_available -= final_balance_table_height
            final_balance_table.drawOn(report, margin_left, height_available)

        self.get_template_footer_report_giornale(report)

        _logger.info("Finalizing PDF document (this may take a few seconds)...")
        report.save()

        file_base64 = base64.b64encode(pdf_bytes.getvalue())
        self.write({"report_giornale": file_base64})

        return start_row, tot_debit, tot_credit

    def print_giornale_reportlab(self):
        """
        Main button action - starts report generation in background thread
        and closes the wizard immediately.
        In test mode, generates synchronously.
        """
        # In test mode, generate synchronously without threading
        if self.env.context.get("test_mode") or self._context.get("install_mode"):
            self.create_report_giornale_reportlab()
            return {"type": "ir.actions.act_window_close"}

        # Set state to processing BEFORE starting thread
        self.write(
            {
                "generation_state": "processing",
                "generation_progress": 0,
                "generation_error": False,
            }
        )

        # Start background thread for report generation
        wizard_id = self.id
        db_name = self.env.cr.dbname
        uid = self.env.uid
        context = dict(self.env.context)

        # Send initial notification
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {
                "title": _("Generating Central Journal Report"),
                "message": _(
                    "Your report is being generated in the background. "
                    "You will be notified when it's ready for download."
                ),
                "type": "info",
                "sticky": False,
            },
        )

        def generate_in_thread():
            """Run report generation in separate thread with new cursor"""
            try:
                # Small delay to let the main request complete and commit
                time.sleep(0.5)

                with registry(db_name).cursor() as new_cr:
                    env = api.Environment(new_cr, uid, context)
                    wizard = env["wizard.giornale.reportlab"].browse(wizard_id)

                    # Generate the report
                    wizard._generate_report_async()

            except Exception as e:
                # Error already logged and notified by _generate_report_async()
                # Just ensure the state is updated if it wasn't already
                try:
                    with registry(db_name).cursor() as new_cr:
                        env = api.Environment(new_cr, uid, context)
                        wizard = env["wizard.giornale.reportlab"].browse(wizard_id)
                        # Only update if not already in failed state
                        if wizard.generation_state != "failed":
                            wizard.write(
                                {
                                    "generation_state": "failed",
                                    "generation_error": str(e),
                                }
                            )
                            wizard.env.cr.commit()
                except Exception:
                    _logger.error("Failed to update error state", exc_info=True)

        # Start thread immediately
        thread = threading.Thread(target=generate_in_thread)
        thread.daemon = True
        thread.start()

        # Close the wizard immediately
        return {"type": "ir.actions.act_window_close"}

    def _generate_report_async(self):
        """
        Async method that generates the report in background
        """
        try:
            # Log the start
            move_line_ids = self.get_line_reportlab_ids()
            _logger.info(
                "Starting central journal report generation for %d lines "
                "(date range: %s to %s)",
                len(move_line_ids),
                self.date_move_line_from,
                self.date_move_line_to,
            )

            # Generate the report (uses batch processing internally)
            self.create_report_giornale_reportlab()

            # Create ir.attachment from the generated PDF
            filename = (
                f"giornale_{self.date_move_line_from}_{self.date_move_line_to}.pdf"
            )
            attachment = self.env["ir.attachment"].create(
                {
                    "name": filename,
                    "type": "binary",
                    "datas": self.report_giornale,
                    "res_model": self._name,
                    "res_id": self.id,
                    "mimetype": "application/pdf",
                }
            )
            self.write({"attachment_id": attachment.id})

            _logger.info(
                "PDF generation completed, attachment saved for wizard %s",
                self.id,
            )

            # Mark as complete
            self.write(
                {
                    "generation_state": "done",
                    "generation_progress": 100,
                }
            )

            if not self.env.context.get("test_mode"):
                # pylint: disable=invalid-commit
                self.env.cr.commit()

            # From this point on, if process is killed, user can still download
            # the PDF from the wizard form view using the attachment_id

            _logger.info(
                "Preparing download notification for wizard %s (attachment: %d)",
                self.id,
                self.attachment_id.id if self.attachment_id else 0,
            )

            # Try to trigger automatic download, but if this fails the PDF
            # is still accessible via the wizard form
            try:
                self._trigger_download_notification()
            except Exception as e:
                # Log but don't fail - PDF is already saved and accessible
                _logger.warning(
                    "Failed to send download notification (PDF still accessible): %s",
                    str(e),
                )

            _logger.info(
                "Completed central journal report generation for %d lines",
                len(move_line_ids),
            )

        except Exception as e:
            _logger.error(
                "Failed to generate central journal report: %s", str(e), exc_info=True
            )
            self.write(
                {
                    "generation_state": "failed",
                    "generation_error": str(e),
                }
            )
            # Send error notification
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "title": _("Report Generation Failed"),
                    "message": _("Error: %s") % str(e),
                    "type": "danger",
                    "sticky": True,
                },
            )
            # pylint: disable=invalid-commit
            self.env.cr.commit()
            raise

    def _trigger_download_notification(self):
        """
        Send bus notifications to trigger automatic PDF download.
        This is a best-effort attempt - if it fails, the PDF is still
        accessible via the wizard form view.
        """
        if not self.attachment_id:
            _logger.error("Cannot trigger download: no attachment found")
            return

        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        download_url = (
            f"{base_url}/web/content?"
            f"model=ir.attachment&"
            f"id={self.attachment_id.id}&"
            f"field=datas&"
            f"download=true&"
            f"filename={self.attachment_id.name}"
        )

        # Trigger download via custom bus notification
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "l10n_it_central_journal.download_report",
            {
                "url": download_url,
                "filename": self.attachment_id.name,
            },
        )

        # Send success notification
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {
                "title": _("Report Ready"),
                "message": _("Your Central Journal PDF is downloading..."),
                "type": "success",
                "sticky": False,
            },
        )

        # Commit notifications
        if not self.env.context.get("test_mode"):
            # pylint: disable=invalid-commit
            self.env.cr.commit()

    def print_giornale_reportlab_final(self):
        """
        Final print that locks the period - runs in background.
        In test mode, generates synchronously.
        """
        # In test mode, generate synchronously without threading
        if self.env.context.get("test_mode") or self._context.get("install_mode"):
            end_row, end_debit, end_credit = self.create_report_giornale_reportlab()
            # Lock the period
            if (
                not self.company_id.period_lock_date
                or self.company_id.period_lock_date < self.date_move_line_to
            ):
                self.company_id.sudo().period_lock_date = self.date_move_line_to
            # Update date range
            daterange_vals = {
                "date_last_print": self.date_move_line_to,
                "progressive_line_number": end_row,
                "progressive_debit": end_debit,
                "progressive_credit": end_credit,
            }
            self.daterange_id.write(daterange_vals)
            self.write({"print_state": "printed"})
            return {"type": "ir.actions.act_window_close"}

        # Set state to processing
        self.write(
            {
                "generation_state": "processing",
                "generation_progress": 0,
                "generation_error": False,
                "print_state": "print",  # Reset state
            }
        )

        # Start background thread for report generation
        wizard_id = self.id
        db_name = self.env.cr.dbname
        uid = self.env.uid
        context = dict(self.env.context)

        # Send initial notification
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {
                "title": _("Generating Definitive Central Journal Report"),
                "message": _(
                    "Your definitive report is being generated. "
                    "The period will be locked upon completion."
                ),
                "type": "warning",
                "sticky": False,
            },
        )

        def generate_in_thread():
            """Run report generation in separate thread with new cursor"""
            try:
                time.sleep(0.5)

                with registry(db_name).cursor() as new_cr:
                    env = api.Environment(new_cr, uid, context)
                    wizard = env["wizard.giornale.reportlab"].browse(wizard_id)

                    # Generate the report with finalization
                    wizard._generate_report_async_final()

            except Exception as e:
                # Error already logged and notified by _generate_report_async_final()
                # Just ensure the state is updated if it wasn't already
                try:
                    with registry(db_name).cursor() as new_cr:
                        env = api.Environment(new_cr, uid, context)
                        wizard = env["wizard.giornale.reportlab"].browse(wizard_id)
                        # Only update if not already in failed state
                        if wizard.generation_state != "failed":
                            wizard.write(
                                {
                                    "generation_state": "failed",
                                    "generation_error": str(e),
                                }
                            )
                            wizard.env.cr.commit()
                except Exception:
                    _logger.error("Failed to update error state", exc_info=True)

        # Start thread immediately
        thread = threading.Thread(target=generate_in_thread)
        thread.daemon = True
        thread.start()

        # Close the wizard immediately
        return {"type": "ir.actions.act_window_close"}

    def _generate_report_async_final(self):
        """
        Background job for final report with period locking
        """
        try:
            _logger.info(
                "Starting async final central journal report for wizard %s", self.id
            )
            end_row, end_debit, end_credit = self.create_report_giornale_reportlab()

            _logger.info(
                "PDF generation completed, committing report data for wizard %s "
                "(final row: %s, debit: %s, credit: %s)",
                self.id,
                end_row,
                end_debit,
                end_credit,
            )

            # Commit the PDF data immediately
            # pylint: disable=invalid-commit
            self.env.cr.commit()

            # Lock the period
            if (
                not self.company_id.period_lock_date
                or self.company_id.period_lock_date < self.date_move_line_to
            ):
                self.company_id.sudo().period_lock_date = self.date_move_line_to

            # Update date range
            daterange_vals = {
                "date_last_print": self.date_move_line_to,
                "progressive_line_number": end_row,
                "progressive_debit": end_debit,
                "progressive_credit": end_credit,
            }
            self.daterange_id.write(daterange_vals)

            self.write(
                {
                    "generation_state": "done",
                    "generation_progress": 100,
                    "print_state": "printed",
                }
            )
            # pylint: disable=invalid-commit
            self.env.cr.commit()

            # Try to trigger download notification, but if this fails the PDF
            # is still accessible via the wizard form
            try:
                # Send custom success message for final report
                self.env["bus.bus"]._sendone(
                    self.env.user.partner_id,
                    "simple_notification",
                    {
                        "title": _("Definitive Report Ready"),
                        "message": _("Period locked to %s. Your PDF is downloading...")
                        % format_date(self.env, self.date_move_line_to),
                        "type": "success",
                        "sticky": False,
                    },
                )
                # Use the common download notification method
                self._trigger_download_notification()
            except Exception as e:
                # Log but don't fail - PDF is already saved and period is locked
                _logger.warning(
                    "Failed to send download notification for final report "
                    "(PDF still accessible): %s",
                    str(e),
                )

            _logger.info(
                "Completed async final central journal report for wizard %s", self.id
            )

        except Exception as e:
            _logger.error(
                "Failed to generate final central journal report for wizard %s: %s",
                self.id,
                str(e),
                exc_info=True,
            )
            self.write(
                {
                    "generation_state": "failed",
                    "generation_error": str(e),
                }
            )
            # Send notification via bus
            self.env["bus.bus"]._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "title": _("Report Generation Error"),
                    "message": _("Definitive report generation failed: %s") % str(e),
                    "type": "danger",
                    "sticky": True,
                },
            )
            # pylint: disable=invalid-commit
            self.env.cr.commit()
            raise
