# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    fatturhello_identifier = fields.Char(
        related="company_id.fatturhello_identifier",
    )
    fatturhello_last_downloaded_e_bill_identifer = fields.Char(
        related="company_id.fatturhello_last_downloaded_e_bill_identifer",
        readonly=False,
    )
    fatturhello_is_used = fields.Boolean(
        related="company_id.fatturhello_is_used",
        readonly=False,
    )
    fatturhello_base_url = fields.Char(
        related="company_id.fatturhello_base_url",
        readonly=False,
    )
    fatturhello_username = fields.Char(
        related="company_id.fatturhello_username",
    )
    fatturhello_login_authtoken = fields.Char(
        related="company_id.fatturhello_login_authtoken",
    )
    fatturhello_login_authtoken_create_date = fields.Date(
        related="company_id.fatturhello_login_authtoken_create_date",
    )

    def fatturhello_action_login(self):
        """Open the login wizard for the active company."""
        return self.env.company.fatturhello_action_login()
