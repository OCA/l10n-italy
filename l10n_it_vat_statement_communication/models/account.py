

from odoo import api, fields, models, _


class AccountTaxCode(models.Model):
    _inherit = "account.tax"

    vsc_exclude_operation = fields.Boolean(
        string='Escludi da operazioni attive/passive')
    vsc_exclude_vat = fields.Boolean(
        string='Escludi da iva esigibile/detratta')
