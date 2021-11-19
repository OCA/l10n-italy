# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class RibaList(models.Model):
    def _compute_acceptance_move_ids(self):
        for riba in self:
            move_ids = self.env["account.move"]
            for line in riba.line_ids:
                move_ids |= line.acceptance_move_id
            riba.acceptance_move_ids = move_ids

    def _compute_unsolved_move_ids(self):
        for riba in self:
            move_ids = self.env["account.move"]
            for line in riba.line_ids:
                move_ids |= line.unsolved_move_id
            riba.unsolved_move_ids = move_ids

    def _compute_payment_ids(self):
        for riba in self:
            move_lines = self.env["account.move.line"]
            for line in riba.line_ids:
                move_lines |= line.payment_ids
            riba.payment_ids = move_lines

    _name = "riba.distinta"
    _description = "C/O Slip"
    _inherit = ["mail.thread"]
    _order = "date_created desc"

    name = fields.Char(
        "Reference",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=(lambda self: self.env["ir.sequence"].next_by_code("riba.distinta")),
    )
    config_id = fields.Many2one(
        "riba.configuration",
        string="Configuration",
        index=True,
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="C/O configuration to be used.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("accepted", "Accepted"),
            ("accredited", "Credited"),
            ("paid", "Paid"),
            ("unsolved", "Past Due"),
            ("cancel", "Canceled"),
        ],
        "State",
        readonly=True,
        default="draft",
    )
    line_ids = fields.One2many(
        "riba.distinta.line",
        "distinta_id",
        "C/O Due Dates",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    user_id = fields.Many2one(
        "res.users",
        "User",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.user,
    )
    date_created = fields.Date(
        "Creation Date",
        readonly=True,
        default=lambda self: fields.Date.context_today(self),
    )
    date_accepted = fields.Date("Acceptance Date")
    date_accreditation = fields.Date("Credit Date")
    date_paid = fields.Date("Payment Date", readonly=True)
    date_unsolved = fields.Date("Past Due Date", readonly=True)
    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.company,
    )
    acceptance_move_ids = fields.Many2many(
        "account.move",
        compute="_compute_acceptance_move_ids",
        string="Acceptance Entries",
    )
    accreditation_move_id = fields.Many2one(
        "account.move", "Credit Entry", readonly=True
    )
    payment_ids = fields.Many2many(
        "account.move.line", compute="_compute_payment_ids", string="Payments"
    )
    unsolved_move_ids = fields.Many2many(
        "account.move", compute="_compute_unsolved_move_ids", string="Past Due Entries"
    )
    type = fields.Selection(string="Type", related="config_id.type", readonly=True)
    registration_date = fields.Date(
        "Registration Date",
        states={
            "draft": [("readonly", False)],
            "cancel": [("readonly", False)],
        },
        readonly=True,
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Keep empty to use the current date.",
    )

    def action_riba_export(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Issue C/O",
            "res_model": "riba.file.export",
            "view_mode": "form",
            "target": "new",
            "context": self.env.context,
        }

    def unlink(self):
        for riba_list in self:
            if riba_list.state not in ("draft", "cancel"):
                raise UserError(
                    _(
                        "Slip %s is in state '%s'. You can only delete documents"
                        " in state 'Draft' or 'Canceled'."
                    )
                    % (riba_list.name, riba_list.state)
                )
        super(RibaList, self).unlink()

    def confirm(self):
        for distinta in self:
            for line in distinta.line_ids:
                line.confirm()

    def riba_cancel(self):
        for distinta in self:
            for line in distinta.line_ids:
                line.state = "cancel"
                if line.acceptance_move_id:
                    line.acceptance_move_id.unlink()
                if line.unsolved_move_id:
                    line.unsolved_move_id.unlink()
            if distinta.accreditation_move_id:
                distinta.accreditation_move_id.unlink()
            distinta.state = "cancel"

    def settle_all_line(self):
        for riba_list in self:
            for line in riba_list.line_ids:
                if line.state == "accredited":
                    line.riba_line_settlement()

    @api.onchange("date_accepted", "date_accreditation")
    def _onchange_date(self):
        if self.date_accepted and self.date_accreditation:
            if self.date_accepted > self.date_accreditation:
                raise UserError(
                    _("Credit date must be greater or equal to" " acceptance date.")
                )

    def riba_unsolved(self):
        self.state = "unsolved"
        self.date_unsolved = fields.Date.context_today(self)

    def test_state(self, state):
        for riba_list in self:
            for line in riba_list.line_ids:
                if line.state != state:
                    return False
        return True

    def test_accepted(self):
        return self.test_state("confirmed")

    def test_unsolved(self):
        return self.test_state("unsolved")

    def test_paid(self):
        return self.test_state("paid")

    def action_cancel_draft(self):
        for riba_list in self:
            riba_list.state = "draft"
            for line in riba_list.line_ids:
                line.state = "draft"


