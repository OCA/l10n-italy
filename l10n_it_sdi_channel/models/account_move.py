#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_open_export_send_sdi(self):
        """Validate, export and send to SdI the invoices."""
        # Validate
        self.action_post()

        # Export
        export_action = self.env["ir.actions.act_window"]._for_xml_id(
            "l10n_it_fatturapa_out.action_wizard_export_fatturapa",
        )
        export_wizard_model = export_action.get("res_model")
        export_wizard = (
            self.env[export_wizard_model]
            .with_context(
                active_model=self._name,
                active_ids=self.ids,
            )
            .create([{}])
        )
        export_result = export_wizard.exportFatturaPA()
        # Ensure the link of the invoice to its attachment before exporting:
        # otherwise an error during the export might break the link
        self.flush(
            fnames=[
                "fatturapa_attachment_out_id",
            ],
            records=self,
        )

        # Get the exported attachments
        attachment_model = self.env[export_result.get("res_model")]
        exported_attachments_domain = export_result.get("domain")
        if not exported_attachments_domain:
            exported_attachments_domain = [
                ("id", "=", export_result.get("res_id")),
            ]
        exported_attachments = attachment_model.search(
            exported_attachments_domain,
        )

        # Send
        send_result = exported_attachments.send_to_sdi()
        return send_result
