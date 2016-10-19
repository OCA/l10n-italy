# -*- coding: utf-8 -*-
# Copyright (C) 2014 Davide Corio
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.osv import fields, orm


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'fatturapa_attachment_out_id': fields.many2one(
            'fatturapa.attachment.out', 'FatturaPA Export File',
            readonly=True),
    }
