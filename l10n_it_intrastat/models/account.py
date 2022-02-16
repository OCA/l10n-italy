# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    intrastat = fields.Boolean(string="Subject to Intrastat")


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _prepare_intrastat_line(self):
        self.ensure_one()
        res = {}
        company_id = self.move_id.company_id
        product_template = self.product_id.product_tmpl_id

        # Code competence
        intrastat_code, intrastat_data = self._prepare_intrastat_line_code(
            product_template, res
        )

        # Type
        res.update({"intrastat_code_type": intrastat_data["intrastat_type"]})

        # Amount
        self._prepare_intrastat_line_amount(res)

        # Weight
        weight_kg = self._prepare_intrastat_line_weight(product_template, res)

        # Additional Units
        self._prepare_intrastat_line_additional_units(
            company_id, intrastat_code, res, weight_kg
        )

        # Transport
        self._prepare_intrastat_line_transport(company_id, res)

        # Transaction
        self._prepare_intrastat_line_transaction(company_id, res)

        # Transaction B
        self._prepare_intrastat_line_transaction_b(company_id, res)

        # Delivery
        self._prepare_intrastat_line_delivery(company_id, res)

        # ---------
        # Origin
        # ---------
        # Provenance Country
        self._prepare_intrastat_line_country_origin(res)

        # Goods Origin Province
        self._prepare_intrastat_line_country_good_origin(res)

        # Origin Province
        self._prepare_intrastat_line_province_origin(company_id, res)

        # ---------
        # Destination
        # ---------
        # Destination Country
        self._prepare_intrastat_line_country_dest(res)

        # Destination Province
        self._prepare_intrastat_line_province_dest(company_id, res)

        # Payment method
        self._prepare_intrastat_line_payment(res)

        # Payment Country
        self._prepare_intrastat_line_country_payment(res)
        return res

    def _prepare_intrastat_line_country_payment(self, res):
        self.ensure_one()
        country_payment_id = self.env["res.country"].browse()
        if self.move_id.is_sale_document():
            country_payment_id = self.move_id.company_id.partner_id.country_id
            if self.move_id.partner_bank_id:
                country_id = self.move_id.partner_bank_id.bank_id.country
                if country_id:
                    country_payment_id = country_id
        elif self.move_id.is_purchase_document():
            country_payment_id = self.move_id.partner_id.country_id
        res.update({"country_payment_id": country_payment_id.id})

    def _prepare_intrastat_line_payment(self, res):
        self.ensure_one()
        payment_method = False
        if (
            self.move_id.invoice_payment_term_id
            and self.move_id.invoice_payment_term_id.intrastat_code
        ):
            payment_method = self.move_id.payment_term_id.intrastat_code
        res.update({"payment_method": payment_method})

    def _prepare_intrastat_line_province_dest(self, company_id, res):
        self.ensure_one()
        province_destination_id = self.env["res.country.state"].browse()
        if self.move_id.is_sale_document():
            province_destination_id = self.move_id.partner_id.state_id
        elif self.move_id.is_purchase_document():
            province_destination_id = (
                company_id.intrastat_purchase_province_destination_id
                or self.move_id.company_id.partner_id.state_id
            )
        res.update({"province_destination_id": province_destination_id.id})

    def _prepare_intrastat_line_country_dest(self, res):
        self.ensure_one()
        country_destination_id = self.env["res.country"].browse()
        if self.move_id.is_sale_document():
            country_destination_id = self.move_id.partner_id.country_id
        elif self.move_id.is_purchase_document():
            country_destination_id = self.move_id.company_id.partner_id.country_id
        res.update({"country_destination_id": country_destination_id.id})

    def _prepare_intrastat_line_province_origin(self, company_id, res):
        self.ensure_one()
        province_origin_id = self.env["res.country.state"].browse()
        if self.move_id.is_sale_document():
            province_origin_id = (
                company_id.intrastat_sale_province_origin_id
                or company_id.partner_id.state_id
            )
            country_origin_id = (
                company_id.intrastat_sale_country_origin_id
                or company_id.partner_id.country_id
            )
            res.update({"country_origin_id": country_origin_id.id})
        elif self.move_id.is_purchase_document():
            province_origin_id = self.move_id.partner_id.state_id
        res.update({"province_origin_id": province_origin_id.id})

    def _prepare_intrastat_line_country_good_origin(self, res):
        self.ensure_one()
        country_good_origin_id = self.env["res.country"].browse()
        if self.move_id.is_sale_document():
            country_good_origin_id = self.move_id.company_id.partner_id.country_id
        elif self.move_id.is_purchase_document():
            country_good_origin_id = self.move_id.partner_id.country_id
        res.update({"country_good_origin_id": country_good_origin_id.id})

    def _prepare_intrastat_line_country_origin(self, res):
        self.ensure_one()
        country_origin_id = self.env["res.country"].browse()
        if self.move_id.is_sale_document():
            country_origin_id = self.move_id.company_id.partner_id.country_id
        elif self.move_id.is_purchase_document():
            country_origin_id = self.move_id.partner_id.country_id
        res.update({"country_origin_id": country_origin_id.id})

    def _prepare_intrastat_line_delivery(self, company_id, res):
        self.ensure_one()
        if self.move_id.is_sale_document():
            res.update(
                {"delivery_code_id": company_id.intrastat_sale_delivery_code_id.id}
            )
        elif self.move_id.is_purchase_document():
            res.update(
                {"delivery_code_id": company_id.intrastat_purchase_delivery_code_id.id}
            )

    def _prepare_intrastat_line_transaction(self, company_id, res):
        self.ensure_one()
        if self.move_id.is_sale_document():
            sale_nature_id = company_id.intrastat_sale_transaction_nature_id.id
            res.update({"transaction_nature_id": sale_nature_id})
        elif self.move_id.is_purchase_document():
            purchase_nature_id = company_id.intrastat_purchase_transaction_nature_id.id
            res.update({"transaction_nature_id": purchase_nature_id})

    def _prepare_intrastat_line_transport(self, company_id, res):
        self.ensure_one()
        if self.move_id.is_sale_document():
            sale_code_id = company_id.intrastat_sale_transport_code_id.id
            res.update({"transport_code_id": sale_code_id})
        elif self.move_id.is_purchase_document():
            purchase_code_id = company_id.intrastat_purchase_transport_code_id.id
            res.update({"transport_code_id": purchase_code_id})

    def _prepare_intrastat_line_additional_units(
        self, company_id, intrastat_code, res, weight_kg
    ):
        self.ensure_one()
        additional_units = False
        # Priority : 1. Intrastat Code  2. Company
        if intrastat_code.additional_unit_from:
            if intrastat_code.additional_unit_from == "weight":
                additional_units = weight_kg
            elif intrastat_code.additional_unit_from == "quantity":
                additional_units = self.quantity
        elif company_id.intrastat_additional_unit_from:
            if company_id.intrastat_additional_unit_from == "weight":
                additional_units = weight_kg
            elif company_id.intrastat_additional_unit_from == "quantity":
                additional_units = self.quantity
        res.update({"additional_units": additional_units})

    def _prepare_intrastat_line_weight(self, product_template, res):
        self.ensure_one()
        intrastat_uom_kg = self.move_id.company_id.intrastat_uom_kg_id
        # ...Weight compute in Kg
        # ...If Uom has the same category of kg -> Convert to Kg
        # ...Else the weight will be product weight * qty
        product_weight = product_template.weight or 0
        if (
            intrastat_uom_kg
            and product_template.uom_id.category_id == intrastat_uom_kg.category_id
        ):
            weight_kg = self.product_uom_id._compute_quantity(
                qty=self.quantity, to_unit=intrastat_uom_kg
            )
        else:
            weight_kg = self.quantity * product_weight
        res.update({"weight_kg": weight_kg})
        return weight_kg

    def _prepare_intrastat_line_code(self, product_template, res):
        self.ensure_one()
        intrastat_data = product_template.get_intrastat_data()
        intrastat_code_model = self.env["report.intrastat.code"]
        intrastat_code = intrastat_code_model.browse()
        if intrastat_data["intrastat_code_id"]:
            intrastat_code = intrastat_code_model.browse(
                intrastat_data["intrastat_code_id"]
            )
        res.update({"intrastat_code_id": intrastat_data["intrastat_code_id"]})
        return intrastat_code, intrastat_data

    def _prepare_intrastat_line_amount(self, res):
        self.ensure_one()
        amount_currency = self.price_subtotal
        company_currency = self.move_id.company_id.currency_id
        invoice_currency = self.move_id.currency_id
        amount_euro = invoice_currency._convert(
            amount_currency,
            company_currency,
            self.move_id.company_id,
            fields.Date.today(),
        )
        statistic_amount_euro = amount_euro
        res.update(
            {
                "amount_currency": amount_currency,
                "amount_euro": amount_euro,
                "statistic_amount_euro": statistic_amount_euro,
            }
        )

    def _prepare_intrastat_line_transaction_b(self, company_id, res):
        self.ensure_one()
        if self.move_id.is_sale_document():
            s_transaction_nature_b = company_id.intrastat_sale_transaction_nature_b_id
            res.update({"transaction_nature_b_id": s_transaction_nature_b.id})
        elif self.move_id.is_purchase_document():
            p_transaction_nature_b = (
                company_id.intrastat_purchase_transaction_nature_b_id
            )
            res.update({"transaction_nature_b_id": p_transaction_nature_b.id})


