#  Copyright 2022 Simone Rubino - TAKOBI
#  Copyright 2023 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.fields import first
from odoo.tools.translate import _


class AccountMove(models.Model):
    _inherit = "account.move"

    customs_doc_type = fields.Selection(
        [
            ("bill_of_entry", "Bill of Entry"),
            ("supplier_invoice", "Supplier Invoice"),
            ("forwarder_invoice", "Forwarder Invoice"),
        ],
        readonly=True,
    )
    supplier_bill_of_entry_ids = fields.Many2many(
        "account.move",
        "sboe_invoice_rel",
        "sboe_id",
        "invoice_id",
        "Supplier Bill of Entries",
        readonly=True,
        copy=False,
    )
    supplier_invoice_ids = fields.Many2many(
        "account.move",
        "sboe_invoice_rel",
        "invoice_id",
        "sboe_id",
        "Supplier Invoices",
        copy=False,
    )
    forwarder_invoice_id = fields.Many2one(
        "account.move", "Forwarder Invoice", copy=False
    )
    forwarder_bill_of_entry_ids = fields.One2many(
        "account.move",
        "forwarder_invoice_id",
        "Forward Bill of Entries",
        readonly=True,
        copy=False,
    )
    bill_of_entry_storno_id = fields.Many2one(
        "account.move", "Bill of Entry Storno", readonly=True, copy=False
    )
    bill_of_entries_count = fields.Integer(
        "Bill of entries number", compute="_compute_bill_of_entries_count"
    )
    extra_supplier_invoices_count = fields.Integer(
        "Supplier invoices number", compute="_compute_extra_supplier_invoices_count"
    )
    forwarder_bill_of_entries_count = fields.Integer(
        "Bill of entries for forwarder",
        compute="_compute_forwarder_bill_of_entries_count",
    )

    def _compute_bill_of_entries_count(self):
        for inv in self:
            inv.bill_of_entries_count = len(inv.supplier_bill_of_entry_ids)

    def _compute_extra_supplier_invoices_count(self):
        for inv in self:
            inv.extra_supplier_invoices_count = len(inv.supplier_invoice_ids)

    def _compute_forwarder_bill_of_entries_count(self):
        for inv in self:
            inv.forwarder_bill_of_entries_count = len(inv.forwarder_bill_of_entry_ids)

    def _bill_of_entry_view_bills(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_in_invoice_type"
        )
        if len(self) > 1:
            action["domain"] = [("id", "in", self.ids)]
        elif len(self) == 1:
            form_view = [(self.env.ref("account.view_move_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = self.ids[0]
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    def action_view_bill_of_entries(self):
        sboes = self.mapped("supplier_bill_of_entry_ids")
        return sboes._bill_of_entry_view_bills()

    def action_view_extra_supplier_invoices(self):
        invoices = self.mapped("supplier_invoice_ids")
        return invoices._bill_of_entry_view_bills()

    def action_view_forwarder_bill_of_entries(self):
        fboes = self.mapped("forwarder_bill_of_entry_ids")
        return fboes._bill_of_entry_view_bills()

    def _check_forwarder_invoice_advance_customs_vat_line(self, boe_tax_rates):
        self.ensure_one()
        advance_customs_vat_line = False
        for line in self.invoice_line_ids:
            if line.advance_customs_vat:
                advance_customs_vat_line = True
                break
        if not advance_customs_vat_line and list(set(boe_tax_rates)) != [0.0]:
            raise UserError(
                _(
                    "Forwarder invoice %s does not have lines with "
                    "'Advance Customs Vat'"
                )
                % self.name
            )
        return True

    def _get_forwarder_invoice_boe_amounts(self):
        self.ensure_one()
        if not self.forwarder_bill_of_entry_ids:
            raise UserError(_("No bill of entries found for this invoice"))
        for bill_of_entry in self.forwarder_bill_of_entry_ids:
            if bill_of_entry.state not in ("posted", "paid"):
                raise UserError(
                    _(
                        "Bill of entry %(partner)s is in state %(state)s",
                        partner=bill_of_entry.partner_id.name,
                        state=bill_of_entry.state,
                    )
                )

        boe_tax_rates = self.forwarder_bill_of_entry_ids.mapped(
            "invoice_line_ids.tax_ids.amount"
        )
        boe_amounts = self.forwarder_bill_of_entry_ids.mapped("amount_total")
        return boe_amounts, boe_tax_rates

    def _prepare_bill_of_entry_storno(self):
        self.ensure_one()
        if not self.company_id.bill_of_entry_journal_id:
            raise UserError(_("No Bill of entry Storno journal configured"))
        move_vals = {
            "customs_doc_type": False,
            "move_type": "entry",
            "journal_id": self.company_id.bill_of_entry_journal_id.id,
            "date": self.invoice_date,
        }
        move_lines = []
        for inv_line in self.invoice_line_ids:
            if inv_line.advance_customs_vat:
                line_vals = {
                    "name": _("Customs expenses"),
                    "account_id": inv_line.account_id.id,
                    "debit": 0.0,
                    "credit": inv_line.price_subtotal,
                    "partner_id": inv_line.partner_id.id,
                }
                if inv_line.product_id:
                    line_vals["product_id"] = inv_line.product_id.id
                move_lines.append((0, 0, line_vals))

        for bill_of_entry in self.forwarder_bill_of_entry_ids:
            boe_payable_lines = bill_of_entry.line_ids.filtered(
                lambda line: line.account_type == "liability_payable"
            )
            boe_account = first(boe_payable_lines).account_id
            line_vals = {
                "name": _("Customs supplier"),
                "account_id": first(boe_account).id,
                "debit": bill_of_entry.amount_total,
                "credit": 0.0,
                "partner_id": bill_of_entry.partner_id.id,
            }
            move_lines.append((0, 0, line_vals))
            for boe_line in bill_of_entry.invoice_line_ids:
                if boe_line.tax_ids:
                    if len(boe_line.tax_ids) > 1:
                        raise UserError(
                            _("Can't handle more than 1 tax for line %s")
                            % boe_line.name
                        )

                line_vals = {
                    "name": _("Extra UE expenses"),
                    "account_id": boe_line.account_id.id,
                    "debit": 0.0,
                    "credit": boe_line.price_subtotal,
                    "partner_id": boe_line.partner_id.id,
                }
                if boe_line.product_id:
                    line_vals["product_id"] = boe_line.product_id.id
                move_lines.append((0, 0, line_vals))
        move_vals["line_ids"] = move_lines
        return move_vals

    def _reconcile_bill_of_entry_storno(self, move):
        self.ensure_one()
        reconcile_ids = []
        for move_line in move.line_ids:
            line_account = move_line.account_id
            for boe in self.forwarder_bill_of_entry_ids:
                boe_payable_lines = boe.line_ids.filtered(
                    lambda line: line.account_type == "liability_payable"
                )
                boe_account = first(boe_payable_lines).account_id
                if line_account == boe_account:
                    reconcile_ids.append(move_line.id)
                    for boe_move_line in boe.line_ids:
                        if boe_move_line.account_id == boe_account:
                            reconcile_ids.append(boe_move_line.id)
        return self.env["account.move.line"].browse(reconcile_ids).reconcile()

    def action_post(self):
        res = super().action_post()

        for invoice in self:
            if invoice.customs_doc_type == "forwarder_invoice":
                boe_amounts, boe_tax_rates = self._get_forwarder_invoice_boe_amounts()
                # In caso di dichiarazione d'intento inviata alla dogana,
                # la dogana non addebita IVA.
                # La bolla doganale ha righe positive e negative, il cui totale è 0
                if list(set(boe_amounts)) == [0.0]:
                    # Nessuna registrazione di storno è necessaria
                    continue

                self._check_forwarder_invoice_advance_customs_vat_line(boe_tax_rates)

                move_vals = self._prepare_bill_of_entry_storno()
                move = self.env["account.move"].create(move_vals)
                move.action_post()
                invoice.write({"bill_of_entry_storno_id": move.id})

                self._reconcile_bill_of_entry_storno(move)
        return res

    def button_cancel(self):
        res = super().button_cancel()
        for invoice in self:
            for boe in invoice.forwarder_bill_of_entry_ids:
                move = boe.move_id
                rec_lines = (
                    move.mapped("line_ids")
                    .filtered("full_reconcile_id")
                    .mapped("full_reconcile_id.reconciled_line_ids")
                )
                rec_lines.remove_move_reconcile()
            if invoice.bill_of_entry_storno_id:
                invoice.bill_of_entry_storno_id.button_cancel()
                invoice.bill_of_entry_storno_id.with_context(force_delete=True).unlink()
        return res

    def _check_no_taxes(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if line.tax_ids:
                raise UserError(_("Extra UE supplier invoice must have no taxes"))

    def generate_bill_of_entry(self):
        self.ensure_one()
        if self.customs_doc_type != "supplier_invoice":
            raise UserError(
                _("You can generate bill of entry from extra UE supplier invoice only")
            )
        if not self.company_id.bill_of_entry_tax_id:
            raise UserError(
                _("Please set 'Bill of entry tax' in accounting configuration")
            )
        if not self.company_id.bill_of_entry_partner_id:
            raise UserError(
                _("Please set 'Bill of entry partner' in accounting configuration")
            )
        self._check_no_taxes()
        boe_inv = self.copy(
            default={
                "partner_id": self.company_id.bill_of_entry_partner_id.id,
                "customs_doc_type": "bill_of_entry",
            }
        )
        for line in boe_inv.invoice_line_ids:
            tax = self.company_id.bill_of_entry_tax_id
            if line.product_id.supplier_taxes_id:
                tax = line.product_id.supplier_taxes_id[0]
            line.tax_ids = [(6, 0, [tax.id])]
        boe_inv.supplier_invoice_ids = [(4, self.id)]

        action = boe_inv._bill_of_entry_view_bills()
        return action


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    advance_customs_vat = fields.Boolean()
