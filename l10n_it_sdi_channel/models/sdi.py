# Copyright 2018 Sergio Corato (https://efatto.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SdiChannel(models.Model):
    _name = "sdi.channel"
    _description = "ES channel"

    name = fields.Char(required=True, translate=True)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    channel_type = fields.Selection(
        string="ES channel type",
        selection=[],
        required=True,
        help="Channels (Pec, Web, Sftp) could be provided by external modules.",
    )

    def send(self, attachment_out_ids):
        """
        Send `attachment_out_ids` to SdI.

        Each channel will define a method send_via_<channel_type>.

        The method will receive a recordset of
        Electronic Invoice (`fatturapa.attachment.out`)
        that have to be sent to SdI.

        The method will take care of updating the state
        of each Electronic Invoice that has managed to send.
        """
        self.ensure_one()
        channel_type = self.channel_type
        send_method_name = "send_via_" + channel_type
        send_method = getattr(self, send_method_name)
        return send_method(attachment_out_ids)
