# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, fields


class FetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    is_fatturapa_pec = fields.Boolean(
        string="FatturaPA PEC server"
    )
