# Copyright 2019 Roberto Fichera <roberto.fichera@levelprime.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    max_invoice_in_xml = fields.Integer(
        string="Max Invoice # in XML",
        default=lambda self: self.env.company.max_invoice_in_xml,
        help="Maximum number of invoices to group in a single " "XML file. 0=Unlimited",
    )

    @api.constrains("max_invoice_in_xml")
    def _validate_max_invoice_in_xml(self):
        if self.max_invoice_in_xml < 0:
            raise ValidationError(
                _("The max number of invoice to group can't be negative")
            )
