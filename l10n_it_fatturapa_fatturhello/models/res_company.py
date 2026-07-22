# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fatturhello_identifier = fields.Char(
        readonly=True,
        help="Identifier of this company in Fatturhello, "
        "set automatically during login.",
    )
    fatturhello_last_downloaded_e_bill_identifer = fields.Char(
        help="Fatturhello's protocol number of the last E-Bill downloaded.\n"
        "All the E-Bills subsequent this one will be downloaded "
        "during the CRON execution.\n"
        "If empty, all the E-Bills in Fatturhello will be downloaded.",
    )
