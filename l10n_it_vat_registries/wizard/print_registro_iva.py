# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import warnings

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardRegistroIva(models.TransientModel):
    _name = "wizard.registro.iva"
    _description = "Run VAT registry"

    date_range_id = fields.Many2one("date.range", string="Date range")
    from_date = fields.Date("From date", required=True)
    to_date = fields.Date("To date", required=True)
    layout_type = fields.Selection(
        [
            ("customer", "Customer Invoices"),
            ("supplier", "Supplier Invoices"),
            ("corrispettivi", "Sums due"),
        ],
        "Layout",
        required=True,
        default="customer",
    )
    show_full_contact_addess = fields.Boolean()
    tax_registry_id = fields.Many2one("account.tax.registry", "VAT registry")
    entry_order = fields.Selection(
        [
            ("date_name", "Date - Number"),
            ("journal_date_name", "Journal - Date - Number"),
        ],
        default="date_name",
    )
    journal_ids = fields.Many2many(
        "account.journal",
        "registro_iva_journals_rel",
        "journal_id",
        "registro_id",
        string="Journals",
        help="Select journals you want retrieve documents from",
    )
    message = fields.Char(size=64, readonly=True)
    only_totals = fields.Boolean(string="Prints only totals")
    fiscal_page_base = fields.Integer("Last printed page", required=True)
    year_footer = fields.Char(
        string="Year for Footer", help="Value printed near number of page in the footer"
    )

    @api.onchange("tax_registry_id")
    def on_change_tax_registry_id(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.layout_type = self.tax_registry_id.layout_type
        self.entry_order = self.tax_registry_id.entry_order
        self.show_full_contact_addess = self.tax_registry_id.show_full_contact_addess

    @api.onchange("date_range_id")
    def on_change_date_range_id(self):
        if self.date_range_id:
            self.from_date = self.date_range_id.date_start
            self.to_date = self.date_range_id.date_end

    @api.onchange("from_date")
    def get_year_footer(self):
        if self.from_date:
            self.year_footer = self.from_date.year

    def _get_move_ids_domain(self):
        return [
            ("date", ">=", self.from_date),
            ("date", "<=", self.to_date),
            ("journal_id", "in", [j.id for j in self.journal_ids]),
            ("state", "=", "posted"),
        ]

    def _get_move_ids(self, wizard):
        if wizard:
            warnings.warn(
                "`wizard` parameter will be removed because is the same as `self`.",
                DeprecationWarning,
                stacklevel=2,
            )

        MAPPING = {
            "journal_date_name": "journal_id, date, name",
            "date_name": "date, name",
        }
        order = MAPPING[self.entry_order]
        moves = self.env["account.move"].search(
            self._get_move_ids_domain(),
            order=order,
        )
        return moves.ids

    def _get_registro_data(self):
        self.ensure_one()
        if not self.journal_ids:
            raise UserError(
                _(
                    "No journals found in the current selection.\n"
                    "Please load them before to retry!"
                )
            )

        lang_code = self.env.company.partner_id.lang
        lang = self.env["res.lang"]._lang_get(lang_code)
        datas_form = {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "journal_ids": self.journal_ids.ids,
            "fiscal_page_base": self.fiscal_page_base,
            "registry_type": self.layout_type,
            "year_footer": self.year_footer,
            "date_format": lang.date_format,
            "only_totals": self.only_totals,
            "entry_order": self.entry_order,
            "show_full_contact_addess": self.show_full_contact_addess,
        }
        if self.tax_registry_id:
            datas_form["tax_registry_name"] = self.tax_registry_id.name
        else:
            datas_form["tax_registry_name"] = ""
        return {
            "ids": self._get_move_ids(self.browse()),
            "model": "account.move",
            "form": datas_form,
        }

    def print_registro(self):
        self.ensure_one()
        datas = self._get_registro_data()
        report_name = "l10n_it_vat_registries.action_report_registro_iva"
        return self.env.ref(report_name).report_action(self, data=datas)
