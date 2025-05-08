# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class DeclarationOfIntentYearlyLimit(models.Model):
    _name = "l10n_it_declaration_of_intent.yearly_limit"
    _description = "Yearly limit for declarations"
    _order = "company_id, year desc"
    _rec_name = "year"

    company_id = fields.Many2one("res.company", string="Company")
    year = fields.Char(required=True)
    limit_amount = fields.Float()
    used_amount = fields.Float(compute="_compute_used_amount")

    def _compute_used_amount(self):
        for record in self:
            date_start = datetime.strptime(f"01-01-{record.year}", "%d-%m-%Y")
            date_end = datetime.strptime(f"31-12-{record.year}", "%d-%m-%Y")
            declarations = self.env["l10n_it_declaration_of_intent.declaration"].search(
                [
                    ("date_start", ">=", date_start),
                    ("date_end", "<=", date_end),
                    ("type", "=", "in"),
                ]
            )
            record.used_amount = sum([d.limit_amount for d in declarations])


class DeclarationOfIntent(models.Model):
    _name = "l10n_it_declaration_of_intent.declaration"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Declaration of intent"
    _order = "date_start desc,date_end desc"

    @api.model
    def _default_currency(self):
        return self.env.company.currency_id

    number = fields.Char(copy=False)
    date = fields.Date(required=True, string="Telematic Protocol Date")
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        required=True,
        default="in",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    telematic_protocol = fields.Char(required=True)
    partner_document_number = fields.Char(
        string="Document Number", help="Number of partner's document"
    )
    partner_document_date = fields.Date(
        string="Document Date", help="Date of partner's document"
    )
    taxes_ids = fields.Many2many("account.tax", string="Taxes", required=True)
    used_amount = fields.Monetary(compute="_compute_amounts", store=True)
    limit_amount = fields.Monetary(required=True)
    available_amount = fields.Monetary(compute="_compute_amounts", store=True)
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=_default_currency,
    )
    fiscal_position_id = fields.Many2one(
        "account.fiscal.position",
        string="Fiscal Position",
        required=True,
        domain=[("valid_for_declaration_of_intent", "=", True)],
    )
    state = fields.Selection(
        [("valid", "Valid"), ("expired", "Expired"), ("close", "Close")],
        compute="_compute_state",
        store=True,
    )
    force_close = fields.Boolean()
    line_ids = fields.One2many(
        comodel_name="l10n_it_declaration_of_intent.declaration_line",
        inverse_name="declaration_id",
        string="Lines",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            # ----- Check if yearly plafond is enough
            #       to create an in declaration
            # Declaration issued by company are "IN"
            if values.get("type", False) == "in":
                year = fields.Date.to_date(values["date_start"]).strftime("%Y")
                plafond = self.env.company.declaration_yearly_limit_ids.filtered(
                    lambda r, y=year: r.year == y
                )
                if not plafond:
                    raise UserError(
                        _(
                            "Define a yearly plafond for in documents in your company "
                            "settings"
                        )
                    )
                date_start = datetime.strptime(f"01-01-{year}", "%d-%m-%Y")
                date_end = datetime.strptime(f"31-12-{year}", "%d-%m-%Y")
                declarations = self.search(
                    [
                        ("date_start", ">=", date_start),
                        ("date_end", "<=", date_end),
                        ("type", "=", "in"),
                    ]
                )
                actual_limit_total = (
                    sum([d.limit_amount for d in declarations]) + values["limit_amount"]
                )
                if actual_limit_total > plafond.limit_amount:
                    raise UserError(_("Total of documents exceed yearly limit"))
            # ----- Assign a number to declaration
            if values and not values.get("number", ""):
                values["number"] = self.env["ir.sequence"].next_by_code(
                    "declaration_of_intent"
                )
        return super().create(vals_list)

    def unlink(self):
        for record in self:
            if record.line_ids:
                raise UserError(
                    _("Impossible to delete a document with linked invoices")
                )
        return super().unlink()

    @api.constrains("fiscal_position_id", "taxes_ids")
    def _check_taxes_for_declaration_of_intent(self):
        for declaration in self:
            if (
                declaration.taxes_ids
                and declaration.fiscal_position_id
                and declaration.fiscal_position_id.tax_ids
            ):
                taxes = [
                    t.tax_dest_id.id for t in declaration.fiscal_position_id.tax_ids
                ]
                for tax in declaration.taxes_ids:
                    if tax.id not in taxes:
                        raise ValidationError(
                            _(
                                "All taxes in declaration of intent must be used "
                                "in fiscal position taxes"
                            )
                        )

    @api.constrains("limit_amount", "used_amount", "line_ids")
    def _check_available_amount(self):
        for declaration in self:
            if declaration.available_amount < 0:
                raise UserError(
                    _(
                        "Limit passed for declaration {number}."
                        "\nExcess value: {symbol}{available_amount}"
                    ).format(
                        number=declaration.number,
                        symbol=declaration.currency_id.symbol,
                        available_amount=abs(declaration.available_amount),
                    )
                )

    def name_get(self):
        res = []
        for record in self:
            complete_name = record.number
            if record.partner_document_number:
                complete_name = f"{complete_name} ({record.partner_document_number})"
            res.append(
                (record.id, complete_name),
            )
        return res

    @api.depends(
        "line_ids",
        "line_ids.amount",
        "limit_amount",
        "line_ids.invoice_id",
        "line_ids.invoice_id.state",
    )
    def _compute_amounts(self):
        for record in self:
            amount = sum(
                line.amount
                for line in record.line_ids.filtered(
                    lambda li: li.invoice_id and li.invoice_id.state == "posted"
                )
            )
            # ----- Force value to 0
            if amount < 0.0:
                amount = 0.0
            record.used_amount = amount
            record.available_amount = record.limit_amount - record.used_amount

    @api.depends("used_amount", "limit_amount", "date_end", "force_close")
    def _compute_state(self):
        for record in self:
            # ----- If state is forced to be close, close document
            if record.force_close:
                state = "close"
            # ----- If used amount is bigger than limit, close document
            elif record.limit_amount and record.used_amount >= record.limit_amount:
                state = "close"
            # ----- If date is passed, close document
            elif record.date_end and record.date_end < datetime.today().date():
                state = "expired"
            else:
                state = "valid"
            record.state = state

    @api.onchange("fiscal_position_id", "type")
    def onchange_fiscal_position_id(self):
        taxes = self.env["account.tax"]
        for tax_mapping in self.fiscal_position_id.tax_ids:
            if tax_mapping.tax_dest_id:
                if (
                    self.type == "in"
                    and tax_mapping.tax_dest_id.type_tax_use == "purchase"
                ) or (
                    self.type == "out"
                    and tax_mapping.tax_dest_id.type_tax_use == "sale"
                ):
                    taxes |= tax_mapping.tax_dest_id
        if taxes:
            self.taxes_ids = [(6, 0, taxes.ids)]

    def change_force_close(self):
        for record in self:
            record.force_close = not record.force_close

    def get_valid(self, type_d=None, partner_id=False, date=False):
        if not partner_id or not type_d or not date:
            return False
        ignore_state = self.env.context.get("ignore_state", False)
        all_for_partner = self.get_all_for_partner(type_d, partner_id, ignore_state)
        # # ----- return valid documents for partner
        records = all_for_partner.filtered(lambda d: d.date_start <= date <= d.date_end)
        return records

    def get_all_for_partner(self, type_d=None, partner_id=False, ignore_state=False):
        if not partner_id or not type_d:
            return False
        # ----- return all documents for partner
        domain = [("partner_id", "=", partner_id), ("type", "=", type_d)]
        if not ignore_state:
            domain.append(
                ("state", "!=", "close"),
            )
        records = self.search(domain, order="state desc, date")
        return records


class DeclarationOfIntentLine(models.Model):
    _name = "l10n_it_declaration_of_intent.declaration_line"
    _description = "Details of declaration of intent"

    declaration_id = fields.Many2one(
        comodel_name="l10n_it_declaration_of_intent.declaration",
        string="Declaration",
    )
    taxes_ids = fields.Many2many("account.tax", string="Taxes")
    move_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="move_line_declaration_line_rel",
        string="Move Lines",
        ondelete="cascade",
    )
    amount = fields.Monetary()
    base_amount = fields.Monetary()
    invoice_id = fields.Many2one("account.move", string="Invoice", ondelete="cascade")
    date_invoice = fields.Date(related="invoice_id.invoice_date", string="Date Invoice")
    company_id = fields.Many2one(
        "res.company", string="Company", related="declaration_id.company_id"
    )
    currency_id = fields.Many2one("res.currency", string="Currency")
