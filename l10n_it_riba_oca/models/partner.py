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
    riba_exclude_expenses = fields.Boolean(
        string="Exclude expenses Ri.Ba.",
        help="If set, collection fees are never added to the invoices "
        "of this partner.",
    )
    riba_policy_expenses = fields.Selection(
        [
            ("one_a_month", "More invoices, one expense per Month"),
            ("unlimited", "One expense per maturity"),
        ],
        default="one_a_month",
        string="Ri.Ba. Policy expenses",
        help="One expense per month: collection fees are not added for the due "
        "dates falling in a month where the partner already has upcoming RiBa "
        "due dates on invoices with collection fees.\n"
        "One expense per maturity: collection fees are added for every due date.",
    )
