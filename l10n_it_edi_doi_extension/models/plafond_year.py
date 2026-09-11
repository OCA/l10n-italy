from odoo import api, exceptions, fields, models


class L10nItEdiDoiPlafondYear(models.Model):
    _name = "l10n_it_edi_doi_extension.plafond.year"
    _description = "Annual Plafond for Declarations of Intent"
    _order = "year desc, company_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        compute="_compute_name",
        store=True,
    )

    year = fields.Integer(
        string="Year (stored)",
        required=True,
        default=lambda self: fields.Date.today().year,
        tracking=True,
    )

    year_display = fields.Char(
        string="Year",
        compute="_compute_year_display",
        inverse="_inverse_year_display",
        store=False,
        help="Year in YYYY format (e.g., 2025)",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
        store=True,
    )

    plafond_total = fields.Monetary(
        string="Total Plafond (AdE)",
        required=True,
        tracking=True,
        help="Total amount assigned by Agenzia delle Entrate for this year",
    )

    plafond_assigned = fields.Monetary(
        string="Total Assigned",
        compute="_compute_plafond_usage",
        store=True,
        help="Sum of thresholds assigned to DOIs with specific threshold",
    )

    plafond_used = fields.Monetary(
        string="Total Used",
        compute="_compute_plafond_usage",
        store=True,
        help="Sum of invoiced amounts from all DOIs linked to this plafond",
    )

    plafond_available = fields.Monetary(
        string="Available",
        compute="_compute_plafond_usage",
        store=True,
        help="Total plafond minus used amount",
    )

    usage_percentage = fields.Float(
        string="Usage %",
        compute="_compute_plafond_usage",
        store=True,
    )

    declaration_ids = fields.One2many(
        comodel_name="l10n_it_edi_doi.declaration_of_intent",
        inverse_name="plafond_id",
        string="Declarations of Intent",
    )

    # Computed field for all invoices linked to this plafond through DOIs
    invoice_ids = fields.Many2many(
        comodel_name="account.move",
        string="Purchase Invoices",
        compute="_compute_invoice_ids",
        store=False,
    )

    invoice_count = fields.Integer(
        compute="_compute_invoice_ids",
        store=False,
    )

    active = fields.Boolean(
        default=True,
    )

    note = fields.Text(
        string="Notes",
    )

    _sql_constraints = [
        (
            "year_company_unique",
            "unique(year, company_id)",
            "A plafond already exists for this year and company!",
        ),
        (
            "plafond_total_positive",
            "CHECK(plafond_total > 0)",
            "The total plafond must be greater than zero!",
        ),
    ]

    def _compute_invoice_ids(self):
        """Compute all purchase invoices linked to this plafond through DOIs."""
        for plafond in self:
            # Get all invoices from all DOIs linked to this plafond
            invoices = plafond.declaration_ids.mapped("invoice_ids").filtered(
                lambda inv: inv.move_type in ("in_invoice", "in_refund")
            )
            plafond.invoice_ids = invoices
            plafond.invoice_count = len(invoices)

    @api.depends("year")
    def _compute_year_display(self):
        """Convert integer year to string for display."""
        for plafond in self:
            plafond.year_display = str(plafond.year) if plafond.year else ""

    def _inverse_year_display(self):
        """Convert string year to integer for storage."""
        for plafond in self:
            if plafond.year_display:
                try:
                    year_int = int(plafond.year_display)
                    if 2000 <= year_int <= 2100:
                        plafond.year = year_int
                    else:
                        raise exceptions.ValidationError(
                            plafond.env._("Year must be between 2000 and 2100.")
                        )
                except ValueError as ve:
                    raise exceptions.ValidationError(
                        plafond.env._("Year must be a 4-digit number (e.g., 2025).")
                    ) from ve

    @api.depends("year", "company_id")
    def _compute_name(self):
        for plafond in self:
            company_name = plafond.company_id.name or ""
            plafond.name = plafond.env._(
                "Plafond %(year)s - %(company)s",
                year=plafond.year,
                company=company_name,
            )

    @api.depends(
        "plafond_total",
        "declaration_ids.threshold",
        "declaration_ids.invoiced",
        "declaration_ids.state",
        "declaration_ids.type",
    )
    def _compute_plafond_usage(self):
        for plafond in self:
            # Only consider DOIs of type "in" (issued from company)
            # that are not cancelled
            active_dois = plafond.declaration_ids.filtered(
                lambda d: d.state not in ["revoked", "terminated"] and d.type == "in"
            )

            # Sum of thresholds for DOIs with specific threshold
            plafond.plafond_assigned = sum(
                active_dois.filtered(lambda d: d.threshold > 0).mapped("threshold")
            )

            # Sum of all invoiced amounts
            plafond.plafond_used = sum(active_dois.mapped("invoiced"))

            # Available = Total - Used
            plafond.plafond_available = plafond.plafond_total - plafond.plafond_used

            # Usage percentage
            if plafond.plafond_total > 0:
                plafond.usage_percentage = (
                    plafond.plafond_used / plafond.plafond_total
                ) * 100
            else:
                plafond.usage_percentage = 0.0

    @api.constrains("plafond_total", "declaration_ids")
    def _check_plafond_not_exceeded(self):
        """Check that assigned thresholds don't exceed total plafond."""
        for plafond in self:
            if plafond.plafond_assigned > plafond.plafond_total:
                raise exceptions.ValidationError(
                    plafond.env._(
                        "The sum of assigned thresholds (%(assigned)s) exceeds "
                        "the total plafond (%(total)s)!",
                        assigned=plafond.plafond_assigned,
                        total=plafond.plafond_total,
                    )
                )

    def action_open_declarations(self):
        """Open declarations linked to this plafond."""
        self.ensure_one()
        return {
            "name": self.env._("Declarations of Intent - %s", self.name),
            "type": "ir.actions.act_window",
            "res_model": "l10n_it_edi_doi.declaration_of_intent",
            "domain": [("plafond_id", "=", self.id)],
            "views": [(False, "list"), (False, "form")],
            "context": {
                "default_plafond_id": self.id,
                "default_type": "in",
            },
        }

    def action_open_invoices(self):
        """Open all purchase invoices linked to this plafond through DOIs."""
        self.ensure_one()
        return {
            "name": self.env._("Purchase Invoices - %s", self.name),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [("id", "in", self.invoice_ids.ids)],
            "views": [(False, "list"), (False, "form")],
            "context": {
                "default_move_type": "in_invoice",
                "search_default_posted": 1,
            },
        }
