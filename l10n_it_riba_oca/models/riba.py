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

    def _compute_payment_ids(self):
        """
        Compute payment-related move lines for RiBa slips.

        The computed field helps track payment status and provides visibility
        into which specific accounting entries are related to each RiBa slip.

        Migration Note (Odoo 18.0):
        This implementation uses a direct search on slip_line_id field, which is
        more efficient and reliable than the previous complex logic that tried
        to match payments through reconciliation records. The slip_line_id field
        is explicitly set during settlement creation, ensuring accurate tracking.
        """
        for riba in self:
            # Find all move lines that reference this RiBa's slip lines
            # These are created during settlement and represent actual payments
            payment_lines = self.env["account.move.line"].search(
                [("slip_line_id", "in", riba.line_ids.ids)]
            )
            riba.payment_ids = payment_lines

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
        help="Default date for payments.",
    )
    date_past_due = fields.Date("Past Due Date", readonly=True)
    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        default=lambda self: self.env.company,
    )
    acceptance_move_ids = fields.Many2many(
        "account.move",
        compute="_compute_acceptance_move_ids",
        string="Acceptance Entries",
    )
    credit_move_id = fields.Many2one("account.move", "Credit Entry", readonly=True)
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
    total_amount = fields.Float(
        string="Amount",
        compute="_compute_total_amount",
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

    def action_riba_due_date_settlement(self):
        return {
            "type": "ir.actions.act_window",
            "name": "C/O Due Date Settlement",
            "res_model": "riba.due.date.settlement",
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

    def riba_cancel(self):
        for slip in self:
            for line in slip.line_ids:
                line.state = "cancel"
                if line.acceptance_move_id:
                    line.acceptance_move_id.unlink()
                if line.past_due_move_id:
                    line.past_due_move_id.unlink()
            if slip.credit_move_id:
                slip.credit_move_id.unlink()
            slip.state = "cancel"

    def settle_all_line(self):
        payment_wizard_action = (
            self.env["riba.payment.multiple"]
            .with_context(
                active_ids=self.ids,
            )
            .get_formview_action()
        )
        payment_wizard_action.update(
            name=self.env._("Settle lines"),
            target="new",
        )
        return payment_wizard_action

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

    def test_paid(self):
        return self.test_state("paid")

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
    cig = fields.Char(string="CIG", size=256)
    cup = fields.Char(string="CUP", size=256)

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
            ("paid", "Paid"),
            ("past_due", "Past Due"),
            ("cancel", "Canceled"),
        ],
        readonly=True,
        tracking=True,
    )
    payment_id = fields.Many2one("account.move.line", string="Payments", readonly=True)
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
        for line in self:
            journal = line.slip_id.config_id.acceptance_journal_id
            total_credit = 0.0
            move = move_model.create(
                {
                    "ref": f"{line.invoice_number} RiBa {line.slip_id.name} \
                        - Line {line.sequence}",
                    "journal_id": journal.id,
                    "date": line.due_date,
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
            if not line.slip_id.date_accepted:
                line.slip_id.date_accepted = fields.Date.context_today(self)

    def button_settle(self):
        payment_wizard_action = (
            self.env["riba.payment.multiple"]
            .with_context(
                active_ids=self.slip_id.ids,
                default_riba_line_ids=self.ids,
            )
            .get_formview_action()
        )
        payment_wizard_action.update(
            name=self.env._("Settle line"),
            target="new",
        )
        return payment_wizard_action

    def riba_line_settlement(self, date=None):
        """
        Create settlement payment entries for RiBa lines.

        This method handles the final settlement of RiBa lines by creating
        accounting entries that record the actual payment received from customers
        through the bank. It reconciles the credit account with the bank account
        to complete the RiBa collection process.

        Settlement Process:
        1. Find the original credit move line that needs to be settled
        2. Calculate the settlement amount (considering partial payments for SBF)
        3. Create settlement move with:
           - Credit line: reduces the RiBa credit account
           - Debit line: increases the bank account
        4. Reconcile all related move lines to close the collection cycle

        :param date: The settlement date. If not provided, uses today's date.
        :type date: date or None
        :raises UserError: If settlement journal is not configured

        Business Flow:
        - Customer pays invoice → Bank receives payment → Bank notifies company
        - Company records settlement → RiBa line moves to 'paid' state
        """
        # Validate configuration before proceeding
        if not self.slip_id.config_id.settlement_journal_id:
            raise UserError(self.env._("Please define a Settlement Journal."))

        # Initialize models for creating accounting entries
        move_model = self.env["account.move"]
        move_line_model = self.env["account.move.line"]

        # Find the original credit move line that needs to be settled
        # This represents the amount that was credited when the RiBa was issued
        settlement_move_line = move_line_model.search(
            [
                ("account_id", "=", self.slip_id.config_id.credit_account_id.id),
                ("move_id", "=", self.credit_move_id.id),
                ("debit", "!=", 0),  # We need the debit side of the credit entry
            ]
        )

        # Reduce settlement amount by amounts already matched (partial payments)
        settlement_move_amount = settlement_move_line.debit - sum(
            settlement_move_line.mapped("matched_credit_ids.amount")
        )

        # Prepare settlement move data
        move_ref = f"Settlement RiBa {self.slip_id.name}"
        move_date = date or fields.Date.context_today(self)

        # Create the settlement accounting move
        settlement_move = move_model.create(
            {
                "journal_id": (self.slip_id.config_id.settlement_journal_id.id),
                "date": move_date,
                "ref": move_ref,
            }
        )

        # Create credit move lines for each RiBa line being settled
        move_lines_credit = self.env["account.move.line"]
        for riba_line in self:
            # Credit the RiBa account to reduce the outstanding amount
            move_line = move_line_model.with_context(check_move_validity=False).create(
                {
                    "name": move_ref,
                    "partner_id": riba_line.partner_id.id,
                    "account_id": riba_line.slip_id.config_id.credit_account_id.id,
                    "credit": riba_line.amount,  # Reduce RiBa credit account
                    "debit": 0.0,
                    "move_id": settlement_move.id,
                    "slip_line_id": riba_line.id,  # Link back to RiBa line
                }
            )
            move_lines_credit |= move_line

        # Create the corresponding bank debit entry
        bank_account = riba_line.slip_id.config_id.bank_account_id
        move_line_model.with_context(check_move_validity=False).create(
            {
                "name": move_ref,
                "account_id": bank_account.id,
                "credit": 0.0,
                "debit": settlement_move_amount,  # Increase bank account
                "move_id": settlement_move.id,
            }
        )

        # Post the settlement move
        move_lines_credit.mapped("move_id").action_post()

        # Prepare reconciliation: collect all move lines that need to be reconciled
        to_be_settled = self.env["account.move.line"]
        for move_line in move_lines_credit:
            to_be_settled |= move_line
        # Add the original credit move line
        to_be_settled |= settlement_move_line

        # Reconcile all related move lines to complete the settlement
        # This closes the accounting cycle for this RiBa collection
        to_be_settled.reconcile()

    def settle_riba_line(self):
        for line in self:
            if line.state == "credited":
                line.riba_line_settlement()


class RibaListMoveLine(models.Model):
    _name = "riba.slip.move.line"
    _description = "RiBa Details"
    _rec_name = "amount"

    amount = fields.Float(digits="Account")
    move_line_id = fields.Many2one("account.move.line", string="Credit Move Line")
    riba_line_id = fields.Many2one(
        "riba.slip.line", string="Slip Line", ondelete="cascade"
    )
