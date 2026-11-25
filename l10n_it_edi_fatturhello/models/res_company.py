# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    fatturhello_identifier = fields.Char(
        readonly=True,
        help="Identifier of this company in Fatturhello, "
        "set automatically during login.",
    )
    fatturhello_last_downloaded_e_bill_identifer = fields.Char(
        help="Fatturhello's protocol number of the last E-Bill downloaded.\n"
        "All the E-Bills subsequent this one will be downloaded "
        "during the CRON execution.\n"
        "If empty, all the E-Bills in Fatturhello will be downloaded.",
    )
    fatturhello_is_used = fields.Boolean(
        string="Use Fatturhello",
    )
    fatturhello_base_url = fields.Char(
        name="Fatturhello base URL",
        default="https://app.b2beasy.it",
    )
    fatturhello_username = fields.Char(
        readonly=True,
        help="Username can only be set during login.",
    )
    fatturhello_login_authtoken = fields.Char(
        readonly=True,
        help="Token can only be set during login. Login again to update the token.",
    )
    fatturhello_login_authtoken_create_date = fields.Date(
        readonly=True,
    )

    def fatturhello_action_login(self):
        """Action to open the login wizard."""
        login_wizard = self.env["l10n_it_edi_fatturhello.login"].with_context(
            active_id=self.id,
        )
        login_action = login_wizard.get_formview_action()
        login_action.update(
            {
                "name": "Login",
                "target": "new",
            }
        )
        return login_action

    def _fatturhello_update_credentials(self, credentials):
        """Store the credentials for authenticating API calls."""
        self.ensure_one()
        self.update(
            {
                "fatturhello_username": credentials["username"],
                "fatturhello_login_authtoken": credentials["authtoken"],
                "fatturhello_login_authtoken_create_date": fields.Date.today(),
            }
        )
        self.fatturhello_identifier = credentials["company_identifier"]
        return True
