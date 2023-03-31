from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    e_invoice_user_id = fields.Many2one(
        "res.users",
        "E-bill creator",
        help="This user will be used at supplier e-bill creation.",
        default=lambda self: self.env.user.id,
    )
    email_from_for_fatturaPA = fields.Char(
        string="Sender Email Address",
        related="sdi_channel_id.pec_server_id.email_from_for_fatturaPA",
        readonly=True,
    )
    email_exchange_system = fields.Char(
        string="Exchange System Email Address",
        related="sdi_channel_id.email_exchange_system",
        readonly=True,
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    e_invoice_user_id = fields.Many2one(
        related="company_id.e_invoice_user_id",
        readonly=False,
    )
    email_from_for_fatturaPA = fields.Char(
        string="Sender Email Address",
        related="company_id.sdi_channel_id.pec_server_id.email_from_for_fatturaPA",
        readonly=True,
    )
    email_exchange_system = fields.Char(
        string="Exchange System Email Address",
        related="company_id.sdi_channel_id.email_exchange_system",
        readonly=True,
    )
