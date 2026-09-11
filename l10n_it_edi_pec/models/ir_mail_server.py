# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# Copyright 2025 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    is_l10n_it_edi_pec = fields.Boolean(string="E-invoice PEC server")
    l10n_it_edi_pec_email_from = fields.Char(
        string="PEC Sender Email Address",
        help="Email address used as sender for e-invoices sent via PEC.",
    )

    def _get_test_email_from(self):
        if self.is_l10n_it_edi_pec and self.l10n_it_edi_pec_email_from:
            return self.l10n_it_edi_pec_email_from
        return super()._get_test_email_from()

    @api.model
    def _find_mail_server(self, email_from, mail_servers=None):
        # Exclude PEC servers from automatic mail server selection
        # so they are not used for regular emails.
        if mail_servers is None:
            mail_servers = self.sudo().search(
                [("is_l10n_it_edi_pec", "=", False)], order="sequence"
            )
        return super()._find_mail_server(email_from, mail_servers=mail_servers)
