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
            .with_context(ctx)
            .domain_move_lines_for_reconciliation(str=str)
        )

        # Include move lines without payment_id but linked to a C/O slip
        # in order to allow closing bank statement lines with credited
        # journal items
        accr_domain = [
            "&",
            "&",
            "&",
            ("move_id.riba_accredited_ids", "!=", False),
            ("payment_id", "=", False),
            ("statement_id", "=", False),
            ("account_id", "in", reconciliation_aml_accounts),
        ]
        accr_domain = expression.AND([accr_domain, generic_domain])
        accr_res = self.env["account.move.line"].search(
            accr_domain, offset=offset, limit=limit, order="date_maturity asc, id asc"
        )

        # Include move lines without payment_id but linked to a C/O slip
        # in order to allow closing bank statement lines with past due
        # journal items
        unsolved_domain = [
            "&",
            "&",
            "&",
            ("move_id.riba_unsolved_ids", "!=", False),
            ("payment_id", "=", False),
            ("statement_id", "=", False),
            ("account_id", "in", reconciliation_aml_accounts),
        ]
        unsolved_domain = expression.AND([unsolved_domain, generic_domain])
        unsolved_res = self.env["account.move.line"].search(
            unsolved_domain,
            offset=offset,
            limit=limit,
            order="date_maturity asc, id asc",
        )

        res = accr_res | unsolved_res | res
        return res
