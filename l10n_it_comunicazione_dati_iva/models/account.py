# -*- coding: utf-8 -*-


from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    comunicazione_dati_iva_escludi = fields.Boolean(
        string='Escludi dalla dichiarazione IVA', default=False)
