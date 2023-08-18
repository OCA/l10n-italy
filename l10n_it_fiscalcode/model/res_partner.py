# Copyright 2023 Simone Rubino - TAKOBI
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


def _check_company_fiscal_code(fiscal_code):
    """`fiscal_code` is the Fiscal Code of a Company."""
    return len(fiscal_code) == 11


def _check_person_fiscal_code(fiscal_code):
    """`fiscal_code` is the Fiscal Code of a Person."""
    return len(fiscal_code) == 16


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains(
        "fiscalcode",
        "company_type",
    )
    def check_fiscalcode(self):
        for partner in self:
            fiscal_code = partner.fiscalcode
            if not fiscal_code:
                # Because it is not mandatory
                continue
            elif partner.company_type == "person":
                # Person case
                if partner.company_name:
                    # In E-commerce, if there is company_name,
                    # the user might insert VAT in fiscalcode field.
                    if not _check_company_fiscal_code(fiscal_code):
                        raise ValidationError(
                            _("The fiscal code must have 11 characters.")
                        )
                elif not _check_person_fiscal_code(fiscal_code):
                    # Check fiscalcode length of a person
                    msg = _("The fiscal code must have 16 characters.")
                    raise ValidationError(msg)
                if not isvalid(partner.fiscalcode):
                    # Check fiscalcode validity
                    msg = _("The fiscal code isn't valid.")
                    raise ValidationError(msg)
            elif partner.company_type == "company":
                if not _check_company_fiscal_code(fiscal_code):
                    raise ValidationError(_("The fiscal code must have 11 characters."))
        return True

    fiscalcode = fields.Char("Fiscal Code", size=16, help="Italian Fiscal Code")

    @api.onchange("fiscalcode")
    def _fiscalcode_changed(self):
        if self.fiscalcode:
            self.fiscalcode = self.fiscalcode.upper()
