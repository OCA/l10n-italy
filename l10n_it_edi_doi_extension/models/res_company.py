from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_it_edi_doi_bill_tax_id = fields.Many2one(
        comodel_name="account.tax",
        string="Declaration of Intent Bills Tax",
    )
