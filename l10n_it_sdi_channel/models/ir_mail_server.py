# -*- coding: utf-8 -*-
# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    is_fatturapa_pec = fields.Boolean("FatturaPA PEC server")
    email_from_for_fatturaPA = fields.Char(
        "Sender Email Address")
