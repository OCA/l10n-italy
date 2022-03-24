# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardRegistroIva(models.TransientModel):
    _name = "wizard.registro.iva"
    _description = "Run VAT registry"

    date_range_id = fields.Many2one("date.range", string="Date range")
    from_date = fields.Date("From date", required=True)
    to_date = fields.Date("To date", required=True)
    layout_type = fields.Selection(
        selection=[
            ("customer", "Customer Invoices"),
            ("supplier", "Supplier Invoices"),
            ("corrispettivi", "Sums due"),
        ],
        string="Layout",
        required=True,
        default="customer",
    )
    tax_registry_id = fields.Many2one(
        comodel_name="account.tax.registry", string="VAT registry"
    )

    journal_ids = fields.Many2many(
        comodel_name="account.journal",
        relation="registro_iva_journals_rel",
        column1="journal_id",
        column2="registro_id",
        string="Journals",
        help="Select journals you want retrieve documents from",
    )

    message = fields.Char(string="Message", size=64, readonly=True)

    only_totals = fields.Boolean(string="Prints only totals")

    fiscal_page_base = fields.Integer(
        required=True,
        string="Last printed page",
    )

    year_footer = fields.Char(
        string="Year for Footer", help="Value printed near number of page in the footer"
    )

    daily_totals = fields.Boolean(string="Print daily totals")

    @api.onchange("tax_registry_id")
    def on_change_tax_registry_id(self):
        self.update(
            {
                "journal_ids": self.tax_registry_id.journal_ids,
                "layout_type": self.tax_registry_id.layout_type,
                "daily_totals": self.tax_registry_id.daily_totals,
            }
        )

    @api.onchange("date_range_id")
    def on_change_date_range_id(self):
        if self.date_range_id:
            self.from_date = self.date_range_id.date_start
            self.to_date = self.date_range_id.date_end

    @api.onchange("from_date")
    def get_year_footer(self):
        if self.from_date:
            self.year_footer = fields.Datetime.from_string(self.from_date).year

    def _get_move_ids(self, wizard):
        moves = self.env["account.move"].search(
            [
                ("date", ">=", self.from_date),
                ("date", "<=", self.to_date),
                ("journal_id", "in", self.journal_ids.ids),
                ("state", "=", "posted"),
            ],
            order="date, name",
        )

        if not moves:
            raise UserError(_("No documents found in the current selection"))

        return moves.ids

    def print_registro(self):
        self.ensure_one()
        wizard = self
        if not wizard.journal_ids:
            raise UserError(
                _(
                    "No journals found in the current selection.\n"
                    "Please load them before to retry!"
                )
            )
        move_ids = self._get_move_ids(wizard)

        datas_form = {}
        datas_form["from_date"] = wizard.from_date
        datas_form["to_date"] = wizard.to_date
        datas_form["journal_ids"] = [j.id for j in wizard.journal_ids]
        datas_form["fiscal_page_base"] = wizard.fiscal_page_base
        datas_form["registry_type"] = wizard.layout_type
        datas_form["year_footer"] = wizard.year_footer

        lang_code = self.env.company.partner_id.lang
        lang = self.env["res.lang"]._lang_get(lang_code)
        date_format = lang.date_format

        if wizard.tax_registry_id:
            tax_registry_name = wizard.tax_registry_id.name
        else:
            tax_registry_name = ""

        report_name = "l10n_it_vat_registries.action_report_registro_iva"

        datas = {
            "ids": move_ids,
            "model": "account.move",
            "form": {
                "daily_totals": wizard.daily_totals,
                "date_format": date_format,
                "from_date": wizard.from_date,
                "fiscal_page_base": wizard.fiscal_page_base,
                "journal_ids": wizard.journal_ids.ids,
                "only_totals": wizard.only_totals,
                "registry_type": wizard.layout_type,
                "tax_registry_name": tax_registry_name,
                "to_date": wizard.to_date,
                "year_footer": wizard.year_footer,
            },
        }

        return self.env.ref(report_name).report_action(self, data=datas)
