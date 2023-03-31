#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IntrastatStatementSaleSection(models.AbstractModel):
    _inherit = "account.intrastat.statement.section"
    _name = "account.intrastat.statement.sale.section"
    _description = "Fields and methods " "common to all Intrastat sale sections"

    @api.model
    def get_section_type(self):
        return "sale"

    @api.model
    def _default_transaction_nature_id(self):
        company_id = self.env.context.get("company_id", self.env.user.company_id)
        return company_id.intrastat_sale_transaction_nature_id
