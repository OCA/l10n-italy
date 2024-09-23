# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RibaCredit(models.TransientModel):
    @api.model
    def _get_credit_journal_id(self):
        return self.env["riba.configuration"].get_default_value_by_list(
            "credit_journal_id"
        )

    @api.model
    def _get_credit_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list(
            "credit_account_id"
        )

    @api.model
    def _get_bank_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list(
            "bank_account_id"
        )

    @api.model
    def _get_bank_expense_account_id(self):
        return self.env["riba.configuration"].get_default_value_by_list(
            "bank_expense_account_id"
        )

    @api.model
    def _get_credit_amount(self):
        if not self.env.context.get("active_id", False):
            return False
        slip_model = self.env["riba.slip"]
        slip = slip_model.browse(self.env.context["active_id"])
        amount = 0.0
        for line in slip.line_ids:
            amount += line.amount
        return amount

    _name = "riba.credit"
    _description = "Bank Credit"
    credit_journal_id = fields.Many2one(
        "account.journal",
        "Credit Journal",
        domain=[("type", "=", "bank")],
        default=_get_credit_journal_id,
    )
    credit_account_id = fields.Many2one(
        "account.account", "RiBa Account", default=_get_credit_account_id
    )
    credit_amount = fields.Float(default=_get_credit_amount)
    bank_account_id = fields.Many2one(
        "account.account",
        "A/C Bank Account",
        domain=[("account_type", "=", "asset_cash")],
        default=_get_bank_account_id,
    )
    bank_amount = fields.Float("Paid Amount")
    bank_expense_account_id = fields.Many2one(
        "account.account", "Bank Fees Account", default=_get_bank_expense_account_id
    )
    expense_amount = fields.Float("Fees Amount")

    def skip(self):
        active_id = self.env.context.get("active_id") or False
        if not active_id:
            raise UserError(_("No active ID found."))
        riba_slip = self.env["riba.slip"].browse(active_id)
        riba_slip.state = "credited"
        riba_slip.line_ids.state = "credited"
        return {"type": "ir.actions.act_window_close"}

    def create_move(self):
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("No active ID found."))
        move_model = self.env["account.move"]
        slip_model = self.env["riba.slip"]
        slip = slip_model.browse(active_id)
        wizard = self
        if (
            not wizard.credit_journal_id
            or not wizard.credit_account_id
            or not wizard.bank_account_id
            or not wizard.bank_expense_account_id
        ):
            raise UserError(_("Every account is mandatory."))
        move_vals = {
            "ref": _("RiBa Credit %s") % slip.name,
            "journal_id": wizard.credit_journal_id.id,
            "line_ids": [
                (
                    0,
                    0,
                    {
                        "name": _("Credit"),
                        "account_id": wizard.credit_account_id.id,
                        "credit": wizard.credit_amount,
                        "debit": 0.0,
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": _("A/C Bank"),
                        "account_id": wizard.bank_account_id.id,
                        "debit": wizard.bank_amount,
                        "credit": 0.0,
                    },
                ),
            ],
        }

        if wizard.expense_amount:
            move_vals["line_ids"].append(
                (
                    0,
                    0,
                    {
                        "name": _("Bank Fee"),
                        "account_id": wizard.bank_expense_account_id.id,
                        "debit": wizard.expense_amount,
                        "credit": 0.0,
                    },
                ),
            )

        move = move_model.create(move_vals)
        vals = {
            "credit_move_id": move.id,
            "state": "credited",
        }
        if not slip.date_credited:
            vals.update({"date_credited": fields.Date.context_today(self)})
        slip.update(vals)

        for line in slip.line_ids:
            line.state = "credited"

        return {
            "name": _("Credit Entry"),
            "view_mode": "form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "target": "current",
            "res_id": move.id or False,
        }
