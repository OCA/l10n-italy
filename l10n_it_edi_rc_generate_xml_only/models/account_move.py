# Copyright 2026 Marco Colombo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models

from odoo.addons.base.models.ir_qweb_fields import Markup, nl2br


class AccountMove(models.Model):
    _inherit = "account.move"

    def _l10n_it_generate_xml_for_self_invoice_or_invoice(self):
        """Validate the move data and generate the FatturaPA XML attachment.

        Works for both self-invoices (purchase journals) and regular customer
        invoices (sale journals): the base l10n_it_edi XML generation chain has
        no journal-type restriction.

        :return: the errors dict from ``_l10n_it_edi_export_data_check()``
          (empty when the XML was generated successfully)
        """
        self.ensure_one()

        if errors := self._l10n_it_edi_export_data_check():
            return errors

        attachment_vals = self._l10n_it_edi_get_attachment_values(pdf_values=None)
        self.env["ir.attachment"].create(attachment_vals)
        self.invalidate_recordset(
            fnames=["l10n_it_edi_attachment_id", "l10n_it_edi_attachment_file"]
        )
        return {}

    def _l10n_it_edi_error_messages(self, errors):
        """Turn the errors dict from ``_l10n_it_edi_export_data_check()`` into a
        list of plain-text messages (no HTML markup).
        """
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
            messages.append(message)
        return messages

    def _l10n_it_edi_errors_to_messages(self, errors):
        """HTML variant of ``_l10n_it_edi_error_messages()``, suitable for the
        ``l10n_it_edi_header`` widget.
        """
        return [nl2br(message) for message in self._l10n_it_edi_error_messages(errors)]

    def action_l10n_it_edi_generate_xml(self):
        """Validate the move data, generate the FatturaPA XML, attach it and
        post it to the chatter, but do NOT send it to the SdI and do NOT
        mark the move as sent.

        Supports both single-record and multi-record (batch) calls, for
        self-invoices (purchase journals) and regular customer invoices (sale
        journals).
        """
        if len(self) == 1:
            return self._action_l10n_it_edi_generate_xml_single()
        return self._action_l10n_it_edi_generate_xml_batch()

    def _action_l10n_it_edi_generate_xml_single(self):
        """Single-record implementation.

        A reload client action is returned on validation failure (with the error
        header set); the return value is falsy on success (header cleared).
        """
        self.ensure_one()

        if self.l10n_it_edi_attachment_id:
            # XML already generated, just resurface it in the chatter
            self.with_context(no_new_invoice=True).message_post(
                attachment_ids=self.l10n_it_edi_attachment_id.ids
            )
            self.l10n_it_edi_header = False
            return

        errors = self._l10n_it_generate_xml_for_self_invoice_or_invoice()
        if errors:
            # Update the vendor bill's header with the warning messages,
            # and force reload the view to make sure the header is loaded
            self.l10n_it_edi_header = Markup("<br/>").join(
                self._l10n_it_edi_errors_to_messages(errors)
            )
            return {
                "type": "ir.actions.client",
                "tag": "reload",
            }

        self.with_context(no_new_invoice=True).message_post(
            attachment_ids=self.l10n_it_edi_attachment_id.ids
        )
        self.l10n_it_edi_header = False

    def _action_l10n_it_edi_generate_xml_batch(self):
        """Multi-record implementation for the list view.

        Moves that already have an attachment and moves that are not eligible
        (not posted, fiscal country != IT, EDI state not in (False, 'rejected'),
        or already sent) are skipped. The remaining eligible moves are processed
        individually: a move failing validation is collected but does not abort
        the others, so successful generations are committed even when some moves
        fail.

        :return: a client notification action summarising the outcome, or False
          when there is nothing to report (no failures and no skips)
        """
        already_generated = self.filtered("l10n_it_edi_attachment_id")
        to_process = self - already_generated

        ineligible = to_process.filtered(
            lambda move: not self._l10n_it_edi_is_eligible_for_xml_generation(move)
        )
        to_generate = to_process - ineligible

        failures = []
        generated = 0
        for move in to_generate:
            errors = move._l10n_it_generate_xml_for_self_invoice_or_invoice()
            if errors:
                failures.append(
                    (move, "; ".join(move._l10n_it_edi_error_messages(errors)))
                )
            else:
                generated += 1
                move.with_context(no_new_invoice=True).message_post(
                    attachment_ids=move.l10n_it_edi_attachment_id.ids
                )

        if not failures and not already_generated and not ineligible:
            return False

        parts = []
        if generated:
            parts.append(_("Generated XML for %s move(s).", generated))
        for move, reason in failures:
            parts.append(f"{move.display_name}: {reason}")
        if already_generated:
            parts.append(
                _(
                    "Skipped %s move(s) that already had an attachment.",
                    len(already_generated),
                )
            )
        if ineligible:
            parts.append(
                _(
                    "Skipped %s move(s) that are not eligible for XML generation.",
                    len(ineligible),
                )
            )
        if not parts:
            return False

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("FatturaPA XML generation"),
                "message": " · ".join(parts),
                "sticky": True,
                "type": "warning" if failures else "success",
            },
        }

    @staticmethod
    def _l10n_it_edi_is_eligible_for_xml_generation(move):
        """Whether a move is eligible for XML generation.

        Unlike ``_l10n_it_edi_ready_for_xml_export()`` (which is restricted to
        sale journals), this accepts both self-invoices (purchase journals) and
        regular customer invoices (sale journals). A 'rejected' EDI state stays
        eligible on purpose: regenerating after a SdI rejection is legitimate.

        Moves that already have an attachment are filtered out by the batch
        caller *before* this check (see ``_action_l10n_it_edi_generate_xml_batch``),
        so the predicate does not need to re-check ``l10n_it_edi_attachment_id``.
        Consequently it must not be used as a standalone gate by callers that
        have not performed that subtraction first.
        """
        return (
            move.state == "posted"
            and move.company_id.account_fiscal_country_id.code == "IT"
            and move.l10n_it_edi_state in (False, "rejected")
            and not move.is_move_sent
        )

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
