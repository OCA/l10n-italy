# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# Copyright 2024 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.exceptions import UserError


class RibaList(models.Model):
    def _compute_acceptance_move_ids(self):
        for riba in self:
            move_ids = self.env["account.move"]
            for line in riba.line_ids:
                move_ids |= line.acceptance_move_id
            riba.acceptance_move_ids = move_ids

    def _compute_past_due_move_ids(self):
        for riba in self:
            move_ids = self.env["account.move"]
            for line in riba.line_ids:
                move_ids |= line.past_due_move_id
            riba.past_due_move_ids = move_ids

    @api.depends(
        "config_id.type",
        "config_id.acceptance_account_id",
        "config_id.credit_account_id",
        "credit_move_id.line_ids.account_id",
        "line_ids.acceptance_account_id",
        "line_ids.acceptance_move_id.line_ids.account_id",
    )
    def _compute_collect_line_ids(self):
        """
        Compute the accounting lines that the bank still has to pay.

        They represent the credit the company has towards the bank, and are
        closed by the bank entry of the actual collection:

        - 'Subject to collection': the RiBa account line of the credit entry,
          because it is the credit entry that makes the amount available;
        - 'After collection': the bills account lines of the acceptance
          entries, because in this mode there is no credit entry at all.
        """
        line_model = self.env["account.move.line"]
        for riba in self:
            config = riba.config_id
            if config.type == "sbf":
                account = config.credit_account_id
                collect_lines = riba.credit_move_id.line_ids.filtered(
                    lambda line, account=account: line.account_id == account
                    and line.debit > 0
                )
            else:
                collect_lines = line_model
                for slip_line in riba.line_ids:
                    account = (
                        slip_line.acceptance_account_id or config.acceptance_account_id
                    )
                    collect_lines |= slip_line.acceptance_move_id.line_ids.filtered(
                        lambda line, account=account: line.account_id == account
                        and line.debit > 0
                    )
            riba.collect_line_ids = collect_lines

    @api.depends(
        "config_id.type",
        "config_id.acceptance_account_id",
        "config_id.credit_account_id",
        "line_ids.acceptance_account_id",
        "credit_move_id.line_ids.account_id",
        "credit_move_id.line_ids.debit",
        "credit_move_id.line_ids.amount_residual",
        "line_ids.acceptance_move_id.line_ids.account_id",
        "line_ids.acceptance_move_id.line_ids.debit",
        "line_ids.acceptance_move_id.line_ids.amount_residual",
    )
    def _compute_amount_residual(self):
        for riba in self:
            collect_lines = riba.collect_line_ids
            riba.amount_residual = sum(collect_lines.mapped("amount_residual"))
            riba.amount_paid = sum(collect_lines.mapped("debit")) - riba.amount_residual

    @api.depends(
        "amount_paid",
        "amount_residual",
    )
    def _compute_payment_state(self):
        for riba in self:
            currency = riba.currency_id
            if not riba.collect_line_ids or currency.is_zero(riba.amount_paid):
                payment_state = "not_paid"
            elif currency.is_zero(riba.amount_residual):
                payment_state = "paid"
            else:
                payment_state = "partial"
            riba.payment_state = payment_state

    def _update_state_from_payment(self):
        """
        Align the state of the slip to what the bank has actually paid.

        The slip is paid when the whole credit towards the bank has been
        collected, and goes back to the previous state if the collection
        is undone. This is called when the reconciliation changes, so that
        the state does not depend on the recomputation of `payment_state`.
        """
        for riba in self:
            if riba.state in ("draft", "cancel", "past_due"):
                # These states do not depend on the collection
                continue
            if riba.payment_state == "paid":
                state = "paid"
            elif riba.credit_move_id:
                state = "credited"
            else:
                state = "accepted"
            if riba.state != state:
                riba.state = state

    @api.depends(
        "payment_state",
        "credit_move_id.line_ids.matched_credit_ids.max_date",
        "line_ids.acceptance_move_id.line_ids.matched_credit_ids.max_date",
    )
    def _compute_date_paid(self):
        for riba in self:
            dates = riba.collect_line_ids.matched_credit_ids.mapped("max_date")
            if dates and riba.payment_state == "paid":
                riba.date_paid = max(dates)
            else:
                riba.date_paid = False

    @api.depends(
        "credit_move_id.line_ids.matched_credit_ids.credit_move_id",
        "line_ids.acceptance_move_id.line_ids.matched_credit_ids.credit_move_id",
    )
    def _compute_payment_ids(self):
        """
        Compute the move lines that collected this RiBa slip.

        They are the counterparts reconciled with the lines to collect:
        the bank entries of the actual collection, or the past due entries
        of the RiBa that have not been paid.
        """
        for riba in self:
            riba.payment_ids = riba.collect_line_ids.matched_credit_ids.credit_move_id

    def _compute_total_amount(self):
        for riba in self:
            riba.total_amount = 0.0
            for line in riba.line_ids:
                riba.total_amount += line.amount

    _name = "riba.slip"
    _description = "RiBa Slip"
    _inherit = ["mail.thread"]
    _order = "date_created desc"

    name = fields.Char(
        "Reference",
        required=True,
        default=(lambda self: self.env["ir.sequence"].next_by_code("riba.slip")),
    )
    config_id = fields.Many2one(
        "riba.configuration",
        string="Configuration",
        index=True,
        help="RiBa configuration to be used.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("accepted", "Accepted"),
            ("credited", "Credited"),
            ("paid", "Paid"),
            ("past_due", "Past Due"),
            ("cancel", "Canceled"),
        ],
        readonly=True,
        default="draft",
    )
    line_ids = fields.One2many(
        "riba.slip.line",
        "slip_id",
        "RiBa Due Dates",
    )
    user_id = fields.Many2one(
        "res.users",
        "User",
        required=True,
        default=lambda self: self.env.user,
    )
    date_created = fields.Date(
        "Creation Date",
        readonly=True,
        default=lambda self: fields.Date.context_today(self),
    )
    date_accepted = fields.Date("Acceptance Date")
    date_credited = fields.Date("Credit Date")
    date_paid = fields.Date(
        string="Payment Date",
        compute="_compute_date_paid",
        store=True,
        readonly=True,
        help="Date of the bank entry that collected the slip.",
    )
    date_past_due = fields.Date("Past Due Date", readonly=True)
    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
    )
    acceptance_move_ids = fields.Many2many(
        "account.move",
        compute="_compute_acceptance_move_ids",
        string="Acceptance Entries",
    )
    credit_move_id = fields.Many2one("account.move", "Credit Entry", readonly=True)
    collect_line_ids = fields.Many2many(
        "account.move.line",
        compute="_compute_collect_line_ids",
        string="Lines to Collect",
        help="Accounting lines of the credit towards the bank: "
        "reconciling them with the actual bank entry marks the slip as paid.",
    )
    payment_ids = fields.Many2many(
        "account.move.line", compute="_compute_payment_ids", string="Payments"
    )
    past_due_move_ids = fields.Many2many(
        "account.move", compute="_compute_past_due_move_ids", string="Past Due Entries"
    )
    type = fields.Selection(string="Type", related="config_id.type", readonly=True)
    registration_date = fields.Date(
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Keep empty to use the current date.",
    )
    total_amount = fields.Monetary(
        string="Amount",
        compute="_compute_total_amount",
    )
    amount_paid = fields.Monetary(
        string="Paid Amount",
        compute="_compute_amount_residual",
        help="Amount of the slip already collected by the bank.",
    )
    amount_residual = fields.Monetary(
        string="Amount Due",
        compute="_compute_amount_residual",
        help="Amount of the slip that the bank has still to collect.",
    )
    payment_state = fields.Selection(
        [
            ("not_paid", "Not Paid"),
            ("partial", "Partially Paid"),
            ("paid", "Paid"),
        ],
        string="Payment Status",
        compute="_compute_payment_state",
        store=True,
        readonly=True,
    )

    def action_riba_export(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Issue RiBa",
            "res_model": "riba.file.export",
            "view_mode": "form",
            "target": "new",
            "context": self.env.context,
        }

    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_confirmed(self):
        for riba_list in self:
            if riba_list.state not in ("draft", "cancel"):
                raise UserError(
                    self.env._(
                        "Slip %(name)s is in state '%(state)s'."
                        " You can only delete documents"
                        " in state 'Draft' or 'Canceled'.",
                        name=riba_list.name,
                        state=riba_list.state,
                    )
                )

    def confirm(self):
        for slip in self:
            for line in slip.line_ids:
                line.confirm()

    def _unlink_move(self, move):
        """Delete `move`, setting it back to draft first if it is posted.

        Posted entries cannot be deleted while they are reconciled:
        `button_draft` takes care of removing the reconciliation.
        """
        if move.state == "posted":
            move.button_draft()
        move.unlink()

    def riba_cancel(self):
        for slip in self:
            for line in slip.line_ids:
                line.state = "cancel"
                if line.acceptance_move_id:
                    slip._unlink_move(line.acceptance_move_id)
                if line.past_due_move_id:
                    slip._unlink_move(line.past_due_move_id)
            if slip.credit_move_id:
                slip._unlink_move(slip.credit_move_id)
            slip.state = "cancel"

    @api.onchange("date_accepted", "date_credited")
    def _onchange_date(self):
        if self.date_accepted and self.date_credited:
            if self.date_accepted > self.date_credited:
                raise UserError(
                    self.env._(
                        "Credit date must be greater or equal to acceptance date."
                    )
                )

    def riba_past_due(self):
        self.state = "past_due"
        self.date_past_due = fields.Date.context_today(self)

    def test_state(self, state):
        for riba_list in self:
            for line in riba_list.line_ids:
                if line.state != state:
                    return False
        return True

    def test_accepted(self):
        return self.test_state("confirmed")

    def test_past_due(self):
        return self.test_state("past_due")

    def action_cancel_draft(self):
        for riba_list in self:
            riba_list.state = "draft"
            for line in riba_list.line_ids:
                line.state = "draft"

    def action_open_lines(self):
        action = self.env.ref("l10n_it_riba_oca.detail_riba_action").read()[0]
        action["domain"] = [("slip_id", "=", self.id)]
        return action


