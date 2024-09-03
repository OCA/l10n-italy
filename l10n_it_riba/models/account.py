# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2018 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# Copyright 2024 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountPaymentTerm(models.Model):
    # flag riba utile a distinguere la modalità di pagamento
    _inherit = "account.payment.term"

    riba = fields.Boolean("RiBa", default=False)
    riba_payment_cost = fields.Float(
        "RiBa Collection Fees",
        digits="Account",
        help="Collection fees amount. If different from 0, "
        "for each payment deadline an invoice line will be added "
        "to invoice, with this amount.",
    )


class ResBankAddField(models.Model):
    _inherit = "res.bank"
    banca_estera = fields.Boolean("Foreign Bank")


class ResPartnerBankAdd(models.Model):
    _inherit = "res.partner.bank"
    codice_sia = fields.Char(
        "SIA Code",
        size=5,
        help="Identification Code of the Company in the Interbank System.",
    )


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "past_due_move_line_ids.past_due_invoice_ids",
        "past_due_move_line_ids.full_reconcile_id",
        "past_due_move_line_ids.matched_debit_ids",
        "past_due_move_line_ids.matched_credit_ids",
    )
    def _compute_is_past_due(self):
        for invoice in self:
            invoice.is_past_due = False
            reconciled_past_due = 0
            for past_due_move_line in invoice.past_due_move_line_ids:
                if past_due_move_line.reconciled:
                    reconciled_past_due += 1
            if len(invoice.past_due_move_line_ids) != reconciled_past_due:
                invoice.is_past_due = True

    def _compute_open_amount(self):
        today = fields.Date.today()
        for invoice in self:
            if invoice.is_riba_payment:
                open_amount_line_ids = invoice.line_ids.filtered(
                    lambda line, today=today: line.riba
                    and line.display_type == "payment_term"
                    and line.date_maturity > today
                )
                invoice.open_amount = sum(open_amount_line_ids.mapped("balance"))
            else:
                invoice.open_amount = 0.0

    riba_credited_ids = fields.One2many(
        "riba.slip", "credit_move_id", "Credited RiBa Slips", readonly=True
    )

    open_amount = fields.Float(
        digits="Account",
        compute="_compute_open_amount",
        default=0.0,
        help="Amount currently only supposed to be paid, but has actually not happened",
    )

    riba_past_due_ids = fields.One2many(
        "riba.slip.line", "past_due_move_id", "Past Due RiBa Slips", readonly=True
    )

    past_due_move_line_ids = fields.Many2many(
        "account.move.line",
        "invoice_past_due_line_rel",
        "move_id",
        "line_id",
        "Past Due Journal Items",
    )

    is_past_due = fields.Boolean(
        "Is a past due invoice", compute="_compute_is_past_due", store=True
    )
    is_riba_payment = fields.Boolean(
        "Is RiBa Payment", related="invoice_payment_term_id.riba"
    )

    riba_partner_bank_id = fields.Many2one(
        "res.partner.bank",
        string="RiBa Bank Account",
        help="Bank Account Number to which the RiBa will be debited. "
        "If not set, first bank in partner will be used.",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.model_create_multi
    def create(self, vals_list):
        invoices = super().create(vals_list)
        for invoice in invoices:
            if not invoice.riba_partner_bank_id:
                invoice._onchange_riba_partner_bank_id()
        return invoices

    @api.onchange("partner_id", "invoice_payment_term_id", "move_type")
    def _onchange_riba_partner_bank_id(self):
        allowed_banks = (
            self.partner_id.bank_ids or self.partner_id.commercial_partner_id.bank_ids
        )
        if (
            not self.riba_partner_bank_id
            or self.riba_partner_bank_id not in allowed_banks
        ):
            bank_ids = self.env["res.partner.bank"]
            if (
                self.partner_id
                and self.is_riba_payment
                and self.move_type in ["out_invoice", "out_refund"]
            ):
                bank_ids = allowed_banks
            self.riba_partner_bank_id = bank_ids[0] if bank_ids else None

    def month_check(self, invoice_date_due, all_date_due):
        """
        :param invoice_date_due: first due date of invoice
        :param all_date_due: list of due dates for partner
        :return: True if month of invoice_date_due is in a list of all_date_due
        """
        for d in all_date_due:
            if invoice_date_due.month == d.month and invoice_date_due.year == d.year:
                return True
        return False

    def action_post(self):
        for invoice in self:
            # ---- Add a line with collection fees for each due date only for first due
            # ---- date of the month
            if (
                invoice.move_type != "out_invoice"
                or not invoice.invoice_payment_term_id
                or not invoice.invoice_payment_term_id.riba
                or invoice.invoice_payment_term_id.riba_payment_cost == 0.0
            ):
                continue
            if not invoice.company_id.due_cost_service_id:
                raise UserError(
                    _("Set a Service for Collection Fees in Company Config.")
                )
            # ---- Apply Collection Fees on invoice only on first due date of the month
            # ---- Get Date of first due date
            move_line = self.env["account.move.line"].search(
                [("partner_id", "=", invoice.partner_id.id)]
            )
            if not any(line.due_cost_line for line in move_line):
                move_line = self.env["account.move.line"]
            # ---- Filtered recordset with date_maturity
            move_line = move_line.filtered(lambda line: line.date_maturity is not False)
            # ---- Sorted
            move_line = move_line.sorted(key=lambda r: r.date_maturity)
            # ---- Get date
            previous_date_due = move_line.mapped("date_maturity")
            pterm = self.env["account.payment.term"].browse(
                self.invoice_payment_term_id.id
            )
            pterm_list = pterm._compute_terms(
                date_ref=self.invoice_date,
                currency=self.currency_id,
                company=self.company_id,
                tax_amount=1,
                tax_amount_currency=1,
                untaxed_amount=0,
                untaxed_amount_currency=0,
                sign=1,
            )

            for pay_date in pterm_list:
                if not self.month_check(pay_date["date"], previous_date_due):
                    # ---- Get Line values for service product
                    service_prod = invoice.company_id.due_cost_service_id
                    account = service_prod.product_tmpl_id.get_product_accounts(
                        invoice.fiscal_position_id
                    )["income"]
                    line_vals = {
                        "partner_id": invoice.partner_id.id,
                        "product_id": service_prod.id,
                        "move_id": invoice.id,
                        "price_unit": (
                            invoice.invoice_payment_term_id.riba_payment_cost
                        ),
                        "due_cost_line": True,
                        "name": _("{line_name} for {month}-{year}").format(
                            line_name=service_prod.name,
                            month=pay_date["date"].month,
                            year=pay_date["date"].year,
                        ),
                        "account_id": account.id,
                        "sequence": 9999,
                    }
                    # ---- Update Line Value with tax if is set on product
                    if invoice.company_id.due_cost_service_id.taxes_id:
                        tax = invoice.fiscal_position_id.map_tax(service_prod.taxes_id)
                        line_vals.update({"tax_ids": [(4, tax.id)]})
                    invoice.write({"invoice_line_ids": [(0, 0, line_vals)]})
                    # ---- recompute invoice taxes
                    invoice._sync_dynamic_lines(
                        container={"records": invoice, "self": invoice}
                    )
        return super().action_post()

    def button_draft(self):
        # ---- Delete Collection Fees Line of invoice when set Back to Draft
        # ---- line was added on new validate
        res = super().button_draft()
        for invoice in self:
            due_cost_line_ids = invoice.get_due_cost_line_ids()
            if due_cost_line_ids:
                invoice.write(
                    {"invoice_line_ids": [(2, id, 0) for id in due_cost_line_ids]}
                )
                invoice._sync_dynamic_lines(
                    container={"records": invoice, "self": invoice}
                )
        return res

    def button_cancel(self):
        for invoice in self:
            # we get move_lines with date_maturity and check if they are
            # present in some riba_slip_line
            move_line_model = self.env["account.move.line"]
            rdml_model = self.env["riba.slip.move.line"]
            move_line_ids = move_line_model.search(
                [("move_id", "=", invoice.id), ("date_maturity", "!=", False)]
            )
            if move_line_ids:
                riba_line_ids = rdml_model.search(
                    [("move_line_id", "in", [m.id for m in move_line_ids])]
                )
                if riba_line_ids:
                    if len(riba_line_ids) > 1:
                        riba_line_ids = riba_line_ids[0]
                    raise UserError(
                        _(
                            "Invoice is linked to RiBa slip No. %(riba)s",
                            riba=riba_line_ids.riba_line_id.slip_id.name,
                        )
                    )
        return super().button_cancel()

    def copy(self, default=None):
        self.ensure_one()
        # Delete Collection Fees Line of invoice when copying
        invoice = super().copy(
            default=default,
        )
        if invoice:
            due_cost_line_ids = invoice.get_due_cost_line_ids()
            if due_cost_line_ids:
                invoice.write(
                    {"invoice_line_ids": [(2, id, 0) for id in due_cost_line_ids]}
                )
                invoice._sync_dynamic_lines(
                    container={"records": invoice, "self": invoice}
                )
        return invoice

    def get_due_cost_line_ids(self):
        return self.invoice_line_ids.filtered(lambda line: line.due_cost_line).ids

    def action_riba_payment_date(self):
        return {
            "type": "ir.actions.act_window",
            "name": "RiBa Payment Date",
            "res_model": "riba.payment.date",
            "view_mode": "form",
            "target": "new",
            "context": self.env.context,
        }


# se slip_line_ids == None allora non è stata emessa
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    slip_line_ids = fields.One2many(
        "riba.slip.move.line", "move_line_id", "RiBa Detail"
    )
    riba = fields.Boolean(
        related="move_id.invoice_payment_term_id.riba", string="RiBa", store=False
    )
    past_due_invoice_ids = fields.Many2many(
        "account.move",
        "invoice_past_due_line_rel",
        "line_id",
        "move_id",
        "Past Due Invoices",
    )
    iban = fields.Char(
        related="move_id.riba_partner_bank_id.acc_number", string="IBAN", store=False
    )
    due_cost_line = fields.Boolean("RiBa Collection Fees Line")

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        model_data_obj = self.env["ir.model.data"]
        ids = model_data_obj.search(
            [
                ("module", "=", "l10n_it_riba"),
                ("name", "=", "view_riba_to_issue_tree"),
            ]
        )
        if ids:
            view_payments_tree_id = model_data_obj.get_object_reference(
                "l10n_it_riba", "view_riba_to_issue_tree"
            )
        if ids and view_id == view_payments_tree_id[1]:
            # Use RiBa slip
            result = super(models.Model, self).fields_view_get(
                view_id=view_id,
                view_type=view_type,
                toolbar=toolbar,
                submenu=submenu,
            )
        else:
            # Use special views for account.move.line object
            # (for ex. tree view contains user defined fields)
            result = super().fields_view_get(
                view_id=view_id,
                view_type=view_type,
                toolbar=toolbar,
                submenu=submenu,
            )
        return result

    def get_riba_lines(self):
        riba_lines = self.env["riba.slip.line"]
        return riba_lines.search([("acceptance_move_id", "=", self.move_id.id)])

    def update_paid_riba_lines(self):
        # set paid only if not past_due
        if not self.env.context.get("past_due_reconciliation"):
            riba_lines = self.get_riba_lines()
            for riba_line in riba_lines:
                # allowed transitions:
                # credited_to_paid and accepted_to_paid. See workflow
                if riba_line.state in ["confirmed", "credited"]:
                    if riba_line.test_reconciled():
                        riba_line.state = "paid"
                        riba_line.slip_id.state = "paid"

    def reconcile(self):
        res = super().reconcile()
        for line in self:
            line.update_paid_riba_lines()
        return res

    def action_riba_issue(self):
        ctx = dict(self.env.context)
        ctx.pop("active_id", None)
        ctx["active_ids"] = self.ids
        ctx["active_model"] = "account.move.line"

        return {
            "type": "ir.actions.act_window",
            "name": "Issue RiBa",
            "res_model": "riba.issue",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }


class AccountFullReconcile(models.Model):
    _inherit = "account.full.reconcile"

    def get_riba_lines(self):
        riba_lines = self.env["riba.slip.line"]
        for move_line in self.reconciled_line_ids:
            riba_lines |= riba_lines.search(
                [("acceptance_move_id", "=", move_line.move_id.id)]
            )
        return riba_lines

    def unreconcile_riba_lines(self, riba_lines):
        for riba_line in riba_lines:
            # allowed transitions:
            # paid_to_cancel and past_due_to_cancel. See workflow
            if riba_line.state in ["paid", "past_due"]:
                if not riba_line.test_reconciled():
                    if riba_line.slip_id.credit_move_id:
                        riba_line.state = "credited"
                        riba_line.slip_id.state = "credited"
                    else:
                        riba_line.state = "confirmed"
                        riba_line.slip_id.state = "accepted"

    def unlink(self):
        riba_lines = None
        for rec in self:
            riba_lines = rec.get_riba_lines()
        res = super().unlink()
        if riba_lines:
            self.unreconcile_riba_lines(riba_lines)
        return res


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    def unlink(self):
        riba_lines = None
        for rec in self:
            riba_lines = rec.get_riba_lines()
        res = super().unlink()
        if riba_lines:
            self.env["account.full.reconcile"].unreconcile_riba_lines(riba_lines)
        return res

    def get_riba_lines(self):
        riba_lines = self.env["riba.slip.line"]
        riba_lines |= riba_lines.search(
            [("acceptance_move_id", "=", self.debit_move_id.move_id.id)]
        )
        riba_lines |= riba_lines.search(
            [("acceptance_move_id", "=", self.credit_move_id.move_id.id)]
        )
        return riba_lines
