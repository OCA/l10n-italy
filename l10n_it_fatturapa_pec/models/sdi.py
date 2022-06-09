# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models

from odoo.addons.base.models.ir_mail_server import extract_rfc2822_addresses, \
    MailDeliveryException
from odoo.exceptions import UserError


class SdiChannel(models.Model):
    _inherit = "sdi.channel"

    channel_type = fields.Selection(
        selection_add=[("pec", "PEC")],
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
        "sdi01@pec.fatturapa.it.\n"
        "Odoo will automatically set this address "
        "the first time you send an e-invoice to SdI using this channel.\n"
        "The system, with the first response "
        "or notification, communicates the PEC address to be used for "
        "future messages",
    )
    first_invoice_sent = fields.Boolean(
        "SDI already assigned a PEC address to my company",
        help="This is set after having sent the first e-invoice to SDI",
    )

    @api.constrains("fetch_pec_server_id")
    def check_fetch_pec_server_id(self):
        pec_channels = self.filtered(lambda c: c.channel_type == 'pec')
        for channel in pec_channels:
            domain = [
                ("fetch_pec_server_id", "=", channel.fetch_pec_server_id.id),
                ("id", 'in', pec_channels.ids),
            ]
            elements = self.search(domain)
            if len(elements) > 1:
                raise exceptions.ValidationError(
                    _("The channel %s with pec server %s already exists")
                    % (channel.name, channel.fetch_pec_server_id.name)
                )

    @api.constrains("pec_server_id")
    def check_pec_server_id(self):
        pec_channels = self.filtered(lambda c: c.channel_type == 'pec')
        for channel in pec_channels:
            domain = [
                ("pec_server_id", "=", channel.pec_server_id.id),
                ("id", 'in', pec_channels.ids),
            ]
            elements = self.search(domain)
            if len(elements) > 1:
                raise exceptions.ValidationError(
                    _("The channel %s with pec server %s already exists")
                    % (channel.name, channel.pec_server_id.name)
                )

    @api.constrains("email_exchange_system")
    def check_email_validity(self):
        if self.env.context.get("skip_check_email_validity"):
            return
        pec_channels = self.filtered(lambda c: c.channel_type == 'pec')
        for channel in pec_channels:
            if not extract_rfc2822_addresses(channel.email_exchange_system):
                raise exceptions.ValidationError(
                    _("Email %s is not valid") % channel.email_exchange_system
                )

    def check_first_pec_sending(self):
        if not self.first_invoice_sent:
            sdi_address = self.env["ir.config_parameter"].get_param(
                "sdi.pec.first.address",
            )
            self.email_exchange_system = sdi_address
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

    @api.model
    def _check_fetchmail(self):
        server = self.env['fetchmail.server'].search([
            ('is_fatturapa_pec', '=', True),
            ('state', '=', 'done')
        ])
        if not server:
            raise UserError(_(
                "No incoming PEC server found. Please configure it."))

    @api.multi
    def send_via_pec(self, attachment_out_ids):
        self._check_fetchmail()
        self.check_first_pec_sending()
        user = self.env.user
        company = user.company_id
        for att in attachment_out_ids:
            if not att.datas or not att.datas_fname:
                raise UserError(_("File content and file name are mandatory"))
            mail_message = self.env['mail.message'].create({
                'model': att._name,
                'res_id': att.id,
                'subject': att.name,
                'body': 'XML file for FatturaPA {} sent to Exchange System to '
                        'the email address {}.'
                .format(
                    att.name,
                    company.email_exchange_system),
                'attachment_ids': [(6, 0, att.ir_attachment_id.ids)],
                'email_from': (
                    company.email_from_for_fatturaPA),
                'reply_to': (
                    company.email_from_for_fatturaPA),
                'mail_server_id': company.sdi_channel_id.
                pec_server_id.id,
            })

            mail = self.env['mail.mail'].create({
                'mail_message_id': mail_message.id,
                'body_html': mail_message.body,
                'email_to': company.email_exchange_system,
                'headers': {
                    'Return-Path':
                    company.email_from_for_fatturaPA
                }
            })

            if mail:
                try:
                    mail.send(raise_exception=True)
                    att.state = 'sent'
                    att.sending_date = fields.Datetime.now()
                    att.sending_user = user.id
                    company.sdi_channel_id.\
                        update_after_first_pec_sending()
                except MailDeliveryException as e:
                    att.state = 'sender_error'
                    mail.body = str(e)
