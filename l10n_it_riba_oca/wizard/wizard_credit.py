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


class RibaCredit(models.TransientModel):
    """
    Wizard for creating bank credit entries for RiBa slips.

    This wizard handles the "credit" phase of the RiBa collection process, where
    the bank provides immediate liquidity to the company by crediting their account
    with the RiBa amount. This typically happens after the bank accepts the RiBa
    collection but before the actual customer payment is received.

    RiBa Credit Process:
    1. Bank accepts RiBa collection from company
    2. Bank may immediately credit company's account (this wizard)
    3. Bank collects payment from customers
    4. If customer pays: settlement completes the cycle
    5. If customer doesn't pay: past due process reverses the credit

    Accounting Impact:
    - Increases RiBa Credit Account (asset)
    - Decreases Acceptance Account (liability)
    - Optional: Records bank fees and payment
    """

    @api.model
    def _get_credit_journal_id(self):
        """Get default credit journal from RiBa configuration."""
        return self.env["riba.configuration"].get_default_value_by_list(
            "credit_journal_id"
        )

    @api.model
    def _get_credit_account_id(self):
        """Get default RiBa credit account from configuration."""
        return self.env["riba.configuration"].get_default_value_by_list(
            "credit_account_id"
        )

    @api.model
    def _get_acceptance_account_id(self):
        """Get default acceptance account from RiBa configuration."""
        return self.env["riba.configuration"].get_default_value_by_list(
            "acceptance_account_id"
        )

    @api.model
    def _get_bank_account_id(self):
        """Get default bank account for fee payments from configuration."""
        return self.env["riba.configuration"].get_default_value_by_list(
            "bank_account_id"
        )

    @api.model
    def _get_bank_expense_account_id(self):
        """Get default bank expense account for collection fees."""
        return self.env["riba.configuration"].get_default_value_by_list(
            "bank_expense_account_id"
        )

    @api.model
    def _get_acceptance_amount(self):
        """
        Calculate total acceptance amount from RiBa slip lines.

        This represents the total amount that was originally recorded
        in the acceptance phase and needs to be reversed during credit.

        :return: Total amount of all lines in the active RiBa slip
        :rtype: float
        """
        if not self.env.context.get("active_id", False):
            return False
        slip_model = self.env["riba.slip"]
        slip = slip_model.browse(self.env.context["active_id"])
        amount = 0.0
        # Sum all line amounts to get total RiBa value
        for line in slip.line_ids:
            amount += line.amount
        return amount

    _name = "riba.credit"
    _description = "Bank Credit Wizard for RiBa Collections"

    # Journal and account configuration fields
    credit_journal_id = fields.Many2one(
        "account.journal",
        string="Credit Journal",
        default=_get_credit_journal_id,
    )
    credit_account_id = fields.Many2one(
        "account.account",
        string="RiBa Credit Account",
        default=_get_credit_account_id,
        help="Asset account representing amounts credited by the bank. "
        "This will be debited with the credit amount.",
    )
    credit_amount = fields.Float(
        help="Amount the bank is crediting to the company. ",
    )

    # Acceptance account configuration
    acceptance_account_id = fields.Many2one(
        "account.account",
        string="Acceptance Account",
        default=_get_acceptance_account_id,
        help="Liability account used during RiBa acceptance. "
        "This will be credited to reverse the acceptance entry.",
    )
    acceptance_amount = fields.Float(
        default=_get_acceptance_amount,
        help="Total amount from the RiBa slip that was recorded during acceptance. "
        "This amount will be used to reverse the acceptance liability.",
    )

    # Bank account and fee configuration
    bank_account_id = fields.Many2one(
        "account.account",
        string="Bank Account",
        default=_get_bank_account_id,
        help="Bank account from which collection fees will be paid. "
        "This account will be credited for any expense amounts.",
    )
    bank_expense_account_id = fields.Many2one(
        "account.account",
        string="Bank Fees Account",
        default=_get_bank_expense_account_id,
        help="Expense account for recording bank collection fees. "
        "This account will be debited for any fees charged by the bank.",
    )
    expense_amount = fields.Float(
        string="Bank Fees Amount",
        help="Amount of fees charged by the bank for the RiBa collection service. "
        "If specified, separate entries will be created for the fee payment.",
    )

    def create_move(self):
        """
        Create bank credit accounting move for RiBa slip.

        This method handles the bank credit phase of the RiBa process, where the bank
        credits the company's account with the RiBa amount (minus any fees). This
        typically happens when the bank accepts the RiBa collection and provides
        immediate liquidity to the company.

        Accounting Flow:
        1. Debit RiBa Account (asset) - Amount the bank will collect
        2. Credit Acceptance Account (liability) - Offset the acceptance entry
        3. Optional: Debit Bank Fees (expense) - Bank collection fees
        4. Optional: Credit Bank Account (asset) - Fees paid from bank account

        Business Context:
        - After RiBa acceptance, bank may credit company account immediately
        - Company receives liquidity but bank retains collection risk
        - If customer doesn't pay, bank may reverse the credit (past due)

        :return: Action to display the created accounting move
        :rtype: dict
        :raises UserError: If required accounts are not configured or active_id missing
        """
        # Validate context and get the RiBa slip
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(self.env._("No active ID found."))

        # Initialize models and get the RiBa slip
        move_model = self.env["account.move"]
        slip_model = self.env["riba.slip"]
        slip = slip_model.browse(active_id)
        wizard = self

        # Validate all required accounts are configured
        # This ensures the accounting entries can be created properly
        if (
            not wizard.credit_journal_id
            or not wizard.credit_account_id
            or not wizard.acceptance_account_id
            or not wizard.bank_account_id
            or not wizard.bank_expense_account_id
        ):
            raise UserError(self.env._("Every account is mandatory."))

        # Prepare the basic credit move with core RiBa entries
        move_vals = {
            "ref": self.env._("RiBa Credit %s") % slip.name,
            "journal_id": wizard.credit_journal_id.id,
            "line_ids": [
                # Debit RiBa Credit Account - Represents amount bank will collect
                (
                    0,
                    0,
                    {
                        "name": self.env._("Credit"),
                        "account_id": wizard.credit_account_id.id,
                        "credit": 0.0,
                        "debit": wizard.credit_amount,  # Amount bank credits to us
                    },
                ),
                # Credit Acceptance Account - Reverses the acceptance liability
                (
                    0,
                    0,
                    {
                        "name": self.env._("Acceptance Account"),
                        "account_id": wizard.acceptance_account_id.id,
                        "debit": 0.0,
                        "credit": wizard.acceptance_amount,  # Offset acceptance entry
                    },
                ),
            ],
        }

        # Add bank fee entries if applicable
        # Banks often charge fees for RiBa collection services
        if wizard.expense_amount:
            move_vals["line_ids"].extend(
                [
                    # Debit Bank Fees - Record collection expense
                    (
                        0,
                        0,
                        {
                            "name": self.env._("Bank Fee"),
                            "account_id": wizard.bank_expense_account_id.id,
                            "debit": wizard.expense_amount,  # Fee amount charged
                            "credit": 0.0,
                        },
                    ),
                    # Credit Bank Account - Payment of fees from bank balance
                    (
                        0,
                        0,
                        {
                            "name": self.env._("Bank Account"),
                            "account_id": wizard.bank_account_id.id,
                            "debit": 0.0,
                            "credit": wizard.expense_amount,  # Reduce bank balance
                        },
                    ),
                ]
            )

        # Create the accounting move
        move = move_model.create(move_vals)

        # Update RiBa slip to credited state
        vals = {
            "credit_move_id": move.id,  # Link the credit move to the slip
            "state": "credited",  # Mark slip as credited by bank
        }
        # Set credit date if not already set
        if not slip.date_credited:
            vals.update({"date_credited": fields.Date.context_today(self)})
        slip.update(vals)

        # Update all RiBa lines to credited state
        # This indicates the bank has provided credit for these collections
        for line in slip.line_ids:
            line.state = "credited"
            line.credit_move_id = move  # Link credit move to each line

        # Return action to display the created move
        return {
            "name": self.env._("Credit Entry"),
            "view_mode": "form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": move.id or False,
        }
