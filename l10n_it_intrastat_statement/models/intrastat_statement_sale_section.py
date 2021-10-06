#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .intrastat_statement import format_9, format_x


class IntrastatStatementSaleSection(models.AbstractModel):
    _inherit = "account.intrastat.statement.section"
    _name = "account.intrastat.statement.sale.section"
    _description = "Fields and methods " "common to all Intrastat sale sections"

    @api.model
    def get_section_type(self):
        return "sale"

    @api.model
    def _default_transaction_nature_id(self):
        company_id = self.env.context.get("company_id", self.env.company)
        return company_id.intrastat_sale_transaction_nature_id


class IntrastatStatementSaleSection1(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section1"
    _description = "Intrastat Statement - Sales Section 1"

    transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Transaction Nature",
        default=lambda m: m._default_transaction_nature_id(),
    )
    weight_kg = fields.Integer(string="Net Mass (kg)")
    additional_units = fields.Integer(string="Additional Units")
    additional_units_required = fields.Boolean(
        string="Additional Unit Required",
        store=True,
        related="intrastat_code_id.additional_unit_required",
    )
    additional_units_uom = fields.Char(
        string="Additional Unit of Measure",
        readonly=True,
        related="intrastat_code_id.additional_unit_uom_id.name",
    )
    statistic_amount_euro = fields.Integer(string="Statistic Value in Euro")
    delivery_code_id = fields.Many2one(
        comodel_name="account.incoterms", string="Delivery Terms"
    )
    transport_code_id = fields.Many2one(
        comodel_name="account.intrastat.transport", string="Transport Mode"
    )
    country_destination_id = fields.Many2one(
        comodel_name="res.country", string="Destination Country"
    )
    province_origin_id = fields.Many2one(
        comodel_name="res.country.state", string="Origin Province"
    )

    @api.model
    def get_section_number(self):
        return 1

    def apply_partner_data(self, partner_data):
        res = super(IntrastatStatementSaleSection1, self).apply_partner_data(
            partner_data
        )
        if "country_destination_id" in partner_data:
            self.country_destination_id = partner_data["country_destination_id"]
        return res

    @api.onchange("weight_kg")
    def change_weight_kg(self):
        if self.statement_id.company_id.intrastat_additional_unit_from == "weight":
            self.additional_units = self.weight_kg

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super(IntrastatStatementSaleSection1, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )
        company_id = self.env.company

        # Company defaults
        delivery_code_id = (
            inv_intra_line.delivery_code_id
            or company_id.intrastat_sale_delivery_code_id
        )
        province_origin_id = (
            inv_intra_line.province_origin_id
            or company_id.intrastat_sale_province_origin_id
        )
        statistic_amount = (
            inv_intra_line.statistic_amount_euro
            or company_id.intrastat_sale_statistic_amount
        )
        transaction_nature_id = (
            inv_intra_line.transaction_nature_id
            or company_id.intrastat_sale_transaction_nature_id
        )
        transport_code_id = (
            inv_intra_line.transport_code_id
            or company_id.intrastat_sale_transport_code_id
        )

        # Amounts
        dp_model = self.env["decimal.precision"]
        statistic_amount = statement_id.round_min_amount(
            statistic_amount,
            statement_id.company_id or company_id,
            dp_model.precision_get("Account"),
        )

        # check if additional_units has a value
        has_additional_units = bool(inv_intra_line.additional_units)
        res.update(
            {
                "transaction_nature_id": transaction_nature_id.id,
                "weight_kg": round(inv_intra_line.weight_kg) or 1,
                "additional_units": round(inv_intra_line.additional_units)
                or (0 if not has_additional_units else 1),
                "statistic_amount_euro": statistic_amount,
                "delivery_code_id": delivery_code_id.id,
                "transport_code_id": transport_code_id.id,
                "country_destination_id": inv_intra_line.country_destination_id.id,
                "province_origin_id": province_origin_id.id,
            }
        )
        return res

    @api.model
    def _prepare_export_line(self):
        self.ensure_one()
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA dell’acquirente
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Codice della natura della transazione
        rcd += format_x(self.transaction_nature_id.code, 1)
        # Codice della nomenclatura combinata della merce
        rcd += format_9(self.intrastat_code_id.name, 8)
        if self.statement_id.period_type == "M":
            #  Massa netta in chilogrammi
            rcd += format_9(self.weight_kg, 10)
            #  Quantità espressa nell'unità di misura supplementare
            rcd += format_9(self.additional_units, 10)
            #  Valore statistico in euro
            rcd += format_9(self.statistic_amount_euro, 13)
            #  Codice delle condizioni di consegna
            delivery_code = self.delivery_code_id.code or ""
            rcd += format_x(delivery_code[:1], 1)
            #  Codice del modo di trasporto
            transport_code = self.transport_code_id.code
            rcd += format_9(transport_code, 1)
            #  Codice del paese di destinazione
            rcd += format_x(self.country_destination_id.code, 2)
            #  Codice del paese di origine della merce
            rcd += format_x(self.province_origin_id.code, 2)

        rcd += "\r\n"
        return rcd