class RibaListLine(models.Model):
    _name = "riba.slip.line"
    _inherit = "mail.thread"
    _description = "RiBa Details"
    _rec_name = "sequence"

    def _compute_line_values(self):
        for line in self:
            line.amount = 0.0
            line.invoice_date = ""
            line.invoice_number = ""
            for move_line in line.move_line_ids:
                line.amount += move_line.amount
                move_date = move_line.move_line_id.move_id.invoice_date
                if move_date:
                    move_date = str(
                        fields.Date.from_string(move_date).strftime("%d/%m/%Y")
                    )
                if not line.invoice_date:
                    line.invoice_date = move_date
                else:
                    line.invoice_date = f"{line.invoice_date}, {move_date}"
                if not line.invoice_number:
                    line.invoice_number = str(
                        move_line.move_line_id.move_id.name
                        if move_line.move_line_id.move_id.display_name == "/"
                        else move_line.move_line_id.move_id.display_name
                    )
                else:
                    line.invoice_number = "{}, {}".format(
                        line.invoice_number,
                        str(
                            move_line.move_line_id.move_id.name
                            if move_line.move_line_id.move_id.display_name == "/"
                            else move_line.move_line_id.move_id.display_name
                        ),
                    )

    amount = fields.Float(compute="_compute_line_values")
    invoice_date = fields.Char(compute="_compute_line_values", size=256)
    invoice_number = fields.Char(compute="_compute_line_values", size=256)
    cig = fields.Char(compute="_compute_cig_cup_values", string="CIG", size=256)
    cup = fields.Char(compute="_compute_cig_cup_values", string="CUP", size=256)

    def _compute_cig_cup_values(self):
        for line in self:
            line.cig = ""
            line.cup = ""
            related_documents = line.mapped(
                "move_line_ids.move_line_id.move_id.related_document_ids"
            )

            for related_document in related_documents:
                if related_document.cup:
                    line.cup = str(related_document.cup)
                if related_document.cig:
                    line.cig = str(related_document.cig)
                # Stop if at least one value is found
                if line.cup or line.cig:
                    break

    sequence = fields.Integer("Number")
    move_line_ids = fields.One2many(
        "riba.slip.move.line", "riba_line_id", string="Credit Move Lines"
    )
    acceptance_move_id = fields.Many2one(
        "account.move", string="Acceptance Entry", readonly=True
    )
    credit_move_id = fields.Many2one(
        "account.move", string="Credit Entry", readonly=True
    )
    past_due_move_id = fields.Many2one(
        "account.move", string="Past Due Entry", readonly=True
    )
    acceptance_account_id = fields.Many2one(
        "account.account", string="Acceptance Account"
    )
    bank_id = fields.Many2one("res.partner.bank", string="Debtor Bank")
    iban = fields.Char(
        related="bank_id.acc_number", string="IBAN", store=False, readonly=True
    )
    slip_id = fields.Many2one(
        "riba.slip", string="Slip", required=True, ondelete="cascade"
    )
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    due_date = fields.Date(readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("credited", "Credited"),
            ("past_due", "Past Due"),
            ("cancel", "Canceled"),
        ],
        readonly=True,
        tracking=True,
    )
    type = fields.Selection(
        string="Type", related="slip_id.config_id.type", readonly=True
    )
    config_id = fields.Many2one(
        string="Configuration", related="slip_id.config_id", readonly=True
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        related="slip_id.company_id",
        store=True,
        readonly=True,
        related_sudo=False,
    )

    def confirm(self):
        move_model = self.env["account.move"]
        move_line_model = self.env["account.move.line"]
        today = fields.Date.context_today(self)
        for line in self:
            journal = line.slip_id.config_id.acceptance_journal_id
            total_credit = 0.0
            date_accepted = line.slip_id.date_accepted
            if not date_accepted:
                line.slip_id.date_accepted = date_accepted = line.due_date or today
            move = move_model.create(
                {
                    "ref": f"{line.invoice_number} RiBa {line.slip_id.name} \
                        - Line {line.sequence}",
                    "journal_id": journal.id,
                    "date": date_accepted,
                }
            )
            to_be_reconciled = self.env["account.move.line"]
            riba_move_line_name = ""
            for riba_move_line in line.move_line_ids:
                total_credit += riba_move_line.amount
                if (
                    str(riba_move_line.move_line_id.move_id.sequence_number)
                    and str(riba_move_line.move_line_id.move_id.sequence_number)
                    not in riba_move_line_name
                ):
                    riba_move_line_name = " ".join(
                        [
                            riba_move_line_name,
                            str(riba_move_line.move_line_id.move_id.sequence_number),
                        ]
                    ).lstrip()
                elif (
                    riba_move_line.move_line_id.name
                    and riba_move_line.move_line_id.name not in riba_move_line_name
                ):
                    riba_move_line_name = " ".join(
                        [riba_move_line_name, riba_move_line.move_line_id.name]
                    ).lstrip()
                move_line = move_line_model.with_context(
                    check_move_validity=False
                ).create(
                    {
                        "name": (
                            riba_move_line.move_line_id.move_id
                            and riba_move_line.move_line_id.move_id.sequence_number
                            or riba_move_line.move_line_id.name
                        ),
                        "partner_id": line.partner_id.id,
                        "account_id": riba_move_line.move_line_id.account_id.id,
                        "credit": riba_move_line.amount,
                        "debit": 0.0,
                        "move_id": move.id,
                    }
                )
                to_be_reconciled |= move_line
                to_be_reconciled |= riba_move_line.move_line_id
            move_line_model.with_context(check_move_validity=False).create(
                {
                    "name": f"{line.invoice_number} RiBa {line.slip_id.name}-\
                        {line.sequence} Ref. {riba_move_line_name} - \
                            {line.partner_id.name}",
                    "account_id": (
                        line.acceptance_account_id.id
                        or line.slip_id.config_id.acceptance_account_id.id
                        # in questo modo se la riga non ha conto accettazione
                        # viene prelevato il conto in configuration riba
                    ),
                    "partner_id": line.partner_id.id,
                    "date_maturity": line.due_date,
                    "credit": 0.0,
                    "debit": total_credit,
                    "move_id": move.id,
                }
            )
            move.action_post()
            to_be_reconciled.reconcile()
            line.write(
                {
                    "acceptance_move_id": move.id,
                    "state": "confirmed",
                }
            )
            line.slip_id.state = "accepted"


class RibaListMoveLine(models.Model):
    _name = "riba.slip.move.line"
    _description = "RiBa Details"
    _rec_name = "amount"

    amount = fields.Float(digits="Account")
    move_line_id = fields.Many2one("account.move.line", string="Credit Move Line")
    riba_line_id = fields.Many2one(
        "riba.slip.line", string="Slip Line", ondelete="cascade"
    )
