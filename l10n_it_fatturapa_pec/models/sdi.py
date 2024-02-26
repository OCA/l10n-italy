# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    channel_type = fields.Selection(
        selection_add=[("pec", "PEC")], ondelete={"pec": "cascade"}
    )

    # SdiChannelPEC
    pec_server_id = fields.Many2one(
        "ir.mail_server",
        string="Outgoing PEC server",
        required=False,
        domain=[("is_fatturapa_pec", "=", True)],
    )
    # This is only used in configuration, to force the user to create one
    fetch_pec_server_id = fields.Many2one(
        "fetchmail.server",
        string="Incoming PEC server",
        required=False,
        domain=[("is_fatturapa_pec", "=", True)],
    )
    email_exchange_system = fields.Char(
        "Exchange System Email Address",
        help="The first time you send a PEC to SDI, you must use the address "
        "sdi01@pec.fatturapa.it . The system, with the first response "
        "or notification, communicates the PEC address to be used for "
        "future messages",
        default=lambda self: self.env["ir.config_parameter"].get_param(
            "sdi.pec.first.address"
        ),
    )
    first_invoice_sent = fields.Boolean(
        "SDI already assigned a PEC address to my company",
        help="This is set after having sent the first e-invoice to SDI",
    )

    @api.constrains("fetch_pec_server_id")
    def check_fetch_pec_server_id(self):
        for channel in self:
            domain = [("fetch_pec_server_id", "=", channel.fetch_pec_server_id.id)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise exceptions.ValidationError(
                    _(
                        "The channel %(name)s with pec server "
                        "%(server_name)s already exists"
                    )
                    % {
                        "name": channel.name,
                        "server_name": channel.fetch_pec_server_id.name,
                    }
                )

    @api.constrains("pec_server_id")
    def check_pec_server_id(self):
        for channel in self:
            domain = [("pec_server_id", "=", channel.pec_server_id.id)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise exceptions.ValidationError(
                    _(
                        "The channel %(name)s with pec server "
                        "%(server_name)s already exists"
                    )
                    % {
                        "name": channel.name,
                        "server_name": channel.pec_server_id.name,
                    }
                )

    @api.constrains("email_exchange_system")
    def check_email_validity(self):
        if self.env.context.get("skip_check_email_validity"):
            return
        for channel in self:
            if not extract_rfc2822_addresses(channel.email_exchange_system):
                raise exceptions.ValidationError(
                    _("Email %s is not valid") % channel.email_exchange_system
                )

    def check_first_pec_sending(self):
        sdi_address = self.env["ir.config_parameter"].get_param("sdi.pec.first.address")
        if not self.first_invoice_sent:
            if self.email_exchange_system != sdi_address:
                raise exceptions.UserError(
                    _("This is a first sending but SDI address is different " "from %s")
                    % sdi_address
                )
        else:
            if not self.email_exchange_system:
                raise exceptions.UserError(
                    _(
                        "SDI PEC address not set. Please update it with the "
                        "address indicated by SDI after the first sending"
                    )
                )

    def update_after_first_pec_sending(self):
        if not self.first_invoice_sent:
            self.first_invoice_sent = True
            self.with_context(
                skip_check_email_validity=True
            ).email_exchange_system = False
