# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round


def format_x(value, length):
    """
    Format for alphanumeric characters.

    > i dati alfanumerici (rappresentati con “X”) vanno allineati a sinistra,
    > riempiendo il campo, ove occorra, di spazi non significativi a destra;

    :param value: value to be formatted
    :param length: length of the formatted field
    :return: formatted value
    """
    value = str(value or "")[:length]  # Formatting only sets minimum width
    return ("{: <" + str(length) + "}").format(value)


def format_9(value, length):
    """
    Format for numeric characters.

    > i dati numerici (rappresentati con “9”) vanno allineati a destra,
    > riempiendo il campo, ove occorra, di zeri non significativi a sinistra.

    :param value: value to be formatted
    :param length: length of the formatted field
    :return: formatted value
    """
    value = str(value or "")[:length]  # Formatting only sets minimum width
    return ("{:0>" + str(length) + "}").format(value)


class AccountIntrastatStatement(models.Model):
    _name = "account.intrastat.statement"
    _description = "Intrastat Statement"
    _rec_name = "number"

    def round_min_amount(self, amount, company=None, prec_digits=None, truncate=False):
        """
        Return an integer representing `amount`,
        ready for usage in the statement.

        :param amount: Amount to be edited
        :param company: Company to be used for fetching minimal value,
                        if not present the statement's company is used
        :param prec_digits: Digits to be used for rounding,
                            if not present it is rounded to the unit
        :param truncate: True if the float number
                         has to be truncated, otherwise it is rounded
        :return: An integer representing `amount`
        """
        self.ensure_one()
        if company is None:
            company = self.company_id

        if prec_digits:
            round_amount = float_round(amount, precision_digits=prec_digits)
        else:
            round_amount = float_round(amount, precision_digits=0)

        if truncate:
            round_amount = int(round_amount)
        else:
            round_amount = int(float_round(round_amount, precision_digits=0))

        return max(round_amount or 1, company.intrastat_min_amount)

    def _compute_amount_section(self, section_type, section_number):
        """
        Compute operation_number and amount for specified section.

        :param section_type: 'purchase' or 'sale'
        :param section_number: 1..4
        """
        section_ids_field = self.get_section_field_name(section_type, section_number)
        section_op_number_field = "{}_section{}_operation_number".format(
            section_type,
            section_number,
        )
        section_op_amount_field = "{}_section{}_operation_amount".format(
            section_type,
            section_number,
        )
        if any(
            field_name not in self._fields
            for field_name in [
                section_ids_field,
                section_op_number_field,
                section_op_amount_field,
            ]
        ):
            raise UserError(
                _(
                    "Wrong section type %(section_type)s or number %(section_number)s",
                    section_type=section_type,
                    section_number=section_number,
                )
            )
        for statement in self:
            op_number = len(statement[section_ids_field])
            op_amount = statement[section_ids_field].get_amount_euro()
            statement.update(
                {section_op_number_field: op_number, section_op_amount_field: op_amount}
            )

    @api.depends("sale_section1_ids.amount_euro")
    def _compute_amount_sale_s1(self):
        self._compute_amount_section("sale", 1)

    @api.depends("sale_section2_ids.amount_euro")
    def _compute_amount_sale_s2(self):
        self._compute_amount_section("sale", 2)

    @api.depends("sale_section3_ids.amount_euro")
    def _compute_amount_sale_s3(self):
        self._compute_amount_section("sale", 3)

    @api.depends("sale_section4_ids.amount_euro")
    def _compute_amount_sale_s4(self):
        self._compute_amount_section("sale", 4)

    @api.depends("purchase_section1_ids.amount_euro")
    def _compute_amount_purchase_s1(self):
        self._compute_amount_section("purchase", 1)

    @api.depends("purchase_section2_ids.amount_euro")
    def _compute_amount_purchase_s2(self):
        self._compute_amount_section("purchase", 2)

    @api.depends("purchase_section3_ids.amount_euro")
    def _compute_amount_purchase_s3(self):
        self._compute_amount_section("purchase", 3)

    @api.depends("purchase_section4_ids.amount_euro")
    def _compute_amount_purchase_s4(self):
        self._compute_amount_section("purchase", 4)

    @api.model
    def _compute_progressive(self):
        # From last statement
        st = self.search([], order="number desc", limit=1)
        return (st.number or 0) + 1

    def recompute_sequence_lines(self):
        for statement in self:
            for section_type in ["purchase", "sale"]:
                for section_number in range(1, 5):
                    section_field = self.get_section_field_name(
                        section_type, section_number
                    )
                    section = statement[section_field]
                    sequence = 1
                    for line in section:
                        line.sequence = sequence
                        sequence += 1

    @api.model
    def _get_sequence(self):
        return self.env["ir.sequence"].next_by_code("intrastat.statement.sequence")

    number = fields.Integer(default=_compute_progressive)
    date = fields.Date(
        string="Submission Date", default=fields.Date.today(), required=True
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company.id,
        required=True,
    )
    vat_taxpayer = fields.Char(
        string="Taxpayer VAT Number",
        required=True,
        default=lambda self: self.env.company.partner_id.vat
        and self.env.company.partner_id.vat[2:]
        or False,
    )
    intrastat_vat_delegate = fields.Char(
        string="Delegate VAT Number",
        default=lambda self: self.env.company.intrastat_delegated_vat,
    )
    intrastat_name_delegate = fields.Char(
        string="Delegate Name",
        default=lambda self: self.env.company.intrastat_delegated_name,
    )
    fiscalyear = fields.Integer(
        string="Year", required=True, default=fields.Date.today().year
    )
    period_type = fields.Selection(
        selection=[
            ("M", "Month"),
            ("T", "Quarter"),
        ],
        default="M",
        required=True,
    )
    period_number = fields.Integer(
        string="Period",
        help="Values accepted:\n" " - Month : From 1 to 12\n" " - Quarter: From 1 to 4",
        default=1,
        required=True,
    )
    date_start = fields.Date(
        string="Start Date", store=True, readonly=True, compute="_compute_dates"
    )
    date_stop = fields.Date(
        string="Stop Date", store=True, readonly=True, compute="_compute_dates"
    )
    content_type = fields.Selection(
        selection=[
            ("0", "Normal Period"),
            ("8", "Change Period in quarter: only first month operations"),
            (
                "9",
                "Change Period in quarter: only first and second month " "operations",
            ),
        ],
        required=True,
        default="0",
    )
    special_cases = fields.Selection(
        selection=[
            ("7", "First Statement Submitted"),
            ("8", "Ceasing Activity or Changing VAT Number"),
            ("9", "First Statement in Ceasing Activity or Changing VAT Number"),
            ("0", "None of the above cases"),
        ],
        required=True,
        default="0",
    )
    intrastat_custom_id = fields.Many2one(
        comodel_name="account.intrastat.custom",
        string="Customs Section",
        required=True,
        default=lambda self: self.env.company.intrastat_custom_id,
    )
    sale = fields.Boolean(string="Sales", default=True)
    purchase = fields.Boolean(string="Purchases", default=True)
    exclude_optional_column_sect_1_3 = fields.Boolean(
        "Exclude supplier data",
        help="Exclude supplier country, TIN and currency amount from statement",
    )
    intrastat_type_data = fields.Selection(
        selection=[
            ("all", "All (Fiscal and Statistic)"),
            ("fiscal", "Fiscal"),
            ("statistic", "Statistic"),
        ],
        string="Data Type",
        required=True,
        default="all",
    )
    intrastat_code_type = fields.Selection(
        selection=[("service", "Service"), ("good", "Goods")],
        string="Code Type",
        required=True,
        default="good",
    )

    sale_statement_sequence = fields.Integer(
        string="Sales Statement Sequence", default=_get_sequence
    )
    sale_section1_ids = fields.One2many(
        comodel_name="account.intrastat.statement.sale.section1",
        inverse_name="statement_id",
        string="Sales - Section 1",
    )
    sale_section1_operation_number = fields.Integer(
        string="Operation Count - Sales Section 1",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s1",
    )
    sale_section1_operation_amount = fields.Integer(
        string="Operation Amount - Sales Section 1",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s1",
    )
    sale_section2_ids = fields.One2many(
        comodel_name="account.intrastat.statement.sale.section2",
        inverse_name="statement_id",
        string="Sales - Section 2",
    )
    sale_section2_operation_number = fields.Integer(
        string="Operation Count - Sales Section 2",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s2",
    )
    sale_section2_operation_amount = fields.Integer(
        string="Operation Amount - Sales Section 2",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s2",
    )
    sale_section3_ids = fields.One2many(
        comodel_name="account.intrastat.statement.sale.section3",
        inverse_name="statement_id",
        string="Sales - Section 3",
    )
    sale_section3_operation_number = fields.Integer(
        string="Operation Count - Sales Section 3",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s3",
    )
    sale_section3_operation_amount = fields.Integer(
        string="Operation Amount - Sales Section 3",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s3",
    )
    sale_section4_ids = fields.One2many(
        comodel_name="account.intrastat.statement.sale.section4",
        inverse_name="statement_id",
        string="Sales - Section 4",
    )
    sale_section4_operation_number = fields.Integer(
        string="Operation Count - Sales Section 4",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s4",
    )
    sale_section4_operation_amount = fields.Integer(
        string="Operation Amount - Sales Section 4",
        store=True,
        readonly=True,
        compute="_compute_amount_sale_s4",
    )

    purchase_statement_sequence = fields.Integer(
        string="Purchases Statement Sequence", default=_get_sequence
    )
    purchase_section1_ids = fields.One2many(
        comodel_name="account.intrastat.statement.purchase.section1",
        inverse_name="statement_id",
        string="Purchases - Section 1",
    )
    purchase_section1_operation_number = fields.Integer(
        string="Operation Count - Purchases Section 1",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s1",
    )
    purchase_section1_operation_amount = fields.Integer(
        string="Operation Amount - Purchases Section 1",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s1",
    )
    purchase_section2_ids = fields.One2many(
        comodel_name="account.intrastat.statement.purchase.section2",
        inverse_name="statement_id",
        string="Purchases - Section 2",
    )
    purchase_section2_operation_number = fields.Integer(
        string="Operation Count - Purchases Section 2",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s2",
    )
    purchase_section2_operation_amount = fields.Integer(
        string="Operation Amount - Purchases Section 2",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s2",
    )
    purchase_section3_ids = fields.One2many(
        comodel_name="account.intrastat.statement.purchase.section3",
        inverse_name="statement_id",
        string="Purchases - Section 3",
    )
    purchase_section3_operation_number = fields.Integer(
        string="Operation Count - Purchases Section 3",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s3",
    )
    purchase_section3_operation_amount = fields.Integer(
        string="Operation Amount - Purchases Section 3",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s3",
    )
    purchase_section4_ids = fields.One2many(
        comodel_name="account.intrastat.statement.purchase.section4",
        inverse_name="statement_id",
        string="Purchases - Section 4",
    )
    purchase_section4_operation_number = fields.Integer(
        string="Operation Count - Purchases Section 4",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s4",
    )
    purchase_section4_operation_amount = fields.Integer(
        string="Operation Amount - Purchases Section 4",
        store=True,
        readonly=True,
        compute="_compute_amount_purchase_s4",
    )

    @api.model_create_multi
    def create(self, vals_list):
        statements = super().create(vals_list)
        for statement in statements:
            statement._normalize_statement()
        return statements

    def write(self, vals):
        res = super().write(vals)
        self._normalize_statement()
        self.recompute_sequence_lines()
        return res

    @api.depends("fiscalyear", "period_type", "period_number")
    def _compute_dates(self):
        for statement in self:
            if (
                not statement.fiscalyear
                or not statement.period_type
                or not statement.period_number
            ):
                continue

            statement._constrain_period_number()

            period_date_start, period_date_stop = statement.get_dates_start_stop()

            statement.date_start = fields.Date.to_date(period_date_start)
            statement.date_stop = fields.Date.to_date(period_date_stop)

    def get_dates_start_stop(self):
        self.ensure_one()
        year = self.fiscalyear
        period_date_start = date(year, 1, 1)
        period_date_stop = date(year, 12, 31)

        if self.period_type == "M":
            month = self.period_number
            period_date_start = date(year, month, 1)
            period_date_stop = (
                datetime(year, month, 1) + relativedelta(months=1) - timedelta(days=1)
            )
        elif self.period_type == "T":
            quarter = self.period_number
            month_start = int(12 / 4 * (quarter - 1) + 1)
            period_date_start = date(year, month_start, 1)
            period_date_stop = (
                period_date_start + relativedelta(months=3) - timedelta(days=1)
            )
        return period_date_start, period_date_stop

    def _get_period_ref(self):
        self.ensure_one()
        res = {"year_id": self.fiscalyear}

        # Month/Quarter
        if self.period_type == "T":
            res.update({"quarterly": self.period_number})
        elif self.period_type == "M":
            res.update({"month": self.period_number})
        return res

    def _normalize_statement(self):
        # Unlink lines sale/purchase sections
        self.ensure_one()
        if not self.sale:
            self._unlink_sections(section_type="sale")
        if not self.purchase:
            self._unlink_sections(section_type="purchase")
        return True

    def _unlink_sections(self, section_type="all"):
        """
        Unlink lines sale/purchase sections.

        :param section_type: 'all' (default), 'sale' or 'purchase'
        """
        self.ensure_one()
        # sale
        if section_type in ["all", "sale"]:
            self.sale_section1_ids.unlink()
            self.sale_section2_ids.unlink()
            self.sale_section3_ids.unlink()
            self.sale_section4_ids.unlink()
        # purchase
        if section_type in ["all", "purchase"]:
            self.purchase_section1_ids.unlink()
            self.purchase_section2_ids.unlink()
            self.purchase_section3_ids.unlink()
            self.purchase_section4_ids.unlink()
        return True

    def _get_progressive_interchange(self):
        self.ensure_one()
        prg = 0
        domain = [("date", "=", self.date)]
        for st in self.search(domain):
            prg += 1
            if st.id == self.id:
                break
        return prg

    @api.model
    def _get_file_name(self):
        """Format UA code + %m + %d"""

        # Calcolo progressivo interchange
        prg = self._get_progressive_interchange()
        if self.env.context.get("export_filename"):
            return self.env.context.get("export_filename")
        if self.company_id.intrastat_export_file_name:
            return self.company_id.intrastat_export_file_name
        else:
            return "{}{}{}.{}{}".format(
                self.company_id.intrastat_ua_code or "",
                f"{str(self.date.month).zfill(2):2s}",
                f"{str(self.date.day).zfill(2):2s}",
                "I",  # doc intrastat
                f"{str(prg).zfill(2):2s}",
            )

    def _prepare_export_head(self):
        self.ensure_one()

        rcd = ""
        # Codice utente abilitato (mittente)
        rcd += format_x(self.company_id.intrastat_ua_code, 4)
        # Riservato a SDA
        rcd += format_x("", 12)
        # Nome del flusso
        rcd += format_x(self._get_file_name(), 12)
        # Riservato a SDA
        rcd += format_x("", 12)
        # Codice sezione doganale presso la quale si effettua l'operazione
        rcd += format_x(self.intrastat_custom_id.code, 6)
        # Riservato a SDA
        rcd += format_x("", 4)
        # Codice fiscale o numero partita IVA o codice spedizioniere del
        # richiedente (utente autorizzato)
        # Partita IVA del presentatore o delegato
        vat_applicant = self.intrastat_vat_delegate or self.vat_taxpayer
        rcd += format_x(vat_applicant.replace(" ", ""), 16)
        # Progressivo sede utente autorizzato
        prg = self._get_progressive_interchange()
        rcd += format_9(prg, 3)
        # Riservato a SDA
        rcd += format_x("", 1)
        # Numero di record presenti nel flusso
        tot_lines = (
            self.sale_section1_operation_number
            + self.sale_section2_operation_number
            + self.sale_section3_operation_number
            + self.sale_section4_operation_number
            + self.purchase_section1_operation_number
            + self.purchase_section2_operation_number
            + self.purchase_section3_operation_number
            + self.purchase_section4_operation_number
            + 1
        )  # this rec
        # Add frontispiece sale
        if (
            self.sale_section1_operation_number
            or self.sale_section2_operation_number
            or self.sale_section3_operation_number
            or self.sale_section4_operation_number
        ):
            tot_lines += 1
        # Add frontispiece purchase
        if (
            self.purchase_section1_operation_number
            or self.purchase_section2_operation_number
            or self.purchase_section3_operation_number
            or self.purchase_section4_operation_number
        ):
            tot_lines += 1
        rcd += format_9(tot_lines, 5)

        rcd += "\r\n"
        return rcd

    def _prepare_export_prefix(self, ref_number, line=None):
        """
        Fixed part for every line of the exported file

        :param ref_number: number of the listing
        :param line: statement line, if None this is the frontispiece's prefix
        :return: Prefix for all statement lines
        """
        self.ensure_one()
        is_frontispiece = not bool(line)
        # Campo fisso: “EUROX”
        prefix = format_x("EUROX", 5)

        # Partita IVA del presentatore (soggetto obbligato o soggetto delegato)
        vat_applicant = self.intrastat_vat_delegate or self.vat_taxpayer
        prefix += format_9(vat_applicant, 11)

        # Numero di riferimento dell’elenco
        prefix += format_9(ref_number, 6)

        # Tipo record:
        #  0 = frontespizio
        #  1 = righe dettaglio sezione 1
        #  2 = righe dettaglio sezione 2
        #  3 = righe dettaglio sezione 3
        #  4 = righe dettaglio sezione 4
        if is_frontispiece:
            record_type = 0
        else:
            record_type = line.get_section_number()
        prefix += format_9(record_type, 1)

        # Numero progressivo di riga dettaglio all’interno
        # delle sezioni 1, 2, 3 e 4, viene impostato a zero
        # solo nel record frontespizio
        if is_frontispiece:
            prog_number = 0
        else:
            prog_number = line.sequence
        prefix += format_9(prog_number, 5)
        return prefix

    @api.model
    def _format_negative_number_frontispiece(self, number):
        if number >= 0:
            return str(number)
        # interchange last values with p for 0, q for 1 ...and y for 9
        interchange = ["p", "q", "r", "s", "t", "u", "v", "w", "x", "y"]
        last_char = str(number)[-1:]
        number = list(str(number * -1))
        # change last number
        number[len(number) - 1] = interchange[int(last_char)]
        return "".join(number)

    def _prepare_export_frontispiece(self, kind, ref_number):
        self.ensure_one()
        rcd = self._prepare_export_prefix(ref_number)
        # Tipo riepilogo: A = acquisti C = cessioni
        summary_type = None
        if kind == "purchase":
            summary_type = "A"
        elif kind == "sale":
            summary_type = "C"
        rcd += format_x(summary_type, 1)
        # Anno
        rcd += format_9(str(self.fiscalyear)[-2:], 2)
        # Periodicità
        rcd += format_x(self.period_type, 1)
        # Periodo
        rcd += format_9(self.period_number, 2)
        # Partita IVA del contribuente
        rcd += format_9(self.vat_taxpayer, 11)
        # Contenuto degli elenchi
        rcd += format_9(self.content_type, 1)
        # Casi particolari riferiti al soggetto obbligato
        rcd += format_9(self.special_cases, 1)
        # Partita IVA del soggetto delegato
        rcd += format_9(self.intrastat_vat_delegate, 11)
        for section_number in range(1, 5):
            section_op_number_field = f"{kind}_section{section_number}_operation_number"
            rcd += format_9(self[section_op_number_field], 5)

            section_op_amount_field = f"{kind}_section{section_number}_operation_amount"
            amount = self[section_op_amount_field]
            if section_number == 2:
                amount = self._format_negative_number_frontispiece(amount)
            rcd += format_9(amount, 13)
        # Aggiunti segnaposti per sezione 5. non supportata
        if kind == "sale":
            rcd += format_9(0, 5)

        rcd += "\r\n"
        return rcd

    def generate_file_export(self):
        self.ensure_one()
        file_content = ""
        # Head
        if not self.env.context.get("export_without_head"):
            file_content += self._prepare_export_head()
        content_sale = self.env.context.get("sale")
        content_purchase = self.env.context.get("purchase")
        # Purchase
        if (
            self.purchase_section1_operation_number
            or self.purchase_section2_operation_number
            or self.purchase_section3_operation_number
            or self.purchase_section4_operation_number
        ) and content_purchase:
            ref_number = self.purchase_statement_sequence
            # frontispiece
            file_content += self._prepare_export_frontispiece("purchase", ref_number)
            # Section 1
            purchase_lines = [
                self.purchase_section1_ids,
                self.purchase_section2_ids,
                self.purchase_section3_ids,
                self.purchase_section4_ids,
            ]
            for section_lines in purchase_lines:
                for line in section_lines:
                    rcd = self._prepare_export_prefix(ref_number, line)
                    rcd += line._prepare_export_line()
                    file_content += rcd
        # Sale
        if (
            self.sale_section1_operation_number
            or self.sale_section2_operation_number
            or self.sale_section3_operation_number
            or self.sale_section4_operation_number
        ) and content_sale:
            ref_number = self.sale_statement_sequence
            # frontispiece
            file_content += self._prepare_export_frontispiece("sale", ref_number)
            sale_lines = [
                self.sale_section1_ids,
                self.sale_section2_ids,
                self.sale_section3_ids,
                self.sale_section4_ids,
            ]
            for section_lines in sale_lines:
                for line in section_lines:
                    rcd = self._prepare_export_prefix(ref_number, line)
                    rcd += line._prepare_export_line()
                    file_content += rcd

        # Data validation
        if not file_content:
            raise ValidationError(_("Nothing to export"))
        if (
            not self.sale_section1_ids
            and not self.sale_section2_ids
            and not self.sale_section3_ids
            and not self.sale_section4_ids
            and not self.purchase_section1_ids
            and not self.purchase_section2_ids
            and not self.purchase_section3_ids
            and not self.purchase_section4_ids
        ):
            raise ValidationError(_("Statement without lines"))

        return file_content

    def compute_statement(self):
        self.ensure_one()
        # Unlink existing lines
        self._unlink_sections()

        # Setting period
        period_date_start, period_date_stop = self.get_dates_start_stop()

        # Search intrastat lines
        domain = [
            ("invoice_date", ">=", period_date_start),
            ("invoice_date", "<=", period_date_stop),
            ("intrastat", "=", True),
        ]
        inv_type = []
        if self.sale:
            inv_type += ["out_invoice", "out_refund"]
        if self.purchase:
            inv_type += ["in_invoice", "in_refund"]
        domain.append(("move_type", "in", inv_type))

        statement_data = dict()
        invoices = self.env["account.move"].search(domain)

        for inv_intra_line in invoices.mapped("intrastat_line_ids"):
            for section_type in ["purchase", "sale"]:
                for section_number in range(1, 5):
                    section_details = (section_type, section_number)
                    statement_section = "{}_s{}".format(*section_details)
                    if inv_intra_line.statement_section != statement_section:
                        continue
                    statement_section_model_name = self.get_section_model(
                        *section_details
                    )
                    st_line = self.env[
                        statement_section_model_name
                    ]._prepare_statement_line(inv_intra_line, self)
                    if not st_line:
                        continue
                    statement_section_field = self.get_section_field_name(
                        *section_details
                    )
                    if statement_section_field not in statement_data:
                        statement_data[statement_section_field] = list()
                    st_line["sequence"] = (
                        len(statement_data[statement_section_field]) + 1
                    )
                    statement_data[statement_section_field].append((0, 0, st_line))

        self.write(statement_data)
        # Group refund to sale lines if they have the same period of ref
        refund_map = [
            (2, 1),  # Sale (Purchase) section 2 refunds section 1
            (4, 3),  # Sale (Purchase) section 4 refunds section 3
        ]
        for section_type in ["purchase", "sale"]:
            for section_number, refund_section_number in refund_map:
                section_details = (section_type, section_number)
                refund_section_details = (section_type, refund_section_number)
                section_field = self.get_section_field_name(*section_details)
                for line in self[section_field]:
                    refund_section_model = self.get_section_model(
                        *refund_section_details
                    )
                    to_refund_model = self.env[refund_section_model]
                    self.refund_line(line, to_refund_model)
        return True

    @staticmethod
    def get_section_model(section_type, section_number):
        return f"account.intrastat.statement.{section_type}.section{section_number}"

    @staticmethod
    def get_section_field_name(section_type, section_number):
        return f"{section_type}_section{section_number}_ids"

    def refund_line(self, line, to_ref_obj):
        """Refund line into sale if period ref is the same of the statement"""
        self.ensure_one()
        to_refund = False
        if line.year_id == self.fiscalyear:
            if self.period_type == "M" and line.month == self.period_number:
                to_refund = True

            if self.period_type == "T" and line.quarterly == self.period_number:
                to_refund = True
        # Execute refund
        if to_refund:
            domain = [
                ("statement_id", "=", self.id),
                ("partner_id", "=", line.partner_id.id),
                ("intrastat_code_id", "=", line.intrastat_code_id.id),
                ("amount_euro", ">=", line.amount_euro),
            ]
            line_to_refund = to_ref_obj.search(domain, limit=1)
            if line_to_refund:
                if line_to_refund.amount_euro < line.amount_euro:
                    raise ValidationError(
                        _(
                            "Invoice and credit note in the same period with"
                            " credit note > invoice for partner %s"
                        )
                        % line.partner_id.name
                    )
                val = {"amount_euro": (line_to_refund.amount_euro - line.amount_euro)}
                if "statistic_amount_euro" in line_to_refund:
                    val["statistic_amount_euro"] = (
                        line_to_refund.statistic_amount_euro
                        - line.statistic_amount_euro
                    )
                if "amount_currency" in line_to_refund:
                    val["amount_currency"] = (
                        line_to_refund.amount_currency - line.amount_currency
                    )

                line_to_refund.write(val)
                line.unlink()

    @api.onchange("company_id")
    def change_company_id(self):
        self.vat_taxpayer = (
            self.company_id.partner_id.vat
            and self.company_id.partner_id.vat[2:]
            or False
        )
        self.intrastat_vat_delegate = self.company_id.intrastat_delegated_vat or False

    @api.constrains("period_type", "period_number")
    def _constrain_period_number(self):
        for statement in self:
            if statement.period_type == "M" and not (
                1 <= statement.period_number <= 12
            ):
                raise ValidationError(
                    _("Period Not Valid! Range accepted: from 1 to 12")
                )
            if statement.period_type == "T" and not (1 <= statement.period_number <= 4):
                raise ValidationError(
                    _("Period Not Valid! Range accepted: from 1 to 4")
                )
