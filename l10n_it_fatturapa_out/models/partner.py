# -*- coding: utf-8 -*-
# Copyright 2019 Roberto Fichera <roberto.fichera@levelprime.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    max_invoice_in_xml = fields.Integer(string='Max Num. Invoice in XML',
        default=0, help="Maximum number of invoices to group in a single "
                        "XML file. Default=0 unlimited")

    @api.constrains('max_invoice_in_xml')
    def _validate_max_invoice_in_xml(self):
        if self.max_invoice_in_xml < 0:
            raise ValidationError(
                _("The max number of invoice to group can't be negative"))
