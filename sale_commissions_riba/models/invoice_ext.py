from odoo import api, exceptions, fields, models, _


class InvoiceExtended(models.Model):
    _inherit = "account.invoice"

    no_commission = fields.Boolean(string="Non considerare provvigioni")
