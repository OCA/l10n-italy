# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    is_fatturapa_pec = fields.Boolean("E-invoice PEC server")
