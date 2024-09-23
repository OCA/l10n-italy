# Copyright 2019 Roberto Fichera <roberto.fichera@levelprime.com>
# Copyright 2023 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    max_invoice_in_xml = fields.Integer(
        string="Max Invoice # in XML",
        default=lambda self: self.env.company.max_invoice_in_xml,
        help="Maximum number of invoices to group in a single "
        "XML file.\n"
        "If this is 0, then the number configured "
        "in the account settings is considered.",
    )

    @api.constrains("max_invoice_in_xml")
    def _validate_max_invoice_in_xml(self):
        for partner in self:
            if partner.max_invoice_in_xml < 0:
                raise ValidationError(
                    _(
                        "The max number of invoice to group "
                        "can't be negative for partner %s",
                        partner.name,
                    )
                )
