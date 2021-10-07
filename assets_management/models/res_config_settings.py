from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def compute_civilistico(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_civilistico')
        ])
        return internal_sequence.res_id

    def compute_fiscale(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_fiscale')
        ])
        return internal_sequence.res_id

    def compute_gestionale(self):
        internal_sequence = self.env['ir.model.data'].search([
            ('model', '=', 'asset.depreciation.type'),
            ('name', '=', 'ad_type_gestionale')
        ])
        return internal_sequence.res_id

    civilistico = fields.Many2one(
        string='Tipo ammortamento civilistico',
        comodel_name='asset.depreciation.type',
        default=compute_civilistico,
        domain=[('requires_account_move', '=', True)]
    )

    fiscale = fields.Many2one(
        string='Tipo ammortamento fiscale',
        comodel_name='asset.depreciation.type',
        default=compute_fiscale,
    )

    gestionale = fields.Many2one(
        string='Tipo ammortamento gestionale',
        comodel_name='asset.depreciation.type',
        default=compute_gestionale,
    )


