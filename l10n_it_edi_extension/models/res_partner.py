# Copyright 2024 Simone Rubino - Aion Tech
# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


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
    l10n_it_edi_import_detail_level = fields.Selection(
        selection=[
            ("min", "Minimum"),
            ("tax", "Tax rate"),
            ("max", "Maximum"),
        ],
        string="E-bills import detail level",
        help="Override the 'E-bills import detail level' of the company "
        "for bills of this supplier.\n"
        "Minimum: the bill is created with no lines; "
        "the user will have to create them, according to what specified in "
        "the electronic bill.\n"
        "Tax rate: every tax rate present in the electronic bill "
        "will create a line in the bill.\n"
        "Maximum: every line contained in the electronic bill "
        "will create a line in the bill.",
    )

    @api.constrains(
        "l10n_it_codice_fiscale",
        "company_type",
    )
    def validate_codice_fiscale(self):
        res = super().validate_codice_fiscale()
        for partner in self:
            if not partner.l10n_it_codice_fiscale:
                # Because it is not mandatory
                continue
            elif partner.company_type == "person":
                # Person case
                if partner.company_name:
                    # In E-commerce, if there is company_name,
                    # the user might insert VAT in l10n_it_codice_fiscale field.
                    # Perform the same check as Company case
                    continue
                if len(partner.l10n_it_codice_fiscale) != 16:
                    # Check l10n_it_codice_fiscale length of a person
                    msg = self.env._(
                        "The fiscal code '%s' must have 16 characters.",
                        partner.l10n_it_codice_fiscale,
                    )
                    raise ValidationError(msg)
        return res
