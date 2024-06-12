# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    compute_on_einvoice_values = fields.Boolean(
        string="Compute imported invoices on e-invoices precision values",
        help="Import vendor invoices preserving e-invoices datas.",
    )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    compute_on_einvoice_values = fields.Boolean(
        related='company_id.compute_on_einvoice_values',
        string="Compute imported invoices on e-invoices precision values",
        help="Import vendor invoices preserving e-invoices datas.",
        readonly=False,
    )
