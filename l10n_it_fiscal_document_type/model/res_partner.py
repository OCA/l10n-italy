# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    out_fiscal_document_type = fields.Many2one(
        'fiscal.document.type', string="Tipo documento fiscale",)
    in_fiscal_document_type = fields.Many2one(
        'fiscal.document.type', string="Tipo documento fiscale",)