class IntrastatStatementSaleSection2(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section2"
    _description = "Intrastat Statement - Sales Section 2"

    month = fields.Integer(string="Ref. Month")
    quarterly = fields.Integer(string="Ref. Quarter")
    year_id = fields.Integer(string="Ref. Year")
    sign_variation = fields.Selection(
        selection=[("+", "+"), ("-", "-")], string="Adjustment Sign"
    )
    transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Transaction Nature",
        default=lambda m: m._default_transaction_nature_id(),
    )
    statistic_amount_euro = fields.Integer(string="Statistic Value in Euro")

    @api.model
    def get_section_number(self):
        return 2

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super(IntrastatStatementSaleSection2, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )
        company_id = self._context.get("company_id", self.env.company)

        # Company defaults
        transaction_nature_id = (
            inv_intra_line.transaction_nature_id
            or company_id.intrastat_sale_transaction_nature_id
        )
        statistic_amount = (
            inv_intra_line.statistic_amount_euro
            or company_id.intrastat_sale_statistic_amount
        )

        # Amounts
        dp_model = self.env["decimal.precision"]
        statistic_amount = statement_id.round_min_amount(
            statistic_amount,
            statement_id.company_id or company_id,
            dp_model.precision_get("Account"),
        )

        # Period Ref
        ref_period = statement_id._get_period_ref()

        # Sign variation
        sign_variation = False
        if inv_intra_line.invoice_id.move_type == "out_refund":
            sign_variation = "-"
        res.update(
            {
                "month": ref_period.get("month"),
                "quarterly": ref_period.get("quarterly"),
                "year_id": ref_period.get("year_id"),
                "sign_variation": sign_variation,
                "transaction_nature_id": transaction_nature_id.id,
                "statistic_amount_euro": statistic_amount,
            }
        )
        return res

    def _export_line_checks(self, section_label, section_number):
        super(IntrastatStatementSaleSection2, self)._export_line_checks(
            section_label, section_number
        )
        if not self.year_id:
            raise ValidationError(_("Missing reference year on 'Sales - Section 2'"))
        if not self.sign_variation:
            raise ValidationError(_("Missing adjustment sign on 'Sales - Section 2'"))
        if self.statement_id.period_type == "M":
            if not self.month:
                raise ValidationError(
                    _("Missing reference month on 'Sales - Section 2' adjustment")
                )
        elif self.statement_id.period_type == "T":
            if not self.quarterly:
                raise ValidationError(
                    _("Missing reference quarter on 'Sales - Section 2' adjustment")
                )

    @api.model
    def _prepare_export_line(self):
        self.ensure_one()
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Mese di riferimento del riepilogo da rettificare
        rcd += format_9(self.month, 2)
        #  Trimestre di riferimento del riepilogo da rettificare
        rcd += format_9(self.quarterly, 1)
        # Anno periodo di ref da modificare
        year = (self.year_id or 0) % 100
        rcd += format_9(year, 2)
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA dell’acquirente
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        #  Segno da attribuire alle variazioni da X(1) apportare
        rcd += format_x(self.sign_variation, 1)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Codice della natura della transazione
        rcd += format_x(self.transaction_nature_id.code, 1)
        # Codice della nomenclatura combinata della merce
        rcd += format_9(self.intrastat_code_id.name, 8)
        if self.statement_id.period_type == "M":
            #  Valore statistico in euro
            rcd += format_9(self.statistic_amount_euro, 13)

        rcd += "\r\n"
        return rcd

    def get_amount_euro(self):
        amount = 0
        for section in self:
            if section.sign_variation == "-":
                amount -= section.amount_euro
            else:
                amount += section.amount_euro
        return amount