class RibaListLine(models.Model):
    _name = "riba.distinta.line"
    _inherit = "mail.thread"
    _description = "C/O Details"
    _rec_name = "sequence"

    def _compute_line_values(self):
        for line in self:
            line.amount = 0.0
            line.invoice_date = ""
            line.invoice_number = ""
            for move_line in line.move_line_ids:
                line.amount += move_line.amount
                if not line.invoice_date:
                    line.invoice_date = str(
                        fields.Date.from_string(
                            move_line.move_line_id.move_id.invoice_date
                        ).strftime("%d/%m/%Y")
                    )
                else:
                    line.invoice_date = "{}, {}".format(
                        line.invoice_date,
                        str(
                            fields.Date.from_string(
                                move_line.move_line_id.move_id.invoice_date
                            ).strftime("%d/%m/%Y")
                        ),
                    )
                if not line.invoice_number:
                    line.invoice_number = str(
                        move_line.move_line_id.move_id.move_id.name
                        if move_line.move_line_id.move_id.display_name == "/"
                        else move_line.move_line_id.move_id.display_name
                    )
                else:
                    line.invoice_number = "{}, {}".format(
                        line.invoice_number,
                        str(
                            move_line.move_line_id.move_id.move_id.name
                            if move_line.move_line_id.move_id.display_name == "/"
                            else move_line.move_line_id.move_id.display_name
                        ),
                    )

    amount = fields.Float(compute="_compute_line_values", string="Amount")
    invoice_date = fields.Char(
        compute="_compute_line_values", string="Invoice Date", size=256
    )
    invoice_number = fields.Char(
        compute="_compute_line_values", string="Invoice Number", size=256
    )
    cig = fields.Char(compute="_compute_cig_cup_values", string="CIG", size=256)
    cup = fields.Char(compute="_compute_cig_cup_values", string="CUP", size=256)

    def _compute_cig_cup_values(self):
        for line in self:
            line.cig = ""
            line.cup = ""
            for move_line in line.move_line_ids:
                for (
                    related_document
                ) in move_line.move_line_id.move_id.related_documents:
                    if related_document.cup:
                        line.cup = str(related_document.cup)
                    if related_document.cig:
                        line.cig = str(related_document.cig)

    def move_line_id_payment_get(self):
        # return the move line ids with the same account as the distinta line
        if not self.id:
            return []
        query = """ SELECT l.id
                    FROM account_move_line l, riba_distinta_line rdl
                    WHERE rdl.id = %s AND l.move_id = rdl.acceptance_move_id
                    AND l.account_id = rdl.acceptance_account_id
                """
        self._cr.execute(query, (self.id,))
        return [row[0] for row in self._cr.fetchall()]

    def test_reconciled(self):
        # check whether all corresponding account move lines are reconciled
        line_ids = self.move_line_id_payment_get()
        if not line_ids:
            return False
        move_lines = self.env["account.move.line"].browse(line_ids)
        reconcilied = all(line.reconciled for line in move_lines)
        return reconcilied

    def _compute_lines(self):
        for riba_line in self:
            payment_lines = []
            if riba_line.acceptance_move_id and not riba_line.state == "unsolved":
                for line in riba_line.acceptance_move_id.line_ids:
                    payment_lines.extend(
                        [
                            _f
                            for _f in [
                                rp.credit_move_id.id for rp in line.matched_credit_ids
                            ]
                            if _f
                        ]
                    )
            riba_line.payment_ids = self.env["account.move.line"].browse(
                list(set(payment_lines))
            )

    sequence = fields.Integer("Number")
    move_line_ids = fields.One2many(
        "riba.distinta.move.line", "riba_line_id", string="Credit Move Lines"
    )
    acceptance_move_id = fields.Many2one(
        "account.move", string="Acceptance Entry", readonly=True
    )
    unsolved_move_id = fields.Many2one(
        "account.move", string="Past Due Entry", readonly=True
    )
    acceptance_account_id = fields.Many2one(
        "account.account", string="Acceptance Account"
    )
    bank_id = fields.Many2one("res.partner.bank", string="Debtor Bank")
    iban = fields.Char(
        related="bank_id.acc_number", string="IBAN", store=False, readonly=True
    )
    distinta_id = fields.Many2one(
        "riba.distinta", string="Slip", required=True, ondelete="cascade"
    )
    partner_id = fields.Many2one("res.partner", string="Customer", readonly=True)
    due_date = fields.Date("Due Date", readonly=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("accredited", "Credited"),
            ("paid", "Paid"),
            ("unsolved", "Past Due"),
            ("cancel", "Canceled"),
        ],
        "State",
        readonly=True,
        tracking=True,
    )
    payment_ids = fields.Many2many(
        "account.move.line", compute="_compute_lines", string="Payments"
    )
    type = fields.Selection(
        string="Type", related="distinta_id.config_id.type", readonly=True
    )
    config_id = fields.Many2one(
        string="Configuration", related="distinta_id.config_id", readonly=True
    )

    def confirm(self):
        move_model = self.env["account.move"]
        move_line_model = self.env["account.move.line"]
        for line in self:
            journal = line.distinta_id.config_id.acceptance_journal_id
            total_credit = 0.0
            move = move_model.create(
                {
                    "ref": "C/O {} - Line {}".format(
                        line.distinta_id.name, line.sequence
                    ),
                    "journal_id": journal.id,
                    "date": line.distinta_id.registration_date,
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
                    {"check_move_validity": False}
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
            move_line_model.with_context({"check_move_validity": False}).create(
                {
                    "name": "C/O %s-%s Ref. %s - %s"
                    % (
                        line.distinta_id.name,
                        line.sequence,
                        riba_move_line_name,
                        line.partner_id.name,
                    ),
                    "account_id": (
                        line.acceptance_account_id.id
                        or line.distinta_id.config_id.acceptance_account_id.id
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
            line.distinta_id.state = "accepted"
            if not line.distinta_id.date_accepted:
                line.distinta_id.date_accepted = fields.Date.context_today(self)

    def riba_line_settlement(self):
        for riba_line in self:
            if not riba_line.distinta_id.config_id.settlement_journal_id:
                raise UserError(_("Please define a Settlement Journal."))

            # trovare le move line delle scritture da chiudere
            move_model = self.env["account.move"]
            move_line_model = self.env["account.move.line"]

            settlement_move_line = move_line_model.search(
                [
                    ("account_id", "=", riba_line.acceptance_account_id.id),
                    ("move_id", "=", riba_line.acceptance_move_id.id),
                    ("debit", "!=", 0),
                ]
            )

            settlement_move_amount = settlement_move_line.debit

            move_ref = "Settlement C/O {} - {}".format(
                riba_line.distinta_id.name,
                riba_line.partner_id.name,
            )
            settlement_move = move_model.create(
                {
                    "journal_id": (
                        riba_line.distinta_id.config_id.settlement_journal_id.id
                    ),
                    "date": date.today().strftime("%Y-%m-%d"),
                    "ref": move_ref,
                }
            )

            move_line_credit = move_line_model.with_context(
                {"check_move_validity": False}
            ).create(
                {
                    "name": move_ref,
                    "partner_id": riba_line.partner_id.id,
                    "account_id": riba_line.acceptance_account_id.id,
                    "credit": settlement_move_amount,
                    "debit": 0.0,
                    "move_id": settlement_move.id,
                }
            )

            accr_acc = riba_line.distinta_id.config_id.accreditation_account_id
            move_line_model.with_context({"check_move_validity": False}).create(
                {
                    "name": move_ref,
                    "account_id": accr_acc.id,
                    "credit": 0.0,
                    "debit": settlement_move_amount,
                    "move_id": settlement_move.id,
                }
            )

            move_line_credit.move_id.action_post()
            to_be_settled = self.env["account.move.line"]
            to_be_settled |= move_line_credit
            to_be_settled |= settlement_move_line

            to_be_settled.reconcile()


class RibaListMoveLine(models.Model):
    _name = "riba.distinta.move.line"
    _description = "C/O Details"
    _rec_name = "amount"

    amount = fields.Float("Amount", digits="Account")
    move_line_id = fields.Many2one("account.move.line", string="Credit Move Line")
    riba_line_id = fields.Many2one(
        "riba.distinta.line", string="Slip Line", ondelete="cascade"
    )
