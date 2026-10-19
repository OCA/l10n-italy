# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


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
        "registro_iva_journals_rel",
        "journal_id",
        "registro_id",
        string="Journals",
        help="Select journals you want retrieve documents from",
    )
    message = fields.Char(string="Message", size=64, readonly=True)
    only_totals = fields.Boolean(string="Prints only totals")
    fiscal_page_base = fields.Integer("Last printed page", required=True)
    year_footer = fields.Char(
        string="Year for Footer", help="Value printed near number of page in the footer"
    )
    enable_currency = fields.Boolean(
        string="Enable currency values", help="Enable currency values in the report"
    )
    holes_in_registry = fields.Text(
        compute="_compute_holes_in_registry",
        string="Holes in registry",
    )
    multiple_taxes = fields.Text(
        compute="_compute_multiple_taxes",
        string="Multiple taxes",
    )

    def _compute_multiple_taxes(self):
        multiple_taxes = []
        if self.journal_ids and self.from_date and self.to_date:
            moves = self.env["account.move"].search(
                [
                    ("date", ">=", self.from_date),
                    ("date", "<=", self.to_date),
                    ("journal_id", "in", [j._origin.id for j in self.journal_ids]),
                    ("state", "=", "posted"),
                ],
            )
            for move_line in moves.mapped("line_ids"):
                if move_line.tax_ids and len(move_line.tax_ids) != 1:
                    multiple_taxes.append(
                        _("Move line %s of invoice %s has too many base taxes: %s")
                        % (
                            move_line.name,
                            move_line.move_id.name,
                            move_line.tax_ids.mapped("name"),
                        )
                    )
        self.multiple_taxes = "\n".join(multiple_taxes) or _("No multiple taxes found!")

    def _compute_holes_in_registry(self):
        # this method is called from onchange methods
        holes = []
        if self.journal_ids and self.from_date and self.to_date:
            moves = self.env["account.move"].search(
                [
                    ("date", ">=", self.from_date),
                    ("date", "<=", self.to_date),
                    ("journal_id", "in", [j._origin.id for j in self.journal_ids]),
                    ("state", "=", "posted"),
                ],
            )
            # get the previous move for each journal and add to the moves to check
            for journal in self.journal_ids:
                move = self.env["account.move"].search(
                    [
                        ("date", "<", self.from_date),
                        ("journal_id", "=", journal.id),
                        ("state", "=", "posted"),
                    ],
                    order="name desc",
                    limit=1,
                )
                if move:
                    moves |= move
            for journal in moves.mapped("journal_id"):
                hole = journal.check_holes(
                    moves.filtered(lambda m: m.journal_id == journal)
                )
                if hole:
                    holes.append(hole)
        self.holes_in_registry = "\n".join(holes) or _("No holes found!")

    @api.onchange("tax_registry_id")
    def on_change_tax_registry_id(self):
        self.journal_ids = self.tax_registry_id.journal_ids
        self.layout_type = self.tax_registry_id.layout_type
        self.entry_order = self.tax_registry_id.entry_order
        self.show_full_contact_addess = self.tax_registry_id.show_full_contact_addess
        if self.tax_registry_id and self.from_date and self.to_date:
            self._compute_holes_in_registry()
            self._compute_multiple_taxes()

    @api.onchange("date_range_id")
    def on_change_date_range_id(self):
        if self.date_range_id:
            self.from_date = self.date_range_id.date_start
            self.to_date = self.date_range_id.date_end

    @api.onchange("from_date")
    def get_year_footer(self):
        if self.from_date:
            self.year_footer = self.from_date.year
        if self.tax_registry_id and self.from_date and self.to_date:
            self._compute_holes_in_registry()
            self._compute_multiple_taxes()

    @api.onchange("to_date")
    def on_change_to_date(self):
        if self.tax_registry_id and self.from_date and self.to_date:
            self._compute_holes_in_registry()
            self._compute_multiple_taxes()

    def _get_move_ids(self, wizard):
        MAPPING = {
            "journal_date_name": "journal_id, date, name",
            "date_name": "date, name",
        }
        order = MAPPING[wizard.entry_order]
        moves = self.env["account.move"].search(
            [
                ("date", ">=", self.from_date),
                ("date", "<=", self.to_date),
                ("journal_id", "in", [j.id for j in self.journal_ids]),
                ("state", "=", "posted"),
            ],
            order=order,
        )
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
        datas_form["enable_currency"] = wizard.enable_currency

        lang_code = self.env.company.partner_id.lang
        lang = self.env["res.lang"]
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        datas_form["date_format"] = date_format

        if wizard.tax_registry_id:
            datas_form["tax_registry_name"] = wizard.tax_registry_id.name
        else:
            datas_form["tax_registry_name"] = ""
        datas_form["only_totals"] = wizard.only_totals
        datas_form["entry_order"] = wizard.entry_order
        datas_form["show_full_contact_addess"] = wizard.show_full_contact_addess
        # report_name = 'l10n_it_vat_registries.report_registro_iva'
        report_name = "l10n_it_vat_registries.action_report_registro_iva"
        datas = {"ids": move_ids, "model": "account.move", "form": datas_form}
        return self.env.ref(report_name).report_action(self, data=datas)
