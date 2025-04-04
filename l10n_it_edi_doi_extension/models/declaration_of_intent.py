from odoo import api, fields, models


class L10nItDeclarationOfIntent(models.Model):
    _inherit = "l10n_it_edi_doi.declaration_of_intent"

    purchase_order_ids = fields.One2many(
        "purchase.order",
        "l10n_it_edi_doi_id",
        string="Purchase / Rfq Orders",
        copy=False,
        readonly=True,
    )

    type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        required=True,
        default="out",
    )

    def _fetch_valid_declaration_of_intent(
        self, company, partner, currency, date, doi_type="out"
    ):
        domain = [
            ("state", "=", "active"),
            ("company_id", "=", company.id),
            ("currency_id", "=", currency.id),
            ("partner_id", "=", partner.commercial_partner_id.id),
            ("start_date", "<=", date),
            ("end_date", ">=", date),
            ("remaining", ">", 0),
        ]
        if doi_type:
            domain.append(("type", "=", doi_type))

        return self.search(domain, limit=1)

    @api.depends(
        "purchase_order_ids",
        "purchase_order_ids.state",
        "purchase_order_ids.l10n_it_edi_doi_not_yet_invoiced",
    )
    def _compute_not_yet_invoiced(self):
        if self.type == "out":
            return super()._compute_not_yet_invoiced()
        for declaration in self:
            relevant_orders = declaration.purchase_order_ids.filtered(
                lambda order: order.state == "purchase"
            )
            declaration.not_yet_invoiced = sum(
                relevant_orders.mapped("l10n_it_edi_doi_not_yet_invoiced")
            )
