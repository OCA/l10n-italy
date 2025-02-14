# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    l10n_edi_it_eori_code = fields.Char(string="EORI Code")
    l10n_edi_it_electronic_invoice_no_contact_update = fields.Boolean(
        string="Do not update the contact from Electronic Invoice Details"
    )
    l10n_edi_it_register = fields.Char(string="Professional Register")
    l10n_edi_it_register_province_id = fields.Many2one(
        "res.country.state", string="Register Province"
    )
    l10n_edi_it_register_code = fields.Char(string="Register Registration Number")
    l10n_edi_it_register_regdate = fields.Date(string="Register Registration Date")
