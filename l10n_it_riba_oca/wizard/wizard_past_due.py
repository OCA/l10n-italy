# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class RibaPastDue(models.TransientModel):
    @api.model
    def _get_config_type(self):
        return self.env["riba.configuration"].get_default_value_by_list_line("type")

    @api.model
    def _get_past_due_journal_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "past_due_journal_id"
        )

    @api.model
    def _get_unsolved_past_due_fee_amount(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "past_due_fee_amount"
        )

    @api.model
    def _get_acceptance_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "acceptance_account_id"
        )

    @api.model
    def _get_credit_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "credit_account_id"
        )

    @api.model
    def _get_credit_amount(self):
        if not self.env.context.get("active_id", False):
            return False
        return self.env["riba.slip.line"].browse(self.env.context["active_id"]).amount

    @api.model
    def _get_overdue_credit_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "overdue_credit_account_id"
        )

    @api.model
    def _get_bank_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "bank_account_id"
        )

    @api.model
    def _get_bank_expense_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list_line(
            "protest_charge_account_id"
        )

    _name = "riba.past_due"
    _description = "Manage Past Due RiBas"
    config_type = fields.Selection(
        [("sbf", "Subject To Collection"), ("incasso", "After Collection")],
        "Issue Mode",
        default=_get_config_type,
    )
    past_due_journal_id = fields.Many2one(
        "account.journal",
        "Past Due Journal",
        domain=[("type", "=", "bank")],
        default=_get_past_due_journal_id,
    )
    acceptance_account_id = fields.Many2one(
        "account.account",
        "Acceptance Account",
        default=_get_acceptance_account_id,
    )
    credit_account_id = fields.Many2one(
        "account.account",
        "Credit Account",
        default=_get_credit_account_id,
    )
    credit_amount = fields.Float(default=_get_credit_amount)
    overdue_credit_account_id = fields.Many2one(
        "account.account",
        "Past Due Bills Account",
        default=_get_overdue_credit_account_id,
    )
    overdue_credit_amount = fields.Float(
        "Past Due Bills Amount", default=_get_credit_amount
    )

    bank_account_id = fields.Many2one(
        "account.account", "A/C Bank Account", default=_get_bank_account_id
    )
    bank_expense_account_id = fields.Many2one(
        "account.account", "Bank Fees Account", default=_get_bank_expense_account_id
    )
    expense_amount = fields.Float("Fees Amount")
    date = fields.Date(
        help="If empty, the due date in the line will be used.",
        readonly=False,
    )
    past_due_fee_amount = fields.Float(
        "Past Due Fees Amount", default=_get_unsolved_past_due_fee_amount
    )

    def skip(self):
        active_id = self.env.context.get("active_id")
        if not active_id:
            raise UserError(self.env._("No active ID found."))
        line_model = self.env["riba.slip.line"]
        line = line_model.browse(active_id)
        line.acceptance_move_id.button_draft()
        line.acceptance_move_id.unlink()
        line.state = "past_due"
        line.slip_id.state = "past_due"
        return {"type": "ir.actions.act_window_close"}

    def _validate_accounts(self, riba_type):
        """Validate that all required accounts are set based on RiBa type."""
        account_check = (
            not self.past_due_journal_id
            or not self.overdue_credit_account_id
            or not self.bank_expense_account_id
        )
        # only incasso type needs "Acceptance Account"
        if riba_type == "incasso":
            account_check = account_check or not self.acceptance_account_id
        # only sbf type needs "RiBa Account"
        else:
            account_check = account_check or not self.credit_account_id
        if account_check:
            raise UserError(self.env._("Every account is mandatory."))

    def _prepare_move_lines(self, slip_line, riba_type, date):
        """Prepare move lines for the past due entry."""
        line_ids = []

        # Determine account and name based on RiBa type
        if riba_type == "incasso":
            aml_name = self.env._("Bills Account")
            aml_account_id = self.acceptance_account_id.id
        else:
            aml_name = self.env._("RiBa Credit")
            aml_account_id = self.credit_account_id.id

        # Add bank fees line if applicable
        if self.past_due_fee_amount:
            line_ids.extend(
                [
                    (
                        0,
                        0,
                        {
                            "name": self.env._("Bank Fee"),
                            "account_id": self.bank_expense_account_id.id,
                            "debit": self.past_due_fee_amount,
                            "credit": 0.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.env._("Bank Fee"),
                            "account_id": self.bank_account_id.id,
                            "debit": 0.0,
                            "credit": self.past_due_fee_amount,
                        },
                    ),
                ]
            )

        # Add main lines
        line_ids.extend(
            [
                # Past due bills line
                (
                    0,
                    0,
                    {
                        "name": self.env._("Past Due Bills"),
                        "account_id": self.overdue_credit_account_id.id,
                        "debit": self.overdue_credit_amount,
                        "credit": 0.0,
                        "partner_id": slip_line.partner_id.id,
                        "date_maturity": date,
                    },
                ),
                # Credit/acceptance line
                (
                    0,
                    0,
                    {
                        "name": aml_name,
                        "account_id": aml_account_id,
                        "credit": self.overdue_credit_amount,
                        "debit": 0.0,
                    },
                ),
            ]
        )

        return line_ids

    def _process_reconciliation(self, move, slip_line):
        """Process reconciliation for the past due move."""
        move_line_model = self.env["account.move.line"]
        move_model = self.env["account.move"]

        riba_credit_to_be_reconciled, customers_to_be_reconciled = [], []

        # Process move lines for reconciliation
        for move_line in move.line_ids:
            if move_line.account_id.id == self.overdue_credit_account_id.id:
                self._process_overdue_move_line(move_line, slip_line, move_model)
                customers_to_be_reconciled.append(move_line.id)
            if move_line.account_id.id == self.credit_account_id.id:
                riba_credit_to_be_reconciled.append(move_line.id)

        # Add credit move lines for reconciliation
        for credit_move_line in slip_line.credit_move_id.line_ids:
            if credit_move_line.account_id.id == self.credit_account_id.id:
                riba_credit_to_be_reconciled.append(credit_move_line.id)

        # Reconcile RiBa credit lines
        if riba_credit_to_be_reconciled:
            move_line_model.browse(riba_credit_to_be_reconciled).reconcile()

        # Remove existing reconciliations
        slip_line.move_line_ids.move_line_id.remove_move_reconcile()

        # Add acceptance move lines for reconciliation
        for acceptance_move_line in slip_line.acceptance_move_id.line_ids:
            if acceptance_move_line.account_id.id == self.overdue_credit_account_id.id:
                customers_to_be_reconciled.append(acceptance_move_line.id)

        # Reconcile customer lines
        customers_to_be_reconciled_lines = move_line_model.with_context(
            past_due_reconciliation=True
        ).browse(customers_to_be_reconciled)
        customers_to_be_reconciled_lines.reconcile()

    def _process_overdue_move_line(self, move_line, slip_line, move_model):
        """Process overdue move line for invoice linking."""
        for riba_move_line in slip_line.move_line_ids:
            invoice_ids = []
            if riba_move_line.move_line_id.move_id:
                invoice_ids = [riba_move_line.move_line_id.move_id.id]
            elif riba_move_line.move_line_id.past_due_invoice_ids:
                invoice_ids = [
                    i.id for i in riba_move_line.move_line_id.past_due_invoice_ids
                ]
            move_model.browse(invoice_ids).write(
                {
                    "past_due_move_line_ids": [(4, move_line.id)],
                }
            )

    def create_move(self):
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(self.env._("No active ID found."))

        move_model = self.env["account.move"]
        slip_line = self.env["riba.slip.line"].browse(active_id)
        riba_type = slip_line.slip_id.config_id.type

        # Validate required accounts
        self._validate_accounts(riba_type)

        date = self.date or slip_line.due_date

        # Prepare move lines
        line_ids = self._prepare_move_lines(slip_line, riba_type, date)

        # Create and post the move
        move_vals = {
            "ref": self.env._("Past Due RiBa %(name)s - Line %(sequence)s")
            % {
                "name": slip_line.slip_id.name,
                "sequence": slip_line.sequence,
            },
            "journal_id": self.past_due_journal_id.id,
            "date": date,
            "line_ids": line_ids,
        }

        move = move_model.create(move_vals)
        move.action_post()

        # Process reconciliation
        self._process_reconciliation(move, slip_line)

        # Update slip line state
        slip_line.write(
            {
                "past_due_move_id": move.id,
                "state": "past_due",
            }
        )
        slip_line.slip_id.state = "past_due"

        return {
            "name": self.env._("Past Due Entry"),
            "view_mode": "form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": move.id or False,
        }
