# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class Login(models.TransientModel):
    _name = "l10n_it_edi_fatturhello.login"
    _description = "Login to Fatturhello"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda model: model.env.company,
        domain=[
            ("fatturhello_is_used", "=", True),
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
        "company_id",
    )
    def _compute_username(self):
        for login_wiz in self:
            login_wiz.username = login_wiz.company_id.fatturhello_username

    def _check_company_config(self, company):
        """Ensure that `company` is ready for login to fatturhello."""
        if not company.fatturhello_is_used:
            raise exceptions.UserError(_("You can only login to Fatturhello companies"))
        if not company.fatturhello_base_url:
            raise exceptions.UserError(_("Configure the base URL in order to login"))
        return True

    @api.onchange("company_id")
    def onchange_company(self):
        """Check company configuration."""
        self.ensure_one()
        if company := self.company_id:
            self._check_company_config(company)
        else:
            raise exceptions.UserError(_("Please select a company to login to"))

    def confirm(self):
        """Login and save the returned token in `company_id`."""
        self.ensure_one()
        credentials = self.env["l10n_it_edi_fatturhello.connector"].get_secrets(
            self.company_id.fatturhello_base_url,
            self.company_id,
            self.username,
            self.password,
        )
        credentials["username"] = self.username
        self.company_id._fatturhello_update_credentials(credentials)
        # Remove the password from the DB
        self.password = ""
        return True
