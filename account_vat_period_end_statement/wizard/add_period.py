#  Copyright 2012 Domsense s.r.l. (<http://www.domsense.com>).
#  Copyright 2012-15 Agile Business Group sagl (<http://www.agilebg.com>)
#  Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AddPeriod(models.TransientModel):

    _name = "add.period.to.vat.statement"
    _description = "Add period to VAT Statement"

    period_id = fields.Many2one("date.range", "Period", required=True)

    def add_period(self):
        self.ensure_one()
        if "active_id" not in self.env.context:
            raise UserError(_("Current statement not found"))
        statement_env = self.env["account.vat.period.end.statement"]
        wizard = self
        if wizard.period_id.vat_statement_id:
            raise UserError(
                _("Period %s is associated to statement %s yet")
                % (wizard.period_id.name, wizard.period_id.vat_statement_id.date)
            )
        statement_id = self.env.context["active_id"]
        wizard.period_id.vat_statement_id = statement_id
        statement = statement_env.browse(statement_id)
        statement.set_fiscal_year()
        statement.compute_amounts()
        return {
            "type": "ir.actions.act_window_close",
        }
