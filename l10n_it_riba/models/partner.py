# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    group_riba = fields.Boolean(
        "Group RiBa", help="Group RiBa by customer while issuing."
    )
    is_supplier_payment_riba = fields.Boolean(
        string="Is RiBa Payment",
        related="property_supplier_payment_term_id.riba",
        readonly=True,
    )

    def _domain_property_riba_supplier_company_bank_id(self):
        """Allow to select bank accounts linked to the current company."""
        return self.env["res.partner.bank"]._domain_riba_partner_bank_id()

    property_riba_supplier_company_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        company_dependent=True,
        string="Company Bank Account for Supplier",
        domain=_domain_property_riba_supplier_company_bank_id,
        help="Bank account used for the RiBa of this supplier.",
    )