class AccountMove(models.Model):
    _inherit = "account.move"

    intrastat = fields.Boolean(
        string="Subject to Intrastat",
        states={"draft": [("readonly", False)]},
        copy=False,
    )
    intrastat_line_ids = fields.One2many(
        comodel_name="account.invoice.intrastat",
        inverse_name="invoice_id",
        string="Intrastat",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
    )

    @api.onchange("fiscal_position_id")
    def change_fiscal_position(self):
        self.intrastat = self.fiscal_position_id.intrastat

    def action_post(self):
        for invoice in self:
            if not invoice.intrastat_line_ids and invoice.intrastat:
                invoice.compute_intrastat_lines()
        super().action_post()
        precision_digits = self.env["decimal.precision"].precision_get("Account")
        for invoice in self:
            if invoice.intrastat:
                # Calcolo l'importo delle righe di fattura che hanno i prodotti
                # che escludono il tipo intrastat

                excluded_amount = 0
                for line in invoice.invoice_line_ids:
                    product_tmp = line.product_id.product_tmpl_id
                    intrastat_data = product_tmp.get_intrastat_data()
                    if intrastat_data["intrastat_type"] == "exclude":
                        excluded_amount += line.price_subtotal

                total_amount = sum(
                    line.amount_currency for line in invoice.intrastat_line_ids
                )
                subtotal = abs(invoice.amount_untaxed - excluded_amount)
                if not float_is_zero(
                    total_amount - subtotal, precision_digits=precision_digits
                ):
                    raise UserError(
                        _("Intrastat total must be equal to invoice untaxed total")
                    )
        return True

    def compute_intrastat_lines(self):
        for inv in self:
            intrastat_lines = []
            # Unlink existing lines
            inv.intrastat_line_ids.unlink()

            i_line_by_code, lines_to_split = inv._get_intrastat_lines_to_split()

            # Split lines for intrastat with type "misc"
            if lines_to_split:
                inv._split_intrastat_lines(i_line_by_code, lines_to_split)

            for _key, val in i_line_by_code.items():
                intrastat_lines.append((0, 0, val))
            if intrastat_lines:
                inv.intrastat_line_ids = intrastat_lines

    @api.model
    def _split_intrastat_lines(self, i_line_by_code, lines_to_split):
        dp_obj = self.env["decimal.precision"]
        # tot intrastat
        amount_tot_intrastat = 0
        for _key, i_line in i_line_by_code.items():
            amount_tot_intrastat += i_line["amount_currency"]
        # amount to add
        for line in lines_to_split:
            amount_to_split = amount_to_split_residual = line.price_subtotal
            i = 0
            for _key, i_line in i_line_by_code.items():
                i += 1
                # competence
                if i == len(i_line_by_code):
                    amount_competence = amount_to_split_residual
                else:
                    amount_competence = amount_to_split * round(
                        (i_line["amount_currency"] / amount_tot_intrastat),
                        dp_obj.precision_get("Account"),
                    )
                # add to existing code
                i_line["amount_currency"] += amount_competence
                if i_line["statistic_amount_euro"]:
                    i_line["statistic_amount_euro"] += amount_competence

                amount_to_split_residual -= amount_competence

    def _get_intrastat_lines_to_split(self):
        self.ensure_one()
        i_line_by_code = {}
        lines_to_split = []
        for line in self.invoice_line_ids:
            # Lines to compute
            if not line.product_id:
                continue
            product_template = line.product_id.product_tmpl_id
            intrastat_data = product_template.get_intrastat_data()
            if (
                "intrastat_code_id" not in intrastat_data
                or intrastat_data["intrastat_type"] == "exclude"
            ):
                continue
            # Free lines
            if self.company_id.intrastat_exclude_free_line and not line.price_subtotal:
                continue
            # line to split
            if intrastat_data["intrastat_type"] == "misc":
                lines_to_split.append(line)
                continue
            if not intrastat_data["intrastat_code_id"]:
                continue

            # Group by intrastat code
            intra_line = line._prepare_intrastat_line()
            i_code_id = intra_line["intrastat_code_id"]
            i_code_type = intra_line["intrastat_code_type"]

            if i_code_id in i_line_by_code:
                i_line_by_code[i_code_id]["amount_currency"] += intra_line[
                    "amount_currency"
                ]
                i_line_by_code[i_code_id]["statistic_amount_euro"] += intra_line[
                    "statistic_amount_euro"
                ]
                i_line_by_code[i_code_id]["weight_kg"] += intra_line["weight_kg"]
                i_line_by_code[i_code_id]["additional_units"] += intra_line[
                    "additional_units"
                ]
            else:
                intra_line["statement_section"] = self.env[
                    "account.invoice.intrastat"
                ].compute_statement_section(i_code_type, self.move_type)
                i_line_by_code[i_code_id] = intra_line
        return i_line_by_code, lines_to_split


