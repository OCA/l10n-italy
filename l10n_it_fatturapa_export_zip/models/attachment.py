from odoo import fields, models


class FatturaAttachmentOut(models.Model):
    _inherit = ["fatturapa.attachment.out"]

    exported_zip = fields.Many2one("ir.attachment", "Exported ZIP", readonly=True)


class FatturaAttachmentIn(models.Model):
    _inherit = ["fatturapa.attachment.in"]

    exported_zip = fields.Many2one("ir.attachment", "Exported ZIP", readonly=True)
