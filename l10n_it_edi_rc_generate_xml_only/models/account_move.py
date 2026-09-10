# Copyright 2026 Marco Colombo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.base.models.ir_qweb_fields import Markup, nl2br


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_l10n_it_edi_generate_xml(self):
        """Validate the move data, generate the FatturaPA XML, attach it and
        post it to the chatter, but do NOT send it to the SdI and do NOT
        mark the move as sent.
        """
        self.ensure_one()

        if errors := self._l10n_it_edi_export_data_check():
            messages = []
            for error_key, error_data in errors.items():
                message = error_data["message"]
                model_map = {
                    "partner": "res.partner",
                    "move": "account.move",
                    "company": "res.company",
                }
                split = error_key.split("_")
                if len(split) > 3 and (model_name := model_map.get(split[3])):
                    if action := error_data.get("action"):
                        if "res_id" in action:
                            record_ids = [action["res_id"]]
                        else:
                            record_ids = action["domain"][0][2]
                        records = self.env[model_name].browse(record_ids)
                        record_str = ", ".join(records.mapped("display_name"))
                        message = f"{message} - {record_str}"
                messages.append(nl2br(message))

            # Update the vendor bill's header with the warning messages,
            # and force reload the view to make sure the header is loaded
            self.l10n_it_edi_header = Markup("<br/>").join(messages)
            return {
                "type": "ir.actions.client",
                "tag": "reload",
            }

        if self.l10n_it_edi_attachment_id:
            # XML already generated, just resurface it in the chatter
            self.message_post(attachment_ids=self.l10n_it_edi_attachment_id.ids)
        else:
            attachment_vals = self._l10n_it_edi_get_attachment_values(pdf_values=None)
            self.env["ir.attachment"].create(attachment_vals)
            self.invalidate_recordset(
                fnames=["l10n_it_edi_attachment_id", "l10n_it_edi_attachment_file"]
            )
            self.message_post(attachment_ids=self.l10n_it_edi_attachment_id.ids)

        self.l10n_it_edi_header = False

    def action_l10n_it_edi_send(self):
        """Send the self-invoice to the SdI, reusing an existing generated XML
        attachment when available.
        """
        self.ensure_one()

        if result := self.action_l10n_it_edi_generate_xml():
            return result

        if not (attachment := self.l10n_it_edi_attachment_id):
            return

        attachment_vals = {
            "name": attachment.name,
            "raw": attachment.raw,
        }
        self._l10n_it_edi_send({self: attachment_vals})
        self.is_move_sent = True
