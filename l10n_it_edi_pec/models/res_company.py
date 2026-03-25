# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_it_edi_use_pec = fields.Boolean(
        string="Use PEC for e-invoicing",
        help="If enabled, electronic invoices will be sent and received "
        "through PEC (Certified Email) instead of the standard IAP proxy.",
    )
    l10n_it_edi_pec_server_id = fields.Many2one(
        "ir.mail_server",
        string="Outgoing PEC server",
        domain=[("is_l10n_it_edi_pec", "=", True)],
    )
    l10n_it_edi_pec_fetch_server_id = fields.Many2one(
        "fetchmail.server",
        string="Incoming PEC server",
        domain=[("is_l10n_it_edi_pec", "=", True)],
    )
    l10n_it_edi_pec_email_exchange_system = fields.Char(
        string="SDI PEC Email Address",
        help="PEC address used to communicate with the Exchange System (SDI).",
    )

    def _l10n_it_edi_export_check(self):
        non_pec = self.filtered(lambda c: not c.l10n_it_edi_use_pec)
        pec_companies = self - non_pec
        if non_pec:
            result = super(ResCompany, non_pec)._l10n_it_edi_export_check()
        else:
            result = {}
        if not pec_companies:
            return result
        # Add PEC-specific checks
        for company in pec_companies:
            smtp = company.l10n_it_edi_pec_server_id
            fetch = company.l10n_it_edi_pec_fetch_server_id
            if not smtp:
                result["l10n_it_edi_pec_server"] = {
                    "message": _("Please configure an outgoing PEC server."),
                }
            elif not smtp.l10n_it_edi_pec_email_from:
                result["l10n_it_edi_pec_email_from"] = {
                    "message": _(
                        "Please configure the PEC sender email address "
                        "on the outgoing PEC server."
                    ),
                }
            if not fetch:
                result["l10n_it_edi_pec_fetch_server"] = {
                    "message": _("Please configure an incoming PEC server."),
                }
            elif fetch.state != "done":
                result["l10n_it_edi_pec_fetch_server_state"] = {
                    "message": _("The incoming PEC server must be confirmed."),
                }
            if not company.l10n_it_edi_pec_email_exchange_system:
                result["l10n_it_edi_pec_email_exchange_system"] = {
                    "message": _("Please configure the SDI PEC email address."),
                }
        return result
