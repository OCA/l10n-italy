from odoo import models, fields


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'l10n_it_account.mixin']

    out_fiscal_document_type = fields.Many2one(
        'fiscal.document.type', string="Out Fiscal Document Type",)
    in_fiscal_document_type = fields.Many2one(
        'fiscal.document.type', string="In Fiscal Document Type",)
