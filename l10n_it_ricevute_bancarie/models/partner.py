# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    group_riba = fields.Boolean(
        "Group C/O", help="Group C/O by customer while issuing."
    )
    riba_exclude_expenses = fields.Boolean(
        string="Exclude expenses Ri.Ba.",
    )
    riba_policy_expenses = fields.Selection(
        [
            ("one_a_month", "More invoices, one expense per Month"),
            ("unlimited", "One expense per maturity"),
        ],
        default="one_a_month",
        string="Ri.Ba. Policy expenses",
    )
