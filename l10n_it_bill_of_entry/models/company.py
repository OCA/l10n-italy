#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    bill_of_entry_journal_id = fields.Many2one(
        "account.journal",
        "Bill of entry Storno journal",
        help="Journal used for reconciliation of bill of entries",
    )
    bill_of_entry_tax_id = fields.Many2one(
        "account.tax",
        "Bill of entry tax",
        help="Tax used in bill of entries",
    )
    bill_of_entry_partner_id = fields.Many2one(
        "res.partner",
        "Bill of entry partner",
        help="Supplier used in bill of entries",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    bill_of_entry_journal_id = fields.Many2one(
        "account.journal",
        related="company_id.bill_of_entry_journal_id",
        readonly=False,
    )
    bill_of_entry_tax_id = fields.Many2one(
        "account.tax",
        related="company_id.bill_of_entry_tax_id",
        readonly=False,
    )
    bill_of_entry_partner_id = fields.Many2one(
        "res.partner",
        related="company_id.bill_of_entry_partner_id",
        readonly=False,
    )
