# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_attachment_out_id = fields.Many2one(
        'fatturapa.attachment.out', 'FatturaPA Export File',
        readonly=True)
