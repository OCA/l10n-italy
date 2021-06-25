# Copyright 2019 Roberto Fichera - Level Prime Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import base64
import logging

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import EFatturaOut

_logger = logging.getLogger(__name__)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def updateAttachment(self, attach, fatturapa):
        attach_str = fatturapa.to_xml(self.env)
        attach.write(
            {
                "datas": base64.encodebytes(attach_str),
            }
        )

    def exportFatturaPARegenerate(self):
        invoice_obj = self.env["account.move"]
        attachments = self.env["fatturapa.attachment.out"]
        # Browse active invoice
        active_invoice = invoice_obj.browse(self._context.get("active_id"))

        if not active_invoice:
            raise ValidationError(_("The method can be called with a valid active_id"))

        # Search all the invoices belonging the same xml file
        invoices = invoice_obj.search(
            [
                (
                    "fatturapa_attachment_out_id",
                    "=",
                    active_invoice.fatturapa_attachment_out_id.id,
                )
            ]
        )

        attach = active_invoice.fatturapa_attachment_out_id
        if not attach:
            raise ValidationError(
                _(
                    "The invoice cannot be regenerated because doesn't have a "
                    "e-invoice attachment associated to it"
                )
            )

        partner = active_invoice.partner_id
        context_partner = self.env.context.copy()
        context_partner.update({"lang": partner.lang})

        progressivo_invio = attach.name.split("_")[1].split(".")[0]
        for invoice in invoices:
            fatturapa = EFatturaOut(self, partner, invoice, progressivo_invio)
            self.updateAttachment(attach, fatturapa)

        attachments += attach

        action = {
            "view_type": "form",
            "name": "Re-Export Electronic Invoice",
            "res_model": "fatturapa.attachment.out",
            "type": "ir.actions.act_window",
        }

        if len(attachments) == 1:
            action["view_mode"] = "form"
            action["res_id"] = attachments[0].id
        else:
            action["view_mode"] = "tree,form"
            action["domain"] = [("id", "in", attachments.ids)]

        return action
