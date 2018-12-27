
from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    sconto_maggiorazione_product_id = fields.Many2one(
        'product.product', 'Discount Supplement Product',
        help="Product used to model ScontoMaggiorazione XML element on bills."
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    sconto_maggiorazione_product_id = fields.Many2one(
        related='company_id.sconto_maggiorazione_product_id',
        string="Discount Supplement Product",
        help='Product used to model ScontoMaggiorazione XML element on bills',
        readonly=False
        )

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.sconto_maggiorazione_product_id = (
                company.sconto_maggiorazione_product_id and
                company.sconto_maggiorazione_product_id.id or False
                )
        else:
            self.sconto_maggiorazione_product_id = False
        return res
