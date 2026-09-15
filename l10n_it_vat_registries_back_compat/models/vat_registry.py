# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ReportRegistroIvaBackCompat(models.AbstractModel):
    """Backward-compatible VAT registry report that uses the same
    tax-computation logic as Odoo 16 modules:

    - l10n_it_vat_registries
    - l10n_it_vat_registries_rc
    - l10n_it_vat_registries_split_payment
    - l10n_it_vat_settlement_date

    It inherits from the v18 report and only overrides the methods
    whose logic differs between v16 and v18.
    """

    _name = "report.l10n_it_vat_registries_back_compat.report_registro_iva"
    _inherit = "report.l10n_it_vat_registries.report_registro_iva"
    _description = "Report VAT registry (v16 backward compatible)"

    # ------------------------------------------------------------------
    # V16-compatible tax computation
    # ------------------------------------------------------------------

    def _tax_amounts_by_tax_id(self, move, move_lines, registry_type):
        """Compute tax amounts per tax ID using **v16 logic**.

        This method cannot call ``super()`` because the v18 implementation
        applies ``continue`` filters inside the loop that **discard** move
        lines (``_l10n_it_filter_kind``, negative split-payment skip,
        self-invoice handling).  Once super() has run, the excluded data
        is gone and cannot be recovered.  V16 included all those lines,
        so we must iterate from scratch.
        """
        res = {}

        for move_line in move_lines:
            if not (move_line.tax_line_id or move_line.tax_ids):
                continue

            if move_line.tax_ids and len(move_line.tax_ids) != 1:
                raise UserError(
                    _("Move line %s has too many base taxes") % move_line.name
                )

            if move_line.tax_ids:
                tax = move_line.tax_ids[0]
                is_base = True
            else:
                tax = move_line.tax_line_id
                is_base = False

            if tax.parent_tax_ids and len(tax.parent_tax_ids) == 1:
                tax = tax.parent_tax_ids[0]

            if tax.exclude_from_registries:
                continue

            if not res.get(tax.id):
                res[tax.id] = {
                    "name": tax.name,
                    "base": 0,
                    "base_currency": 0,
                    "tax": 0,
                    "tax_currency": 0,
                }

            tax_amount = move_line.debit - move_line.credit
            tax_amount_currency = move_line.amount_currency

            if "receivable" in move.financial_type:
                tax_amount = -tax_amount
                tax_amount_currency = -tax_amount_currency

            if is_base:
                res[tax.id]["base"] += tax_amount
                res[tax.id]["base_currency"] += tax_amount_currency
            else:
                res[tax.id]["tax"] += tax_amount
                res[tax.id]["tax_currency"] += tax_amount_currency

            res[tax.id]["currency_symbol"] = move_line.currency_id.symbol

        return res

    # ------------------------------------------------------------------
    # V16-compatible totals computation
    # ------------------------------------------------------------------

    def _compute_totals_tax(self, tax, data):
        """Compute tax totals using **v16 logic**.

        Calls super() to get the v18 9-tuple, then adjusts:
        - Undoes the v18 reverse-charge adjustment for purchase taxes
          in customer registry (v16 did not have this).
        - Sets ``customer_balance`` and ``supplier_balance`` to the
          same ``balance`` value (v16 had a single Tax column).
        """
        result = list(super()._compute_totals_tax(tax, data))
        registry_type = data.get("registry_type", "customer")

        # Undo v18 RC adjustment: in v18, when a purchase tax appears in
        # the customer registry the base is negated and deductible absorbs
        # undeductible.  V16 did not apply this adjustment.
        if registry_type == "customer" and tax.type_tax_use == "purchase":
            # result[1] = base_balance (was negated by v18)
            result[1] = -result[1]
            # v18 set: deductible = -(orig_ded) - orig_unded, undeductible = 0
            # We cannot perfectly recover the originals from the combined
            # value, so we recompute from the tax record directly.
            context = {
                "from_date": data["from_date"],
                "to_date": data["to_date"],
            }
            if data.get("journal_ids"):
                context["vat_registry_journal_ids"] = data["journal_ids"]
            tax_ctx = self.env["account.tax"].with_context(**context).browse(tax.id)
            result[3] = tax_ctx.deductible_balance
            result[4] = tax_ctx.undeductible_balance

        # V16 had a single "Tax" column: set customer_balance and
        # supplier_balance both equal to balance.
        result[7] = result[2]
        result[8] = result[2]

        return tuple(result)
