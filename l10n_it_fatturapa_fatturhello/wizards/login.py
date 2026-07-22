# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class Login(models.TransientModel):
    _name = "l10n_it_fatturapa_fatturhello.login"
    _description = "Login to Fatturhello"

    channel_id = fields.Many2one(
        comodel_name="sdi.channel",
        default=lambda model: model.env.context.get("active_id"),
        domain=[
            ("channel_type", "=", "fatturhello"),
        ],
        required=True,
    )
    username = fields.Char(
        required=True,
        compute="_compute_username",
        store=True,
        readonly=False,
    )
    password = fields.Char(
        required=True,
    )

    @api.depends(
        "channel_id",
    )
    def _compute_username(self):
        for login_wiz in self:
            login_wiz.username = login_wiz.channel_id.fatturhello_username

    def _check_channel_config(self, channel):
        """Ensure that `channel` is ready for login to fatturhello."""
        if channel.channel_type != "fatturhello":
            raise exceptions.UserError(_("You can only login to Fatturhello channels"))
        if not channel.fatturhello_base_url:
            raise exceptions.UserError(_("Configure the base URL in order to login"))
        return True

    @api.onchange("channel_id")
    def onchange_channel(self):
        """Check channel configuration."""
        self.ensure_one()
        if channel := self.channel_id:
            self._check_channel_config(channel)
        else:
            raise exceptions.UserError(_("Please select a channel to login to"))

    def confirm(self):
        """Login and save the returned token in `channel_id`."""
        self.ensure_one()
        credentials = self.env["l10n_it_fatturapa_fatturhello.connector"].get_secrets(
            self.channel_id.fatturhello_base_url,
            self.channel_id.company_id,
            self.username,
            self.password,
        )
        credentials["username"] = self.username
        self.channel_id._fatturhello_update_credentials(credentials)
        # Remove the password from the DB
        self.password = ""
        return True
