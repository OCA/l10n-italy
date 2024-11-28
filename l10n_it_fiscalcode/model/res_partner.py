# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.constrains(
        "fiscalcode",
        "company_type",
    )
    def check_fiscalcode(self):
        for partner in self:
            if not partner.fiscalcode:
                # Because it is not mandatory
                continue
            elif partner.company_type == "person":
                # Person case
                if partner.company_name:
                    # In E-commerce, if there is company_name,
                    # the user might insert VAT in fiscalcode field.
                    # Perform the same check as Company case
                    continue
                if len(partner.fiscalcode) != 16:
                    # Check fiscalcode length of a person
                    msg = _("The fiscal code must have 16 characters.")
                    raise ValidationError(msg)
                if not isvalid(partner.fiscalcode):
                    # Check fiscalcode validity
                    msg = _("The fiscal code isn't valid.")
                    raise ValidationError(msg)
        return True

    fiscalcode = fields.Char("Fiscal Code", size=16, help="Italian Fiscal Code")

    @api.onchange("fiscalcode")
    def _fiscalcode_changed(self):
        if self.fiscalcode:
            self.fiscalcode = self.fiscalcode.upper()

    @api.model
    def _l10n_it_fiscalcode_build_uniqueness_constraint_error(self, error_dict):
        """Create the error message for uniqueness constraint."""
        error_message_list = [
            _("Multiple partners have the same fiscal code, please correct them.\n"),
        ]
        for fiscal_code, partners in error_dict.items():
            error_message_list.append(
                _(
                    "%(fiscal_code)s: %(partners)s",
                    fiscal_code=fiscal_code,
                    partners=", ".join(partners.mapped("name")),
                )
            )
        return "\n".join(error_message_list)

    @api.constrains(
        "fiscalcode",
    )
    def _l10n_it_fiscalcode_constrain_uniqueness(self):
        """
        Partners in the same company must have different fiscal codes.

        This check is only enabled for companies having "Fiscal code is unique".
        """
        companies = self.company_id
        if not companies:
            companies = self.env["res.company"].search([])

        for company in companies.filtered("l10n_it_fiscalcode_check_uniqueness"):
            error_dict = {}
            partner_groups = self.env["res.partner"].read_group(
                [
                    ("company_id", "in", [False, company.id]),
                    ("fiscalcode", "!=", False),
                ],
                [
                    "fiscalcode",
                ],
                [
                    "fiscalcode",
                ],
            )
            for partner_group in partner_groups:
                if partner_group["fiscalcode_count"] > 1:
                    error_partners = self.env["res.partner"].search(
                        partner_group["__domain"]
                    )
                    if self & error_partners:
                        # Only raise an error for partners we are checking
                        error_fiscal_code = partner_group["fiscalcode"]
                        error_dict[error_fiscal_code] = error_partners

            if error_dict:
                error_message = (
                    self._l10n_it_fiscalcode_build_uniqueness_constraint_error(
                        error_dict
                    )
                )
                raise ValidationError(error_message)
