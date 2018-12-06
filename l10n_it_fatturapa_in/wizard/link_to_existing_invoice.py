# -*- coding: utf-8 -*-

from openerp import models, api, fields, _
from openerp.exceptions import Warning as UserError


class WizardLinkToInvoice(models.TransientModel):
    _name = "wizard.link.to.invoice"
    _description = "Link to Supplier Invoice"
    invoice_id = fields.Many2one(
        'account.invoice', string="Invoice", required=True)

    @api.multi
    def link(self):
        self.ensure_one()
        active_ids = self.env.context.get('active_ids')
        if len(active_ids) != 1:
            raise UserError(_("You can select only 1 XML file to link"))
        self.invoice_id.fatturapa_attachment_in_id = active_ids[0]
