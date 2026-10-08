# Copyright 2015 Alessandro Camilli (a.camilli@openforce.it)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    of_account_end_vat_statement_interest = fields.Boolean(
        "Interest on End Vat Settlement", help="Apply interest on end vat settlement"
    )
    of_account_end_vat_statement_interest_percent = fields.Float(
        "Interest on End Vat Settlement - %",
        help="Apply interest on end vat settlement",
    )
    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        "account.account",
        "Interest on End Vat Settlement - Account",
        help="Apply interest on end vat settlement",
    )
