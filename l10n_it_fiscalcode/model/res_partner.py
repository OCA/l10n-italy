# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from codicefiscale import isvalid

from odoo import _, models, fields, api
from odoo.exceptions import ValidationError


def _check_person_fiscal_code(fiscal_code):
    """`fiscal_code` is the Fiscal Code of a Person."""
    if len(fiscal_code) != 16:
        # Check fiscalcode length of a person
        msg = _("The fiscal code must have 16 characters.")
        raise ValidationError(msg)
    if not isvalid(fiscal_code):
        # Check fiscalcode validity
        msg = _("The fiscal code isn't valid.")
        raise ValidationError(msg)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.constrains('fiscalcode')
    def check_fiscalcode(self):
        for partner in self:
            fiscal_code = partner.fiscalcode
            if not fiscal_code:
                # Because it is not mandatory
                continue
            elif partner.company_type == 'person':
                # Person case
                if partner.company_name:
                    # In E-commerce, if there is company_name,
                    # the user might insert VAT in fiscalcode field.
                    # Perform the same check as Company case
                    continue
                _check_person_fiscal_code(fiscal_code)
        return True

    fiscalcode = fields.Char(
        'Fiscal Code', size=16, help="Italian Fiscal Code")

    @api.onchange('fiscalcode')
    def _fiscalcode_changed(self):
        if self.fiscalcode:
            self.fiscalcode = self.fiscalcode.upper()
