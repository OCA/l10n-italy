# Copyright 2025 Nextev Srl

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError


class L10nItDeclarationOfIntent(models.Model):
    _inherit = "l10n_it_edi_doi.declaration_of_intent"

    number = fields.Char(
        help="Sequential number for internal reference",
        copy=False,
    )

    purchase_order_ids = fields.One2many(
        "purchase.order",
        "l10n_it_edi_doi_id",
        string="Purchase / Rfq Orders",
        copy=False,
        readonly=True,
    )

    move_doi_ids = fields.One2many(
        "account.move.doi",
        "declaration_id",
        string="Invoice Declaration Lines",
        copy=False,
        readonly=True,
        help="Links to invoices using this declaration with specific amounts.",
    )

    type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        required=True,
        default="out",
    )

    # Link to annual plafond (only for type "in")
    plafond_id = fields.Many2one(
        comodel_name="l10n_it_edi_doi_extension.plafond.year",
        string="Annual Plafond",
        tracking=True,
        domain="[('company_id', '=', company_id)]",
        help="Annual plafond assigned by Agenzia delle Entrate. "
        "Required for issued declarations (type 'in').",
    )

    # Computed field to check if DOI has a specific threshold or uses plafond
    has_threshold = fields.Boolean(
        string="Has Specific Threshold",
        compute="_compute_has_threshold",
        store=True,
        help="If True, this DOI has a specific threshold. "
        "If False, it uses the total plafond without individual limit.",
    )

    # Plafond available (for DOIs without threshold, shows plafond available)
    plafond_available = fields.Monetary(
        compute="_compute_plafond_available",
        store=True,
        help="Available amount from annual plafond "
        "(for DOIs without specific threshold)",
    )

    # Override partner_id to make it optional for type "in"
    partner_id = fields.Many2one(
        required=False,  # Will be enforced by constraint for type "out"
    )

    @api.depends("threshold")
    def _compute_has_threshold(self):
        for doi in self:
            doi.has_threshold = doi.threshold > 0

    @api.depends("plafond_id.plafond_available", "type", "has_threshold")
    def _compute_plafond_available(self):
        for doi in self:
            if doi.type == "in" and doi.plafond_id and not doi.has_threshold:
                doi.plafond_available = doi.plafond_id.plafond_available
            else:
                doi.plafond_available = 0.0

    @api.constrains("type", "partner_id")
    def _check_partner_required_for_out(self):
        """Partner is required for received declarations (type 'out')."""
        for doi in self:
            if doi.type == "out" and not doi.partner_id:
                raise exceptions.ValidationError(
                    doi.env._(
                        "Partner is required for received declarations "
                        "(type 'Received from customers')."
                    )
                )

    @api.constrains("type", "plafond_id")
    def _check_plafond_required_for_in(self):
        """Plafond is required for issued declarations (type 'in')."""
        for doi in self:
            if doi.type == "in" and not doi.plafond_id:
                raise exceptions.ValidationError(
                    doi.env._(
                        "Annual Plafond is required for issued declarations "
                        "(type 'Issued from company')."
                    )
                )

    @api.onchange("type")
    def _onchange_type_clear_plafond(self):
        """Clear plafond when switching to type 'out'."""
        if self.type == "out":
            self.plafond_id = False

    @api.onchange("plafond_id")
    def _onchange_plafond_set_dates(self):
        """Suggest dates based on plafond year."""
        if self.plafond_id and not self.start_date:
            year = self.plafond_id.year
            self.start_date = fields.Date.today().replace(year=year, month=1, day=1)
            self.end_date = fields.Date.today().replace(year=year, month=12, day=31)

    def _fetch_valid_declaration_of_intent(
        self, company, partner, currency, date, doi_type="out"
    ):
        res = super()._fetch_valid_declaration_of_intent(
            company, partner, currency, date
        )
        if not res or res.type == doi_type:
            return res
        # Same domain as in the original, with the addition of 'type'
        domain = [
            ("state", "=", "active"),
            ("company_id", "=", company.id),
            ("currency_id", "=", currency.id),
            ("partner_id", "=", partner.commercial_partner_id.id),
            ("start_date", "<=", date),
            ("end_date", ">=", date),
            ("remaining", ">", 0),
            ("type", "=", doi_type),
        ]
        return self.search(domain, limit=1)

    @api.depends(
        "invoice_ids",
        "invoice_ids.state",
        "invoice_ids.l10n_it_edi_doi_amount",
        "invoice_ids.move_type",
        "move_doi_ids",
        "move_doi_ids.amount",
        "move_doi_ids.move_id.state",
        "move_doi_ids.move_id.move_type",
    )
    def _compute_invoiced(self):
        """Override to use bridge model amounts when available.

        For invoices with bridge records (multiple declarations), use the specific
        amounts from the bridge model. For invoices without bridge records (single
        declaration via l10n_it_edi_doi_id), use the standard l10n_it_edi_doi_amount.

        Refunds (in_refund, out_refund) reduce the invoiced amount.
        """
        for declaration in self:
            total_invoiced = 0

            # Get all posted invoices and draft with name linked through the bridge
            # model
            posted_doi_links = declaration.move_doi_ids.filtered(
                lambda doi: doi.move_id.state == "posted"
                or (doi.move_id.state == "draft" and doi.move_id.name)
            )
            bridge_moves = posted_doi_links.mapped("move_id")

            # Sum amounts from bridge records for multi-declaration invoices
            # Refunds reduce the total (negative contribution)
            for doi_link in posted_doi_links:
                amount = doi_link.amount
                if doi_link.move_id.move_type in ("in_refund", "out_refund"):
                    amount = -amount
                total_invoiced += amount

            # For single-declaration invoices (not using bridge model),
            # use the standard field
            posted_invoices = declaration.invoice_ids.filtered(
                lambda invoice: invoice.state == "posted"
            )
            single_declaration_invoices = posted_invoices - bridge_moves
            for invoice in single_declaration_invoices:
                amount = invoice.l10n_it_edi_doi_amount
                if invoice.move_type in ("in_refund", "out_refund"):
                    amount = -amount
                total_invoiced += amount

            declaration.invoiced = total_invoiced

    @api.depends(
        "purchase_order_ids",
        "purchase_order_ids.state",
        "purchase_order_ids.l10n_it_edi_doi_not_yet_invoiced",
    )
    def _compute_not_yet_invoiced(self):
        received_doi = self.filtered(lambda r: r.type == "out")
        issued_doi = self - received_doi
        super(L10nItDeclarationOfIntent, received_doi)._compute_not_yet_invoiced()
        for declaration in issued_doi:
            relevant_orders = declaration.purchase_order_ids.filtered(
                lambda order: order.state == "purchase"
            )
            declaration.not_yet_invoiced = sum(
                relevant_orders.mapped("l10n_it_edi_doi_not_yet_invoiced")
            )
        return  # W8110

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("number"):
                values["number"] = self.env["ir.sequence"].next_by_code(
                    "l10n_it_edi_doi.declaration_of_intent"
                )
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_linked_to_purchase_document(self):
        if self.purchase_order_ids:
            raise UserError(
                _(
                    "You cannot delete Declarations of Intents that "
                    "are already used on at least one Purchase Order."
                )
            )
