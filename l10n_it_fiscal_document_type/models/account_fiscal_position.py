from odoo import models, fields


class AccountFiscalPosition(models.Model):
    _name = 'account.fiscal.position'
    _inherit = ['account.fiscal.position', 'l10n_it_account.mixin']

    fiscal_document_type_id = fields.Many2one(
        'fiscal.document.type',
        string="Fiscal Document Type",
        readonly=False
    )
