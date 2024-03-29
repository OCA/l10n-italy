# Copyright 2015  Davide Corio <davide.corio@abstract.it>
# Copyright 2015  Lorenzo Battistini - Agile Business Group
# Copyright 2016  Alessio Gerace - Agile Business Group
# Copyright 2023  Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sp_account_id = fields.Many2one(
        related="company_id.sp_account_id",
        string="Split Payment Write-off account",
        help="Account used to write off the VAT amount",
        readonly=False,
    )
