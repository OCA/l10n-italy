from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    draft_delivery_note_invoicing_notify = \
        fields.Boolean(string="Notify if delivery note isn't validated")
