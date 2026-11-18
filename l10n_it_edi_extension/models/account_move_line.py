# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# Copyright 2026 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    l10n_it_edi_admin_ref = fields.Char(string="Admin. ref.", size=20, copy=False)
    l10n_it_edi_other_data_ids = fields.One2many(
        "l10n_it_edi.line_other_data",
        "move_line_id",
        string="Other Management Data",
        copy=True,
        help="Additional management data (AltriDatiGestionali) to be exported "
        "in the FatturaPA XML.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get("l10n_it_edi_extension_avoid_off_balance_accounts"):
            for vals in vals_list:
                self._l10n_it_edi_extension_avoid_off_balance_tax_account(vals)
        return super().create(vals_list)

    def _l10n_it_edi_extension_get_non_off_balance_tax_account(self, tax_line_vals):
        """Return a valid account for a tax line created during an EDI import."""
        repartition_line = self.env["account.tax.repartition.line"].browse(
            tax_line_vals.get("tax_repartition_line_id")
        )
        tax = repartition_line.tax_id
        move = self.env["account.move"].browse(tax_line_vals.get("move_id"))
        company = move.company_id or self.env.company

        if tax:
            tax_group = tax.tax_group_id
            fallback_account = (
                tax_group.tax_receivable_account_id
                if tax.type_tax_use == "purchase"
                else tax_group.tax_payable_account_id
            )
            if fallback_account and fallback_account.account_type not in (
                "asset_receivable",
                "liability_payable",
                "off_balance",
            ):
                return fallback_account

            # VAT current accounts are the natural fallback for a tax line:
            # credit VAT for purchases, debit VAT for sales.
            account_model = self.env["account.account"].with_company(company)
            account_type = (
                "asset_current"
                if tax.type_tax_use == "purchase"
                else "liability_current"
            )
            company_domain = account_model._check_company_domain(company)
            vat_account = account_model.search(
                [
                    *company_domain,
                    ("account_type", "=", account_type),
                    ("deprecated", "=", False),
                    "|",
                    ("name", "ilike", "IVA"),
                    ("name", "ilike", "VAT"),
                ],
                limit=1,
            )
            if vat_account:
                return vat_account
            current_account = account_model.search(
                [
                    *company_domain,
                    ("account_type", "=", account_type),
                    ("deprecated", "=", False),
                ],
                limit=1,
            )
            if current_account:
                return current_account

        if move.journal_id.default_account_id:
            fallback_account = move.journal_id.default_account_id
            if fallback_account.account_type != "off_balance":
                return fallback_account

        # As a last resort, use an account already used by the move.
        for line in move.line_ids:
            if line.account_id and line.account_id.account_type != "off_balance":
                return line.account_id
        return self.env["account.account"]

    def _l10n_it_edi_extension_avoid_off_balance_tax_account(self, vals):
        """Replace an off-balance account on a tax line imported from an e-invoice.

        Odoo 18 checks the whole journal entry when a line is created: a tax line
        on an off-balance account would make the import fail as soon as it is
        created, even if the invoice lines use regular accounts.
        """
        account_id = vals.get("account_id")
        if not account_id or not vals.get("tax_repartition_line_id"):
            return
        account = self.env["account.account"].browse(account_id)
        if account.account_type != "off_balance":
            return
        fallback_account = self._l10n_it_edi_extension_get_non_off_balance_tax_account(
            vals
        )
        if not fallback_account:
            return
        _logger.warning(
            "Replacing the off-balance account %s with %s on an imported "
            "e-invoice tax line.",
            account.display_name,
            fallback_account.display_name,
        )
        vals["account_id"] = fallback_account.id

    def action_open_other_data(self):
        """Open a popup to manage Other Management Data for this invoice line."""
        self.ensure_one()
        return {
            "name": "Altri Dati Gestionali",
            "type": "ir.actions.act_window",
            "res_model": "l10n_it_edi.line_other_data",
            "view_mode": "list,form",
            "domain": [("move_line_id", "=", self.id)],
            "context": {
                "default_move_line_id": self.id,
            },
            "target": "new",
        }
