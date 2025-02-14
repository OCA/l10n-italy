# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompanyInherit(models.Model):
    _inherit = "res.company"

    l10n_edi_it_art73 = fields.Boolean(
        string="Art. 73",
        help="Indicates whether the document has been issued according to "
        "methods and terms laid down in a ministerial decree under "
        "the terms of Article 73 of Italian Presidential Decree "
        "633/72 (this enables the company to issue in the same "
        "year several documents with same number)",
    )
    l10n_edi_it_admin_ref = fields.Char(string="Public Administration Reference Code")
    l10n_edi_it_sender_partner = fields.Many2one(
        "res.partner",
        string="Third Party/Sender",
        help="Data of Third-Party Issuer Intermediary who emits the "
        "invoice on behalf of the seller/provider",
    )
    l10n_edi_it_stable_organization = fields.Many2one(
        "res.partner",
        string="Stable Organization",
        help="The fields must be entered only when the seller/provider is "
        "non-resident, with a stable organization in Italy",
    )
