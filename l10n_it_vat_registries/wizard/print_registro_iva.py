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
        required=True,
    )
    journal_ids = fields.Many2many(
        "account.journal",
        "wizard_vat_registries_journals_rel",
        "wizard_id",
        "journal_id",
        string="Journals",
        help="Select journals you want retrieve documents from",
    )
    include_rc_moves = fields.Boolean(
        string="Include reverse charge moves",
    )
    rc_journal_ids = fields.Many2many(
        "account.journal",
        "wizard_vat_registries_rc_journals_rel",
        "wizard_id",
        "journal_id",
        string="Reverse charge journals",
        help="Select journals you want retrieve reverse charge documents from",
    )
    message = fields.Char(size=64, readonly=True)
    only_totals = fields.Boolean(string="Prints only totals")
    fiscal_page_base = fields.Integer("Last printed page", required=True)
    year_footer = fields.Char(
        string="Year for Footer", help="Value printed near number of page in the footer"
    )
    enable_currency = fields.Boolean(
        string="Enable currency values", help="Enable currency values in the report"
    )

    @api.onchange("tax_registry_id")
    def on_change_tax_registry_id(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.layout_type = self.tax_registry_id.layout_type
        self.entry_order = self.tax_registry_id.entry_order
        self.show_full_contact_addess = self.tax_registry_id.show_full_contact_addess
        self.include_rc_moves = self.tax_registry_id.include_rc_moves
        self.rc_journal_ids = self.tax_registry_id.rc_journal_ids

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

    def _include_rc_journals(self):
        if (
            self.include_rc_moves
            and self.rc_journal_ids
            and self.layout_type == "customer"
        ):
            return True
        return False

    def _get_move_ids(self, wizard):
        MAPPING = {
            "journal_date_name": "journal_id, date, name",
            "date_name": "date, name",
        }
        order = MAPPING[wizard.entry_order]
        moves = self.env["account.move"].search(
            self._get_move_ids_domain(),
            order=order,
        )
        if wizard._include_rc_journals():
            LAMBDA_MAPPING = {
                "journal_date_name": lambda m: (m.journal_id, m.date, m.name),
                "date_name": lambda m: (m.date, m.name),
            }
            order = LAMBDA_MAPPING[wizard.entry_order]
            rc_moves = (
                self.env["account.move"]
                .search(
                    [
                        ("date", ">=", wizard.from_date),
                        ("date", "<=", wizard.to_date),
                        ("journal_id", "in", [j.id for j in wizard.rc_journal_ids]),
                        ("state", "=", "posted"),
                    ]
                )
                .filtered(lambda m: m.l10n_it_edi_is_self_invoice)
            )
            moves |= rc_moves
            moves = moves.sorted(order)
        return moves.ids

    def _get_datas_form(self):
        self.ensure_one()
        if not self.journal_ids:
            raise UserError(
                _(
                    "No journals found in the current selection.\n"
                    "Please load them before to retry!"
                )
            )
        datas_form = {}
        datas_form["from_date"] = self.from_date
        datas_form["to_date"] = self.to_date
        datas_form["journal_ids"] = [j.id for j in self.journal_ids]
        if self._include_rc_journals():
            datas_form["rc_journal_ids"] = [j.id for j in self.rc_journal_ids]
        datas_form["fiscal_page_base"] = self.fiscal_page_base
        datas_form["registry_type"] = self.layout_type
        datas_form["year_footer"] = self.year_footer
        datas_form["enable_currency"] = self.enable_currency

        lang_code = self.env.company.partner_id.lang
        lang = self.env["res.lang"]
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        datas_form["date_format"] = date_format

        if self.tax_registry_id:
            datas_form["tax_registry_name"] = self.tax_registry_id.name
        else:
            datas_form["tax_registry_name"] = ""
        datas_form["only_totals"] = self.only_totals
        datas_form["entry_order"] = self.entry_order
        datas_form["show_full_contact_addess"] = self.show_full_contact_addess
        return datas_form

    def print_registro(self):
        move_ids = self._get_move_ids(self)
        datas_form = self._get_datas_form()

        report_name = "l10n_it_vat_registries.action_report_registro_iva"
        datas = {"ids": move_ids, "model": "account.move", "form": datas_form}
        return self.env.ref(report_name).report_action(self, data=datas)

    def print_registro_xlsx(self):
        move_ids = self._get_move_ids(self)
        datas_form = self._get_datas_form()
        report_name = "l10n_it_vat_registries.action_report_registro_iva_xlsx"
        datas = {"ids": move_ids, "model": "account.move", "form": datas_form}
        moves = self.env["account.move"].browse(move_ids)
        return self.env.ref(report_name).report_action(moves, data=datas)
