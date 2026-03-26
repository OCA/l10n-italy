# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# Copyright 2024 Simone Rubino - Aion Tech
# Copyright 2026 Andrea Martinelli - MKT SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_it_vat_settlement_date = fields.Date(
        string="VAT Settlement Date",
        compute="_compute_l10n_it_vat_settlement_date",
        store=True,
        readonly=False,
        copy=False,
        states={
            "posted": [
                ("readonly", True),
            ],
        },
    )

    @api.depends(
        "date",
        "invoice_date",
    )
    def _compute_l10n_it_vat_settlement_date(self):
        for move in self:
            settlement_date = (
                move.date or move.invoice_date or fields.Date.context_today(move)
            )
            move.l10n_it_vat_settlement_date = settlement_date

    def _get_violated_lock_dates(self, invoice_date, has_tax):
        settlement_date = self.l10n_it_vat_settlement_date
        if has_tax and settlement_date and invoice_date == self.date:
            # When tax is involved,
            # VAT Settlement Date is the date that has to be after the lock.
            invoice_date = settlement_date
        return super()._get_violated_lock_dates(invoice_date, has_tax)

    def _get_lock_date_message(self, invoice_date, has_tax):
        message = super()._get_lock_date_message(invoice_date, has_tax)
        if message:
            lock_dates = self._get_violated_lock_dates(invoice_date, has_tax)
            settlement_date = self.l10n_it_vat_settlement_date
            if lock_dates and has_tax and settlement_date and invoice_date == self.date:
                # The super's message talks about a generic date.
                # When tax is involved,
                # VAT Settlement Date is the date that has to be after the lock,
                # and it will be moved too.
                lock_date, lock_type = lock_dates[-1]
                unlocked_invoice_date = self._get_accounting_date(invoice_date, has_tax)
                message = _(
                    "The VAT Settlement Date is being set "
                    "prior to the %(lock_type)s lock date %(lock_date)s.\n"
                    "The Journal Entry will be accounted "
                    "on %(unlocked_invoice_date)s upon posting.",
                    lock_type=lock_type,
                    lock_date=format_date(self.env, lock_date),
                    unlocked_invoice_date=format_date(self.env, unlocked_invoice_date),
                )
            message = "\n".join(
                [
                    message,
                    _(
                        "Both VAT Settlement Date and accounting date "
                        "will be changed upon posting.",
                    ),
                ]
            )
        return message

    @api.depends(
        "l10n_it_vat_settlement_date",
    )
    def _compute_tax_lock_date_message(self):
        return super()._compute_tax_lock_date_message()

    def write(self, vals):
        for move in self:
            lock_date = move.company_id._get_user_fiscal_lock_date()
            if (
                (not self.env.context.get("bypass_journal_lock_date"))
                and move.journal_id
                and hasattr(move.journal_id, "fiscalyear_lock_date")
            ):
                date_min = fields.date.min
                if self.user_has_groups("account.group_account_manager"):
                    lock_date = move.journal_id.fiscalyear_lock_date or date_min
                else:
                    lock_date = max(
                        move.journal_id.period_lock_date or date_min,
                        move.journal_id.fiscalyear_lock_date or date_min,
                    )

            if (
                move.l10n_it_vat_settlement_date
                and move.l10n_it_vat_settlement_date <= lock_date
            ):
                raise UserError(
                    _(
                        "You cannot add/modify entries with settlement date "
                        "(%(settlement)s) prior to and inclusive of the lock date "
                        "%(lock)s."
                    )
                    % {
                        "settlement": format_date(
                            self.env, move.l10n_it_vat_settlement_date
                        ),
                        "lock": format_date(self.env, lock_date),
                    }
                )
            if "l10n_it_vat_settlement_date" in vals:
                if vals["l10n_it_vat_settlement_date"]:
                    settlement_date = fields.Date.to_date(
                        vals["l10n_it_vat_settlement_date"]
                    )
                    if settlement_date <= lock_date:
                        raise UserError(
                            _(
                                "You cannot set a settlement date (%(settlement)s) "
                                "prior to and inclusive of the lock date %(lock)s."
                            )
                            % {
                                "settlement": format_date(self.env, settlement_date),
                                "lock": format_date(self.env, lock_date),
                            }
                        )

        res = super().write(vals)
        return res
