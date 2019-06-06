

from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string='Exclude from invoices communication')
