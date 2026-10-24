# Copyright 2024 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, fields, models
from odoo.exceptions import UserError


def _default_datetime_from(self):
    return fields.Datetime.now() - timedelta(days=30)


class PecEInvoiceCheckWizard(models.TransientModel):
    _name = "pec.e_invoice.check.wizard"
    _description = "Check received PEC e-invoices"

    fetchmail_server_id = fields.Many2one(
        "fetchmail.server", string="PEC server", required=True, readonly=True
    )
    datetime_from = fields.Datetime(
        string="From", required=True, default=_default_datetime_from
    )
    datetime_to = fields.Datetime(
        string="To", required=True, default=fields.Datetime.now
    )
    filter = fields.Selection(
        [("to_import", "To import"), ("imported", "Imported")],
        string="Show",
        default="to_import",
        required=True,
    )
    line_ids = fields.One2many(
        "pec.e_invoice.check.line", "wizard_id", string="E-invoices found"
    )
    to_import_line_ids = fields.One2many(
        "pec.e_invoice.check.line",
        "wizard_id",
        string="E-invoices to import",
        domain=[("is_einvoice_xml_found", "=", False)],
    )
    imported_line_ids = fields.One2many(
        "pec.e_invoice.check.line",
        "wizard_id",
        string="Imported e-invoices",
        domain=[("is_einvoice_xml_found", "=", True)],
    )

    def _reopen_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Check received PEC e-invoices"),
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_check(self):
        """Check the PEC mailbox and show the e-invoices found."""
        self.ensure_one()
        found_e_invoices = self.fetchmail_server_id.check_received_e_invoices(
            self.datetime_from, self.datetime_to
        )
        self.line_ids.unlink()
        line_model = self.env["pec.e_invoice.check.line"]
        for found_e_invoice in found_e_invoices:
            values = dict(found_e_invoice)
            values["wizard_id"] = self.id
            values["to_import"] = not values["is_einvoice_xml_found"]
            line_model.create(values)
        return self._reopen_wizard()

    def action_import_selected(self):
        """Import the e-invoices selected by the user."""
        self.ensure_one()
        lines = self.line_ids.filtered("to_import")
        if not lines:
            raise UserError(_("Select at least one e-invoice to import."))
        message_ids = set(lines.mapped("message_id"))
        self.fetchmail_server_id._import_pec_messages(
            self.datetime_from, self.datetime_to, message_ids
        )
        self.line_ids.filtered(lambda line: line.message_id in message_ids).unlink()
        if not self.line_ids:
            return {"type": "ir.actions.act_window_close"}
        return self._reopen_wizard()


class PecEInvoiceCheckLine(models.TransientModel):
    _name = "pec.e_invoice.check.line"
    _description = "PEC e-invoice to import"
    _order = "date asc, id"

    wizard_id = fields.Many2one(
        "pec.e_invoice.check.wizard",
        string="Wizard",
        required=True,
        ondelete="cascade",
    )
    to_import = fields.Boolean(
        string="Force import",
        default=True,
        help="Select the e-invoices to import.",
    )
    is_einvoice_xml_found = fields.Boolean(string="E-invoice XML found", readonly=True)
    date = fields.Datetime(string="Received on", readonly=True)
    email_from = fields.Char(string="From", readonly=True)
    subject = fields.Char(readonly=True)
    file_name = fields.Char(string="E-invoice file names", readonly=True)
    message_id = fields.Char(string="Message ID", readonly=True)
