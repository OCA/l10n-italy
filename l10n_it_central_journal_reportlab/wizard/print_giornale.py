# Copyright 2018 Gianmarco Conte (gconte@dinamicheaziendali.it)
# Copyright 2022 Giuseppe Borruso (gborruso@dinamicheaziendali.it)
# Copyright 2024 Simone Rubino - Aion Tech
# Copyright 2025 Michele Di Croce - Stesi Consulting

import base64
import gc
import io
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

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import flatten, format_date, formatLang

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
    report_giornale_name = fields.Char(compute="_compute_report_giornale_name")
    group_by_account = fields.Boolean(default=False)

    @api.depends("report_giornale", "daterange_id")
    def _compute_report_giornale_name(self):
        for wizard in self:
            if wizard.report_giornale and wizard.daterange_id:
                wizard.report_giornale_name = (
                    _("Account Central Journal - %s.pdf") % wizard.daterange_id.name
                )
            elif wizard.report_giornale:
                wizard.report_giornale_name = _("Account Central Journal.pdf")
            else:
                wizard.report_giornale_name = False

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
        colwidths = [32, 40, 50, 120, 130, 100, 50, 50]
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

    def get_grupped_final_tables_report_giornale(
        self, list_grupped_line, start_row, width_available
    ):
        """Generator that yields tables one by one to reduce memory usage"""
        style_name = self.get_styles_report_giornale_line()["style_name"]
        style_number = self.get_styles_report_giornale_line()["style_number"]
        style_table = self.get_styles_report_giornale_line()["style_table"]
        style_table_line_above = self.get_styles_report_giornale_line()[
            "style_table_line_above"
        ]
        colwidths = self.get_colwidths_report_giornale(width_available)

        previous_move_name = ""
        list_balance = [
            (0, 0),
            (self.progressive_debit2, self.progressive_credit),
        ]

        processed_count = 0
        current_row = start_row
        for line in list_grupped_line:
            processed_count += 1
            if processed_count % 50000 == 0:  # Memory monitoring every 50000 records
                gc.collect()  # pragma: no cover

            account_name = (
                line["account_code"] + " - " + line["account_name"]
                if line["account_code"]
                else line["account_name"]
            )
            if not account_name:
                continue

            current_row += 1
            row = Paragraph(escape(str(current_row)), style_name)
            date = Paragraph(escape(format_date(self.env, line["date"])), style_name)
            move = Paragraph(escape(line["move_name"]), style_name)
            account = Paragraph(escape(account_name), style_name)
            name = Paragraph(escape(line["name"]), style_name)
            # dato che nel SQL ho la somma dei crediti e debiti potrei avere
            # che un conto ha sia debito che credito
            if line["debit"] > 0:
                debit = Paragraph(
                    escape(formatLang(self.env, line["debit"])), style_number
                )
                credit = Paragraph(escape(formatLang(self.env, 0)), style_number)
                list_balance.append((line["debit"], 0))
                line_data = [[row, date, move, account, name, debit, credit]]

                if previous_move_name != line["move_name"]:
                    previous_move_name = line["move_name"]
                    # pragma: no cover
                    yield (
                        Table(
                            line_data, colWidths=colwidths, style=style_table_line_above
                        ),
                        (line["debit"], 0),
                    )
                else:
                    yield (
                        Table(line_data, colWidths=colwidths, style=style_table),
                        (line["debit"], 0),
                    )

            if line["credit"] > 0:
                debit = Paragraph(escape(formatLang(self.env, 0)), style_number)
                credit = Paragraph(
                    escape(formatLang(self.env, line["credit"])), style_number
                )
                list_balance.append((0, line["credit"]))
                line_data = [[row, date, move, account, name, debit, credit]]

                if previous_move_name != line["move_name"]:
                    previous_move_name = line["move_name"]
                    yield (  # pragma: no cover
                        Table(
                            line_data, colWidths=colwidths, style=style_table_line_above
                        ),
                        (0, line["credit"]),
                    )
                else:
                    yield (
                        Table(line_data, colWidths=colwidths, style=style_table),
                        (0, line["credit"]),
                    )

    def _fetch_line_data_in_chunks(self, move_line_ids, chunk_size=5000):
        """Generator that fetches line data in tuples to reduce memory usage"""
        for i in range(0, len(move_line_ids), chunk_size):
            chunk_ids = move_line_ids[i : i + chunk_size]
            with self.env.registry.cursor() as tmp_cr:
                tmp_cr.execute(
                    """SELECT aml.date, aml.ref, am.name, acc.name as acc_name,
                    p.name as partner_name, aml.name, aml.debit,
                    aml.credit, acc.code as acc_code, acc.account_type
                            FROM account_move_line aml
                            INNER JOIN account_move am on am.id = aml.move_id
                            LEFT JOIN account_account acc on acc.id = aml.account_id
                            LEFT JOIN res_partner p on p.id = aml.partner_id
                            where aml.id in %(line_ids)s
                            ORDER BY am.date, am.name, acc.code""",
                    {"line_ids": tuple(chunk_ids)},
                )
                chunk_data = tmp_cr.fetchall()
                yield from chunk_data
                del chunk_data  # Clear chunk data from memory
            # Force garbage collection after each chunk
            gc.collect()  # pragma: no cover

    def get_final_tables_report_giornale(
        self, move_line_ids, start_row, width_available
    ):
        """Generator that yields tables one by one to reduce memory usage"""
        style_name = self.get_styles_report_giornale_line()["style_name"]
        style_number = self.get_styles_report_giornale_line()["style_number"]
        style_table = self.get_styles_report_giornale_line()["style_table"]
        style_table_line_above = self.get_styles_report_giornale_line()[
            "style_table_line_above"
        ]
        colwidths = self.get_colwidths_report_giornale(width_available)

        previous_move_name = ""
        list_balance = [
            (0, 0),
            (self.progressive_debit2, self.progressive_credit),
        ]
        processed_count = 0
        current_row = start_row
        lang = self.env.lang
        # if l10n_multilang is installed, account_name comes as a dict
        account_name_translated = self.env.ref(
            "account.field_account_account__name"
        ).translate

        for tupled_line in self._fetch_line_data_in_chunks(move_line_ids):
            processed_count += 1
            # Memory monitoring every 50000 records
            if processed_count % 50000 == 0:
                gc.collect()  # pragma: no cover
            current_row += 1
            row = Paragraph(escape(str(current_row)), style_name)
            date = Paragraph(escape(format_date(self.env, tupled_line[0])), style_name)
            ref = Paragraph(escape(str(tupled_line[1] or "")), style_name)
            move_name = tupled_line[2] or ""
            move = Paragraph(escape(move_name), style_name)
            account_name = (
                (
                    tupled_line[3]
                    and (
                        tupled_line[3].get(lang)
                        or tupled_line[3].get("en_GB")
                        or next(iter(tupled_line[3].values()))
                    )
                    or ""
                )
                if account_name_translated
                else (tupled_line[3] or "")
            )
            account_name = (
                f"{tupled_line[8]} - {account_name}" if tupled_line[8] else account_name
            )
            # evitiamo che i caratteri < o > vengano interpretato come tag html
            # dalla libreria reportlab
            account = Paragraph(escape(account_name), style_name)
            if tupled_line[9] in [
                "asset_receivable",
                "liability_payable",
            ]:
                name = Paragraph(escape(str(tupled_line[4] or "")), style_name)
            else:
                name = Paragraph(escape(str(tupled_line[5] or "")), style_name)
            debit = Paragraph(
                escape(formatLang(self.env, tupled_line[6])), style_number
            )
            credit = Paragraph(
                escape(formatLang(self.env, tupled_line[7])), style_number
            )
            list_balance.append((tupled_line[6], tupled_line[7]))
            line_data = [[row, date, ref, move, account, name, debit, credit]]
            if previous_move_name != move_name:
                previous_move_name = move_name
                # pragma: no cover
                yield (
                    Table(line_data, colWidths=colwidths, style=style_table_line_above),
                    (tupled_line[6], tupled_line[7]),
                )
            else:
                yield (
                    Table(line_data, colWidths=colwidths, style=style_table),
                    (tupled_line[6], tupled_line[7]),
                )

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
        pdf_bytes = io.BytesIO()

        WIDTH, HEIGHT = A4
        width_available = WIDTH - (2 * margin_left)
        height_available = HEIGHT
        report = canvas.Canvas(pdf_bytes, pagesize=A4)
        height_available = self.get_template_header_report_giornale(
            report, height_available
        )

        style_table = self.get_styles_report_giornale_line()["style_table"]
        style_table_line_above = self.get_styles_report_giornale_line()[
            "style_table_line_above"
        ]

        colwidths = self.get_colwidths_report_giornale(width_available)
        data_header = self.get_data_header_report_giornale()
        header_table = Table(data_header, colWidths=colwidths, style=style_table)
        initial_balance_data = self.get_initial_balance_data_report_giornale()
        initial_balance_table = Table(
            initial_balance_data, colWidths=colwidths, style=style_table
        )

        # Draw header and initial balance
        header_table_width, header_table_height = header_table.wrapOn(
            report, width_available, HEIGHT
        )
        height_available -= header_table_height
        header_table.drawOn(report, margin_left, height_available)

        (
            initial_balance_table_width,
            initial_balance_table_height,
        ) = initial_balance_table.wrapOn(report, width_available, HEIGHT)
        height_available -= initial_balance_table_height
        initial_balance_table.drawOn(report, margin_left, height_available)

        start_row = self.start_row
        tot_debit = self.progressive_debit2
        tot_credit = self.progressive_credit

        # Get the table generator
        if self.group_by_account:
            list_grupped_line = self.get_grupped_line_reportlab_ids()
            if not list_grupped_line:
                raise UserError(_("No documents found in the current selection"))
            table_generator = self.get_grupped_final_tables_report_giornale(
                list_grupped_line, start_row, width_available
            )
        else:
            move_line_ids = self.get_line_reportlab_ids()
            if not move_line_ids:
                raise UserError(_("No documents found in the current selection"))
            table_generator = self.get_final_tables_report_giornale(
                move_line_ids, start_row, width_available
            )

        height_available -= gap
        processed_count = 0
        final_row = start_row

        # Process tables as they're generated
        for table, (debit, credit) in table_generator:
            processed_count += 1
            final_row += 1  # Track the final row number
            # Memory monitoring every 50000 records
            if processed_count % 50000 == 0:
                gc.collect()  # pragma: no cover

            table_width, table_height = table.wrapOn(report, width_available, HEIGHT)

            # Check if we need a new page
            if height_available - footer_height < table_height:
                # Add balance before page break
                balance_data = self.get_balance_data_report_giornale(
                    tot_debit, tot_credit, final=False
                )
                table_balance = Table(
                    balance_data, colWidths=colwidths, style=style_table_line_above
                )
                table_balance_width, table_balance_height = table_balance.wrapOn(
                    report, WIDTH, HEIGHT
                )
                height_available -= table_balance_height
                table_balance.drawOn(report, margin_left, height_available)
                self.get_template_footer_report_giornale(report)

                # Start new page
                report.showPage()
                height_available = self.get_template_header_report_giornale(
                    report, HEIGHT
                )
                height_available -= gap

                # Redraw header on new page
                header_table = Table(
                    data_header, colWidths=colwidths, style=style_table
                )
                header_table_width, header_table_height = header_table.wrapOn(
                    report, WIDTH, HEIGHT
                )
                height_available -= header_table_height
                header_table.drawOn(report, margin_left, height_available)

                # Redraw balance on new page
                table_balance = Table(
                    balance_data, colWidths=colwidths, style=style_table
                )
                table_balance.wrapOn(report, WIDTH, HEIGHT)
                height_available -= table_balance_height
                table_balance.drawOn(report, margin_left, height_available)

            # Update running totals
            tot_debit += debit
            tot_credit += credit

            # Draw the table
            height_available -= table_height
            table.drawOn(report, margin_left, height_available)

            # Force garbage collection periodically
            if processed_count % 10000 == 0:
                gc.collect()  # pragma: no cover

        # Calculate final row number based on processed count
        final_row = start_row + processed_count

        # Add final balance
        final_balance_data = self.get_balance_data_report_giornale(
            tot_debit, tot_credit, final=True
        )
        final_balance_table = Table(
            final_balance_data, colWidths=colwidths, style=style_table_line_above
        )
        (
            final_balance_table_width,
            final_balance_table_height,
        ) = final_balance_table.wrapOn(report, WIDTH, HEIGHT)

        if height_available - footer_height >= final_balance_table_height:
            height_available -= final_balance_table_height
            final_balance_table.drawOn(report, margin_left, height_available)
        else:
            self.get_template_footer_report_giornale(report)

            report.showPage()
            height_available = self.get_template_header_report_giornale(report, HEIGHT)
            height_available -= gap
            header_table = Table(data_header, colWidths=colwidths, style=style_table)
            header_table_width, header_table_height = header_table.wrapOn(
                report, WIDTH, HEIGHT
            )
            height_available -= header_table_height
            header_table.drawOn(report, margin_left, height_available)
            height_available -= header_table_height + final_balance_table_height
            final_balance_table.drawOn(report, margin_left, height_available)

        self.get_template_footer_report_giornale(report)
        report.showPage()
        report.save()

        file_base64 = base64.b64encode(pdf_bytes.getvalue())
        self.write({"report_giornale": file_base64})

        return final_row, tot_debit, tot_credit

    def print_giornale_reportlab(self):
        self.create_report_giornale_reportlab()

        view_id = self.env.ref(
            "l10n_it_central_journal_reportlab.wizard_giornale_reportlab",
            raise_if_not_found=False,
        )

        return {
            "view_id": view_id.id,
            "view_mode": "form",
            "res_model": "wizard.giornale.reportlab",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "target": "new",
        }

    def print_giornale_reportlab_final(self):
        end_row, end_debit, end_credit = self.create_report_giornale_reportlab()

        if (
            not self.company_id.period_lock_date
            or self.company_id.period_lock_date < self.date_move_line_to
        ):
            self.company_id.sudo().period_lock_date = self.date_move_line_to

        daterange_vals = {
            "date_last_print": self.date_move_line_to,
            "progressive_line_number": end_row,
            "progressive_debit": end_debit,
            "progressive_credit": end_credit,
        }
        self.daterange_id.write(daterange_vals)

        view_id = self.env.ref(
            "l10n_it_central_journal_reportlab.wizard_giornale_reportlab",
            raise_if_not_found=False,
        )

        return {
            "view_id": view_id.id,
            "view_mode": "form",
            "res_model": "wizard.giornale.reportlab",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "target": "new",
        }
