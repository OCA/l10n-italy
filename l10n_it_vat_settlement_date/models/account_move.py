# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    date_vat_settlement = fields.Date(
        "VAT Settlement Date", default=lambda self: self.date
    )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    date_vat_settlement = fields.Date(
        "VAT Settlement Date",
        related="move_id.date_vat_settlement",
        index=True,
        store=True,
        copy=False,
        readonly=False,
    )
