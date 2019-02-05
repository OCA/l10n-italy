# -*- coding: utf-8 -*-

from odoo import models, fields


class FatturaAttachmentOut(models.Model):
    _inherit = ['fatturapa.attachment.out']

    zip_exported = fields.Boolean('Zip Exported')


class FatturaAttachmentIn(models.Model):
    _inherit = ['fatturapa.attachment.in']

    zip_exported = fields.Boolean('Zip Exported')
