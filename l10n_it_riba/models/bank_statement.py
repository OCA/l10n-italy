# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.osv import expression


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def get_move_lines_for_reconciliation(
        self,
        excluded_ids=None,
        string=False,
        offset=0,
        limit=None,
        additional_domain=None,
        overlook_partner=False,
        partner_id=None,
    ):
        res = super(AccountBankStatementLine, self).get_move_lines_for_reconciliation(
            excluded_ids=excluded_ids,
            string=string,
            offset=offset,
            limit=limit,
            additional_domain=additional_domain,
            overlook_partner=overlook_partner,
        )

        reconciliation_aml_accounts = [
            self.journal_id.default_credit_account_id.id,
            self.journal_id.default_debit_account_id.id,
        ]
        ctx = dict(self._context or {})
        ctx["bank_statement_line"] = self
        generic_domain = (
            self.env["account.move.line"]
            .with_context(**ctx)
            .domain_move_lines_for_reconciliation(str=str)
        )

        # Include move lines without payment_id but linked to a RiBa slip
        # in order to allow closing bank statement lines with credited
        # journal items
        credited_domain = [
            "&",
            "&",
            "&",
            ("move_id.riba_credited_ids", "!=", False),
            ("payment_id", "=", False),
            ("statement_id", "=", False),
            ("account_id", "in", reconciliation_aml_accounts),
        ]
        credited_domain = expression.AND([credited_domain, generic_domain])
        credited_res = self.env["account.move.line"].search(
            credited_domain,
            offset=offset,
            limit=limit,
            order="date_maturity asc, id asc",
        )

        # Include move lines without payment_id but linked to a RiBa slip
        # in order to allow closing bank statement lines with past due
        # journal items
        past_due_domain = [
            "&",
            "&",
            "&",
            ("move_id.riba_past_due_ids", "!=", False),
            ("payment_id", "=", False),
            ("statement_id", "=", False),
            ("account_id", "in", reconciliation_aml_accounts),
        ]
        past_due_domain = expression.AND([past_due_domain, generic_domain])
        past_due_res = self.env["account.move.line"].search(
            past_due_domain,
            offset=offset,
            limit=limit,
            order="date_maturity asc, id asc",
        )

        res = credited_res | past_due_res | res
        return res