class AccountInvoiceIntrastat(models.Model):
    _name = "account.invoice.intrastat"
    _description = "Intrastat Line"

    def name_get(self):
        res = []
        for line in self:
            res.append((line.id, "%s" % line.invoice_id.name))
        return res

    @api.depends("amount_currency")
    def _compute_amount_euro(self):
        for line in self:
            company_currency = line.invoice_id.company_id.currency_id
            invoice_currency = line.invoice_id.currency_id
            if invoice_currency:
                line.amount_euro = invoice_currency._convert(
                    line.amount_currency,
                    company_currency,
                    line.invoice_id.company_id,
                    fields.Date.today(),
                )

    @api.depends("invoice_id.partner_id")
    def _compute_partner_data(self):
        for line in self:
            line.country_partner_id = line.invoice_id.partner_id.country_id

    @api.depends(
        "invoice_id.payment_reference", "invoice_id.name", "invoice_id.invoice_date"
    )
    def _compute_invoice_ref(self):
        for line in self:
            if line.invoice_id.is_purchase_document():
                if not line.invoice_id.payment_reference:
                    continue
                line.invoice_number = (
                    line.invoice_id.payment_reference or line.invoice_id.name
                )
                if line.invoice_id.invoice_date:
                    line.invoice_date = line.invoice_id.invoice_date
            elif line.invoice_id.is_sale_document():
                if not line.invoice_id.name:
                    continue
                line.invoice_number = line.invoice_id.name
                if line.invoice_id.invoice_date:
                    line.invoice_date = line.invoice_id.invoice_date

    @api.depends("invoice_id.move_type", "intrastat_code_type")
    def _compute_statement_section(self):
        """
        Compute where the invoice intrastat data will be computed.
        This field is used to show the right values to fill in
        """
        invoice_type_ctx = self.env.context.get("invoice_type")
        intrastat_code_type_ctx = self.env.context.get("intrastat_code_type")
        for line in self:
            invoice_type = invoice_type_ctx or line.invoice_id.move_type
            intrastat_code_type = intrastat_code_type_ctx or line.intrastat_code_type
            line.statement_section = self.compute_statement_section(
                intrastat_code_type, invoice_type
            )

    @api.model
    def compute_statement_section(self, intrastat_code_type, invoice_type):
        section_spec = {
            ("in_invoice", "good"): "purchase_s1",
            ("in_refund", "good"): "purchase_s2",
            ("in_invoice", "service"): "purchase_s3",
            ("in_refund", "service"): "purchase_s4",
            ("out_invoice", "good"): "sale_s1",
            ("out_refund", "good"): "sale_s2",
            ("out_invoice", "service"): "sale_s3",
            ("out_refund", "service"): "sale_s4",
        }
        return section_spec.get((invoice_type, intrastat_code_type))

    @api.model
    def _get_partner_data(self, partner):
        """
        Data default from partner
        """
        res = {
            "country_partner_id": partner.country_id.id,
            "vat_code": partner.vat and partner.vat[2:] or False,
            "country_origin_id": partner.country_id.id,
            "country_good_origin_id": partner.country_id.id,
            "country_destination_id": partner.country_id.id,
        }
        return res

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Invoice",
        ondelete="cascade",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner", readonly=True, related="invoice_id.partner_id", store=True
    )

    intrastat_type_data = fields.Selection(
        selection=[
            ("all", "All (Fiscal and Statistic)"),
            ("fiscal", "Fiscal"),
            ("statistic", "Statistic"),
        ],
        string="Data Type",
        default="all",
        required=True,
    )
    intrastat_code_type = fields.Selection(
        selection=[("service", "Service"), ("good", "Goods")],
        string="Code Type",
        required=True,
        default="good",
    )
    intrastat_code_id = fields.Many2one(
        comodel_name="report.intrastat.code", string="Nomenclature Code", required=True
    )
    statement_section = fields.Selection(
        selection=[
            ("sale_s1", "Sales section 1"),
            ("sale_s2", "Sales section 2"),
            ("sale_s3", "Sales section 3"),
            ("sale_s4", "Sales section 4"),
            ("purchase_s1", "Purchases section 1"),
            ("purchase_s2", "Purchases section 2"),
            ("purchase_s3", "Purchases section 3"),
            ("purchase_s4", "Purchases section 4"),
        ],
        string="Statement Section",
        compute="_compute_statement_section",
    )

    amount_euro = fields.Float(
        string="Amount in Euro",
        compute="_compute_amount_euro",
        digits="Account",
        store=True,
        readonly=True,
    )
    amount_currency = fields.Float(string="Amount in Currency", digits="Account")
    transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature", string="Transaction Nature"
    )
    transaction_nature_b_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature.b",
        string="Transaction Nature B",
    )
    weight_kg = fields.Float(string="Net Mass (kg)")
    additional_units = fields.Float(string="Additional Units")
    additional_units_uom = fields.Char(
        string="Additional Unit of Measure",
        readonly=True,
        related="intrastat_code_id.additional_unit_uom_id.name",
    )
    statistic_amount_euro = fields.Float(
        string="Statistic Value in Euro", digits="Account"
    )
    country_partner_id = fields.Many2one(
        comodel_name="res.country",
        string="Partner State",
        compute="_compute_partner_data",
        store=True,
        readonly=True,
    )
    # Origin
    province_origin_id = fields.Many2one(
        comodel_name="res.country.state", string="Origin Province"
    )
    country_origin_id = fields.Many2one(
        comodel_name="res.country", string="Provenance Country"
    )
    country_good_origin_id = fields.Many2one(
        comodel_name="res.country", string="Goods Origin Country"
    )
    delivery_code_id = fields.Many2one(
        comodel_name="account.incoterms", string="Delivery Terms"
    )
    transport_code_id = fields.Many2one(
        comodel_name="account.intrastat.transport", string="Transport Mode"
    )
    # Destination
    province_destination_id = fields.Many2one(
        comodel_name="res.country.state", string="Destination Province"
    )
    country_destination_id = fields.Many2one(
        comodel_name="res.country", string="Destination Country"
    )
    invoice_number = fields.Char(
        string="Invoice Number", compute="_compute_invoice_ref", store=True
    )
    invoice_date = fields.Date(
        string="Invoice Date", compute="_compute_invoice_ref", store=True
    )
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
    triangulation = fields.Boolean(string="Triangulation", default=False)
    invoice_type = fields.Selection(
        string="Invoice Type",
        related="invoice_id.move_type",
        store=False,
        readonly=True,
    )

    @api.onchange("transaction_nature_id")
    def _onchange_transaction_nature_id(self):
        domain = [("nature_parent_id", "=", self.transaction_nature_id.id)]
        recs = self.env["account.intrastat.transaction.nature.b"].search(domain)
        return {"domain": {"transaction_nature_b_id": [("id", "in", recs.ids)]}}

    @api.onchange("weight_kg")
    def change_weight_kg(self):
        if self.invoice_id.company_id.intrastat_additional_unit_from == "weight":
            self.additional_units = self.weight_kg

    @api.onchange("amount_euro")
    def change_amount_euro(self):
        self.statistic_amount_euro = self.amount_euro

    @api.onchange("intrastat_code_type")
    def change_intrastat_code_type(self):
        self.statement_section = self._compute_statement_section()
        self.intrastat_code_id = False


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    intrastat_code = fields.Selection(
        selection=[("B", "Bank Transfer"), ("A", "Credit"), ("X", "Other")],
        string="Payment Method",
    )
