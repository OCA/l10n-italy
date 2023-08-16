# Copyright 2015 Alessandro Camilli (a.camilli@openforce.it)
# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    of_account_end_vat_statement_interest = fields.Boolean(
        'Interest on End Vat Statement',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_percent = fields.Float(
        'Interest on End Vat Statement - %',
        help="Apply interest on end vat statement")
    of_account_end_vat_statement_interest_account_id = fields.Many2one(
        'account.account', 'Interest on End Vat Statement - Account',
        help="Apply interest on end vat statement")
    account_vat_period_end_statement_set_lock_date = fields.Boolean(
        string="Set Lock Date on Confirmation",
        help="When confirming the VAT period end statement, "
             "the Lock Date for Non-Advisers is set to the Statement's end date.",
    )
