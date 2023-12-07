# Copyright 2019 Roberto Fichera <roberto.fichera@levelprime.com>
# Copyright 2022 Marco Colombo <marco.colombo@phi.technology>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_DEFAULT_XML_DIVISA_VALUE = "force_eur"


class ResCompany(models.Model):
    _inherit = "res.company"

    e_invoice_transmitter_id = fields.Many2one(
        "res.partner",
        "E-bill Transmitter",
        help="This partner will be used as transmitter in out invoice.",
        default=lambda self: self.env.company.partner_id.id,
        required=True,
    )

    max_invoice_in_xml = fields.Integer(
        string="Max Invoice # in XML",
        default=0,
        help="Customer default for maximum number of invoices to group "
        "in a single XML file. 0=Unlimited",
    )

    xml_divisa_value = fields.Selection(
        [
            ("keep_orig", "Keep original"),
            ("force_eur", "Force euro"),
        ],
        string="XML Divisa value",
        default=_DEFAULT_XML_DIVISA_VALUE,
    )

    @api.constrains("max_invoice_in_xml")
    def _validate_max_invoice_in_xml(self):
        if self.max_invoice_in_xml < 0:
            raise ValidationError(
                _(
                    "The customer default for max number of invoices to group "
                    "can't be negative"
                )
            )


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    e_invoice_transmitter_id = fields.Many2one(
        related="company_id.e_invoice_transmitter_id", readonly=False
    )
    max_invoice_in_xml = fields.Integer(
        related="company_id.max_invoice_in_xml", readonly=False
    )

    xml_divisa_value = fields.Selection(
        related="company_id.xml_divisa_value", readonly=False
    )

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super().onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.max_invoice_in_xml = company.max_invoice_in_xml or 0
            self.xml_divisa_value = (
                company.xml_divisa_value or _DEFAULT_XML_DIVISA_VALUE
            )
        else:
            self.max_invoice_in_xml = 0
            self.xml_divisa_value = _DEFAULT_XML_DIVISA_VALUE
        return res