class IntrastatStatementSaleSection3(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section3"
    _description = "Intrastat Statement - Sales Section 3"

    invoice_number = fields.Char(string="Invoice Number")
    invoice_date = fields.Date(string="Invoice Date")
    supply_method = fields.Selection(
        selection=[("I", "Instant"), ("R", "Repeated")], string="Supply Method"
    )
    payment_method = fields.Selection(
        selection=[("B", "Bank Transfer"), ("A", "Credit"), ("X", "Other")],
        string="Payment Method",
    )
    country_payment_id = fields.Many2one(
        comodel_name="res.country", string="Payment Country"
    )

    @api.model
    def get_section_number(self):
        return 3

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super(IntrastatStatementSaleSection3, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )
        res.update(
            {
                "invoice_number": inv_intra_line.invoice_number,
                "invoice_date": inv_intra_line.invoice_date,
                "supply_method": inv_intra_line.supply_method,
                "payment_method": inv_intra_line.payment_method,
                "country_payment_id": inv_intra_line.country_payment_id.id,
            }
        )
        return res

    @api.model
    def _prepare_export_line(self):
        self.ensure_one()
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA del fornitore
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Numero Fattura
        rcd += format_x(self.invoice_number, 15)
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            invoice_date_ddmmyy = self.invoice_date.strftime("%d%m%y")
        rcd += format_x(invoice_date_ddmmyy, 6)
        # Codice del servizio
        rcd += format_9(self.intrastat_code_id.name, 6)
        # Modalità di erogazione
        rcd += format_x(self.supply_method, 1)
        # Modalità di incasso
        rcd += format_x(self.payment_method, 1)
        # Codice del paese di pagamento
        rcd += format_x(self.country_payment_id.code, 2)

        rcd += "\r\n"
        return rcd


class IntrastatStatementSaleSection4(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section4"
    _description = "Intrastat Statement - Sales Section 4"

    intrastat_custom_id = fields.Many2one(
        comodel_name="account.intrastat.custom", string="Customs Section"
    )
    month = fields.Integer(string="Ref. Month")
    quarterly = fields.Integer(string="Ref. Quarter")
    year_id = fields.Integer(string="Ref. Year")
    protocol = fields.Integer(string="Protocol Number", size=6)
    progressive_to_modify = fields.Integer(string="Progressive to Adjust")
    invoice_number = fields.Char(string="Invoice Number")
    invoice_date = fields.Date(string="Invoice Date")
    supply_method = fields.Selection(
        selection=[("I", "Instant"), ("R", "Repeated")], string="Supply Method"
    )
    payment_method = fields.Selection(
        selection=[("B", "Bank Transfer"), ("A", "Credit"), ("X", "Other")],
        string="Payment Method",
    )
    country_payment_id = fields.Many2one(
        comodel_name="res.country", string="Payment Country"
    )

    @api.model
    def get_section_number(self):
        return 4

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super(IntrastatStatementSaleSection4, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )

        # Period Ref
        ref_period = statement_id._get_period_ref()

        res.update(
            {
                "month": ref_period.get("month"),
                "quarterly": ref_period.get("quarterly"),
                "year_id": ref_period.get("year_id"),
                "invoice_number": inv_intra_line.invoice_number,
                "invoice_date": inv_intra_line.invoice_date,
                "supply_method": inv_intra_line.supply_method,
                "payment_method": inv_intra_line.payment_method,
                "country_payment_id": inv_intra_line.country_payment_id.id,
                "intrastat_custom_id": statement_id.intrastat_custom_id.id,
            }
        )
        return res

    def _export_line_checks(self, section_label, section_number):
        super(IntrastatStatementSaleSection4, self)._export_line_checks(
            section_label, section_number
        )
        if not self.year_id:
            raise ValidationError(_("Missing reference year on 'Sales - Section 4'"))
        if not self.intrastat_custom_id:
            raise ValidationError(_("Missing customs section on 'Sales - Section 4'"))
        if not self.protocol:
            raise ValidationError(_("Missing protocol number on 'Sales - Section 4'"))
        if not self.progressive_to_modify:
            raise ValidationError(
                _("Missing progressive to adjust on 'Sales - Section 4'")
            )
        if not self.country_payment_id:
            raise ValidationError(_("Missing payment country on 'Sales - Section 4'"))

    @api.model
    def _prepare_export_line(self):
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Codice della sezione doganale in cui è stato registrata la
        # dichiarazione da rettificare
        rcd += format_9(self.intrastat_custom_id.code, 6)
        # Anno di registrazione della dichiarazione da rettificare
        year = (self.year_id or 0) % 100
        rcd += format_9(year, 2)
        # Protocollo della dichiarazione da rettificare
        rcd += format_9(self.protocol, 6)
        # Progressivo della sezione 3 da rettificare
        rcd += format_9(self.progressive_to_modify, 5)
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA dell’acquirente
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Numero Fattura
        rcd += format_x(self.invoice_number, 15)
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            invoice_date_ddmmyy = self.invoice_date.strftime("%d%m%y")
        rcd += format_x(invoice_date_ddmmyy, 6)
        # Codice del servizio
        rcd += format_9(self.intrastat_code_id.name, 6)
        # Modalità di erogazione
        rcd += format_x(self.supply_method, 1)
        # Modalità di incasso
        rcd += format_x(self.payment_method, 1)
        # Codice del paese di pagamento
        rcd += format_x(self.country_payment_id.code, 2)

        rcd += "\r\n"
        return rcd
