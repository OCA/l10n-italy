# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    sp_account_id = fields.Many2one(
        "account.account",
        string="Split Payment Write-off Account",
        help="Account used to write off the VAT amount",
        readonly=False,
    )
