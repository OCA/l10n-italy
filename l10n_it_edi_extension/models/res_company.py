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
    l10n_edi_it_stable_organization = fields.Many2one(
        "res.partner",
        string="Stable Organization",
        help="The fields must be entered only when the seller/provider is "
        "non-resident, with a stable organization in Italy",
    )
    l10n_edi_it_create_partner = fields.Boolean(
        string="Create Partner on Eletronic Invoice import",
        help="Automatically create the partner if it does not "
        "exist during the import of Electronic Invoices.",
    )
    l10n_it_edi_import_detail_level = fields.Selection(
        selection=[
            ("min", "Minimum"),
            ("tax", "Tax rate"),
            ("max", "Maximum"),
        ],
        default="max",
        required=True,
        string="E-bills import detail level",
        help="Minimum: the bill is created with no lines; "
        "the user will have to create them, according to what specified in "
        "the electronic bill.\n"
        "Tax rate: every tax rate present in the electronic bill "
        "will create a line in the bill.\n"
        "Maximum (default): every line contained in the electronic bill "
        "will create a line in the bill.",
    )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_edi_it_create_partner = fields.Boolean(
        related="company_id.l10n_edi_it_create_partner",
        string="Create Partner on Eletronic Invoice import",
        help="Automatically create the partner if it does not "
        "exist during the import of Electronic Invoices.",
        readonly=False,
    )
    l10n_it_edi_import_detail_level = fields.Selection(
        related="company_id.l10n_it_edi_import_detail_level",
        readonly=False,
    )
