# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2023 Simone Rubino - TAKOBI

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends(
        "move_id",
        "move_id.move_type",
        "move_id.fiscal_position_id",
        "move_id.fiscal_position_id.rc_type_id",
        "tax_ids",
    )
    def _compute_rc_flag(self):
        for line in self:
            move = line.move_id
            # see invoice_line_ids field definition
            is_invoice_line = line.display_type in (
                "product",
                "line_section",
                "line_note",
            )
            is_rc = (
                move.is_purchase_document()
                and move.fiscal_position_id.rc_type_id
                and is_invoice_line
            )
            line.rc = is_rc

    rc = fields.Boolean("RC", compute="_compute_rc_flag", store=True, readonly=False)
    rc_source_line_id = fields.Many2one("account.move.line", readonly=True)

    def _compute_currency_rate(self):
        res = super()._compute_currency_rate()
        for line in self:
            if line.currency_id and line.rc_source_line_id:
                line.currency_rate = line.rc_source_line_id.currency_rate
        return res


class AccountMove(models.Model):
    _inherit = "account.move"

    rc_self_invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Self Invoice",
        copy=False,
        readonly=True,
    )
    rc_purchase_invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Purchase Invoice",
        copy=False,
        readonly=True,
    )
    rc_self_purchase_invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Self Purchase Invoice",
        copy=False,
        readonly=True,
    )
    rc_original_purchase_invoice_ids = fields.One2many(
        "account.move",
        "rc_self_purchase_invoice_id",
        string="Original purchase invoices",
        copy=False,
        readonly=True,
    )
    rc_payment_move_id = fields.Many2one(
        comodel_name="account.move",
        string="RC Payment Move",
        copy=False,
        readonly=True,
    )

    def rc_inv_line_vals(self, line):
        return {
            "product_id": line.product_id.id,
            "name": line.name,
            "product_uom_id": line.product_id.uom_id.id,
            "price_unit": line.price_unit,
            "quantity": line.quantity,
            "discount": line.discount,
            "rc_source_line_id": line.id,
        }

    def rc_inv_vals(self, partner, rc_type, lines, currency):
        if self.move_type == "in_invoice":
            move_type = "out_invoice"
        else:
            move_type = "out_refund"
        supplier = self.partner_id
        original_invoice = self.search(
            [("rc_self_purchase_invoice_id", "=", self.id)], limit=1
        )
        if original_invoice:
            supplier = original_invoice.partner_id

        narration = _(
            "Reverse charge self invoice.\n"
            "Supplier: %(supplier)s\n"
            "Reference: %(reference)s\n"
            "Date: %(date)s\n"
            "Internal reference: %(internal_reference)s",
            supplier=supplier.display_name,
            reference=self.invoice_origin or self.ref or "",
            date=self.date,
            internal_reference=self.name,
        )
        return {
            "partner_id": partner.id,
            "move_type": move_type,
            "journal_id": rc_type.journal_id.id,
            "invoice_line_ids": lines,
            "invoice_date": self.date,
            "date": self.date,
            "invoice_origin": self.sequence_number,
            "rc_purchase_invoice_id": self.id,
            "ref": rc_type.self_invoice_text,
            "currency_id": currency.id,
            "fiscal_position_id": False,
            "invoice_payment_term_id": False,
            "narration": narration,
        }

    def _rc_get_move_line_to_reconcile(self):
        """Get the line to be reconciled in `self`.

        If this move is outbound, then it is the first line having a credit.
        If this move is inbound, then it is the first line having a debit.
        If the line is not found, an exception is raised.
        """
        if self.is_outbound():
            line_field = "credit"
        elif self.is_inbound():
            line_field = "debit"
        else:
            raise UserError(_("Only inbound and outbound moves are supported"))

        is_zero = self.currency_id.is_zero
        for move_line in self.line_ids:
            field_value = getattr(move_line, line_field)
            if not is_zero(field_value) and move_line.account_id.account_type in (
                "asset_receivable",
                "liability_payable",
            ):
                break
        else:
            raise UserError(
                _("No line to reconcile for reverse charge in {move}").format(
                    move=self.display_name,
                )
            )
        return move_line

    def _get_original_suppliers(self):
        rc_purchase_invoices = self.mapped("rc_purchase_invoice_id")
        supplier_invoices = self.env["account.move"]
        for rc_purchase_invoice in rc_purchase_invoices:
            current_supplier_invoices = self.search(
                [("rc_self_purchase_invoice_id", "=", rc_purchase_invoice.id)]
            )
            if current_supplier_invoices:
                supplier_invoices |= current_supplier_invoices
            else:
                supplier_invoices |= rc_purchase_invoice
        return supplier_invoices.mapped("partner_id")

    def compute_rc_amount_tax_main_currency(self):
        """Get Tax for all RC lines in Invoice's Company Currency.

        The result is converted and rounded based on Company Currency
        because this value is used for credit/debit.
        """
        rc_tax_amount = self.get_tax_amount_added_for_rc()

        invoice_currency = self.currency_id
        company_currency = self.company_currency_id
        if invoice_currency != company_currency:
            rc_tax_amount = invoice_currency._convert(
                rc_tax_amount, company_currency, self.company_id, self.invoice_date
            )

        return rc_tax_amount

    def rc_payment_vals(self, rc_type):
        """Values for the RC Payment Move."""
        return {
            "move_type": "entry",
            "journal_id": rc_type.payment_journal_id.id,
            "date": self.date,
        }

    def _rc_line_values(self, account, credit, debit):
        """Base Values for the RC Payment Move lines."""
        return {
            "name": self.name,
            "credit": credit,
            "debit": debit,
            "account_id": account.id,
            "currency_id": self.currency_id.id,
        }

    def _rc_credit_line_amounts(self, amount):
        if self.is_inbound():
            credit, debit = 0, amount
        else:
            credit, debit = amount, 0
        return credit, debit

    def _rc_debit_line_amounts(self, amount):
        if self.is_inbound():
            credit, debit = amount, 0
        else:
            credit, debit = 0, amount
        return credit, debit

    def rc_payment_credit_line_vals(self, line_to_reconcile):
        """Values for the credit line of the RC Payment Move."""
        credit, debit = self._rc_debit_line_amounts(
            abs(line_to_reconcile.balance),
        )
        account = line_to_reconcile.account_id

        line_values = self._rc_line_values(account, credit, debit)
        line_values.update(
            {
                "partner_id": self.partner_id.id,
            }
        )
        return line_values

    def rc_payment_debit_line_vals(self, line_to_reconcile, account):
        """Values for the debit line of the RC Payment Move."""
        credit, debit = self._rc_credit_line_amounts(
            abs(line_to_reconcile.balance),
        )

        line_values = self._rc_line_values(account, credit, debit)
        return line_values

    def rc_credit_line_vals(self, account, amount):
        credit, debit = self._rc_credit_line_amounts(amount)
        return self._rc_line_values(account, credit, debit)

    def rc_debit_line_vals(self, account, amount):
        credit, debit = self._rc_debit_line_amounts(amount)
        line_values = self._rc_line_values(account, credit, debit)
        line_values.update(
            {
                "partner_id": self.partner_id.id,
            }
        )
        return line_values

    def _prepare_rc_supplier_invoice_payment(self, rc_invoice, rc_type):
        """Create RC Payment when there is the supplier invoice.

        The RC Payment has the following lines:
        - one to be reconciled with the RC Invoice
        - one to be reconciled with the original supplier invoice
        """
        rc_payment_data = self.rc_payment_vals(rc_type)
        # Line to be reconciled with the generated RC Invoice
        payment_credit_line_data = rc_invoice.rc_payment_credit_line_vals(
            rc_invoice._rc_get_move_line_to_reconcile(),
        )
        # Line to be reconciled with the original Invoice (self)
        line_to_reconcile = self._rc_get_move_line_to_reconcile()
        payment_debit_line_data = self.rc_debit_line_vals(
            line_to_reconcile.account_id,
            payment_credit_line_data["credit"],
        )
        rc_payment_data["line_ids"] = [
            (0, 0, payment_debit_line_data),
            (0, 0, payment_credit_line_data),
        ]
        return rc_payment_data

    def reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        rc_invoice = self.rc_self_invoice_id

        rc_payment_data = self._prepare_rc_supplier_invoice_payment(rc_invoice, rc_type)
        rc_payment = self.env["account.move"].create(rc_payment_data)
        rc_payment.action_post()
        self.rc_payment_move_id = rc_invoice.rc_payment_move_id = rc_payment

        self._reconcile_rc_invoice_payment(rc_invoice, rc_payment)

    def _prepare_rc_invoice_payment(self, rc_invoice, rc_type):
        """Create RC Payment when there is no supplier invoice.

        The RC Payment has the following lines:
        - two lines to be reconciled with the RC Invoice
        - two lines to be reconciled with the original supplier invoice

        Note that one line of each group is on the RC transitory account.
        """
        rc_payment_data = self.rc_payment_vals(rc_type)

        # Lines to be reconciled with the generated RC Invoice
        rc_invoice_line_to_reconcile = rc_invoice._rc_get_move_line_to_reconcile()
        rc_payment_credit_line_data = rc_invoice.rc_payment_credit_line_vals(
            rc_invoice_line_to_reconcile,
        )
        rc_payment_debit_line_data = rc_invoice.rc_payment_debit_line_vals(
            rc_invoice_line_to_reconcile,
            rc_type.transitory_account_id,
        )

        # Lines to be reconciled with the original supplier Invoice (self)
        rc_tax_amount = self.compute_rc_amount_tax_main_currency()
        payment_credit_line_data = self.rc_credit_line_vals(
            rc_type.transitory_account_id,
            rc_tax_amount,
        )
        line_to_reconcile = self._rc_get_move_line_to_reconcile()
        payment_debit_line_data = self.rc_debit_line_vals(
            line_to_reconcile.account_id,
            rc_tax_amount,
        )

        rc_payment_data["line_ids"] = [
            (0, 0, payment_debit_line_data),
            (0, 0, payment_credit_line_data),
            (0, 0, rc_payment_debit_line_data),
            (0, 0, rc_payment_credit_line_data),
        ]
        return rc_payment_data

    def _rc_reconcile_same_account_line(self, payment):
        """Reconcile `self` with `payment`.

        The move line of `self` to be reconciled is chosen by
        `_rc_get_move_line_to_reconcile`.
        """
        line_to_reconcile = self._rc_get_move_line_to_reconcile()
        if not self.currency_id.is_zero(line_to_reconcile.balance):
            for move_line in payment.line_ids:
                if move_line.account_id == line_to_reconcile.account_id:
                    payment_line_to_reconcile = move_line
                    break
            else:
                raise UserError(
                    _(
                        "No line found to reconcile between "
                        "reverse charge invoice {invoice} "
                        "and reverse charge payment {payment}."
                    ).format(
                        invoice=self.display_name,
                        payment=payment.display_name,
                    )
                )

            if not payment_line_to_reconcile.reconciled:
                # In some cases the payment line is already reconciled
                # simply because it has 0 amount
                rc_lines_to_rec = line_to_reconcile | payment_line_to_reconcile
                rc_lines_to_rec.reconcile()

    def _reconcile_rc_invoice_payment(self, rc_invoice, rc_payment):
        """Reconcile the RC Payment."""
        self._rc_reconcile_same_account_line(rc_payment)
        rc_invoice._rc_reconcile_same_account_line(rc_payment)

    def reconcile_rc_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        rc_invoice = self.rc_self_invoice_id

        rc_payment_data = self._prepare_rc_invoice_payment(rc_invoice, rc_type)
        rc_payment = self.env["account.move"].create(rc_payment_data)
        rc_payment.action_post()
        self.rc_payment_move_id = rc_invoice.rc_payment_move_id = rc_payment

        self._reconcile_rc_invoice_payment(rc_invoice, rc_payment)

    def generate_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if rc_type.partner_type == "other":
            rc_partner = rc_type.partner_id
        else:
            rc_partner = self.partner_id
        rc_currency = self.currency_id

        rc_invoice_lines = []
        for line in self.invoice_line_ids:
            if line.rc:
                rc_invoice_line = self.rc_inv_line_vals(line)
                line_tax_ids = line.tax_ids
                if not line_tax_ids:
                    raise UserError(
                        _(
                            "Invoice %(invoice)s, line\n"
                            " %(line)s\n"
                            " is RC but has not tax",
                            invoice=self.name or self.partner_id.display_name,
                            line=line.name,
                        )
                    )
                mapped_taxes = rc_type.map_tax(
                    line_tax_ids,
                    "purchase_tax_id",
                    "sale_tax_id",
                )
                if line_tax_ids and mapped_taxes:
                    rc_invoice_line["tax_ids"] = [(6, False, mapped_taxes.ids)]
                rc_invoice_line["account_id"] = rc_type.transitory_account_id.id
                rc_invoice_lines.append([0, False, rc_invoice_line])
        if rc_invoice_lines:
            inv_vals = self.rc_inv_vals(
                rc_partner, rc_type, rc_invoice_lines, rc_currency
            )

            # create or write the self invoice
            if self.rc_self_invoice_id:
                # this is needed when user takes back to draft supplier
                # invoice, edit and validate again
                rc_invoice = self.with_context(
                    check_move_validity=False
                ).rc_self_invoice_id
                for line in rc_invoice.line_ids:
                    line.remove_move_reconcile()
                rc_invoice.invoice_line_ids.unlink()
                rc_invoice.write(inv_vals)
            else:
                rc_invoice = self.create(inv_vals)
                self.rc_self_invoice_id = rc_invoice.id
            rc_invoice.action_post()

            if self.amount_total:
                # No need to reconcile invoices with total = 0
                if rc_type.with_supplier_self_invoice:
                    self.reconcile_supplier_invoice()
                else:
                    self.reconcile_rc_invoice()

    def generate_supplier_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        supplier_invoice_vals = self.copy_data()[0]
        supplier_invoice = False
        if self.rc_self_purchase_invoice_id:
            supplier_invoice = self.rc_self_purchase_invoice_id
            for line in supplier_invoice.line_ids:
                line.remove_move_reconcile()
            supplier_invoice.line_ids.with_context(dynamic_unlink=True).unlink()
            # temporary disabling self invoice automations
            supplier_invoice.fiscal_position_id = False

        supplier_invoice_vals["partner_bank_id"] = None
        # because this field has copy=False
        supplier_invoice_vals["date"] = self.date
        supplier_invoice_vals["invoice_date"] = self.date
        supplier_invoice_vals["invoice_origin"] = self.ref or self.name
        supplier_invoice_vals["partner_id"] = rc_type.partner_id.id
        supplier_invoice_vals["journal_id"] = rc_type.supplier_journal_id.id
        # temporary disabling self invoice automations
        supplier_invoice_vals["fiscal_position_id"] = None
        supplier_invoice_vals.pop("line_ids")

        if not supplier_invoice:
            supplier_invoice = self.create(supplier_invoice_vals)
        invoice_line_vals = []
        for inv_line in self.invoice_line_ids:
            line_vals = inv_line.copy_data()[0]
            line_vals["rc_source_line_id"] = inv_line.id
            line_vals["move_id"] = supplier_invoice.id
            line_tax_ids = inv_line.tax_ids
            mapped_taxes = rc_type.map_tax(
                line_tax_ids,
                "original_purchase_tax_id",
                "purchase_tax_id",
            )
            if line_tax_ids and mapped_taxes:
                line_vals["tax_ids"] = [
                    (6, False, mapped_taxes.ids),
                ]
            line_vals["account_id"] = rc_type.transitory_account_id.id
            invoice_line_vals.append((0, 0, line_vals))
        supplier_invoice.write({"invoice_line_ids": invoice_line_vals})
        self.rc_self_purchase_invoice_id = supplier_invoice.id

        supplier_invoice.action_post()
        supplier_invoice.fiscal_position_id = self.fiscal_position_id.id

    def action_post(self):
        ret = super().action_post()
        for invoice in self:
            fp = invoice.fiscal_position_id
            rc_type = fp and fp.rc_type_id
            if not rc_type:
                continue
            if rc_type.method == "selfinvoice":
                if not rc_type.with_supplier_self_invoice:
                    invoice.generate_self_invoice()
                else:
                    # See with_supplier_self_invoice field help
                    invoice.generate_supplier_self_invoice()
                    invoice.rc_self_purchase_invoice_id.generate_self_invoice()
            elif rc_type.method == "integration":
                raise UserError(
                    _(
                        "VAT integration RC type, "
                        "defined in fiscal position {fp}, is not managed yet"
                    ).format(fp=fp.display_name)
                )
        return ret

    def remove_rc_payment(self, delete_self_invoice=True):
        rc_invoice = self.rc_self_invoice_id
        rc_invoice.remove_invoice_payment()

        if delete_self_invoice:
            # unlink self invoice
            self_invoice = self.with_context(force_delete=True).browse(rc_invoice.id)
            self_invoice.line_ids.remove_move_reconcile()
            self_invoice.unlink()

    def remove_invoice_payment(self):
        payment_move = self.rc_payment_move_id
        if payment_move:
            payment_move.line_ids.remove_move_reconcile()
            payment_move.with_context(force_delete=True).unlink()

    def button_cancel(self):
        for inv in self:
            rc_type = inv.fiscal_position_id.rc_type_id
            if rc_type and rc_type.method == "selfinvoice" and inv.rc_self_invoice_id:
                inv.remove_rc_payment()
            elif (
                rc_type
                and rc_type.method == "selfinvoice"
                and inv.rc_self_purchase_invoice_id
            ):
                inv.rc_self_purchase_invoice_id.remove_rc_payment()
                inv.rc_self_purchase_invoice_id.button_cancel()
        return super().button_cancel()

    def button_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        invoice_model = new_self.env["account.move"]
        for inv in new_self.filtered(lambda i: i != i.rc_payment_move_id):
            # remove payments without deleting self invoice
            inv.remove_rc_payment(delete_self_invoice=False)
            inv.remove_invoice_payment()

            if inv.rc_self_invoice_id:
                self_invoice = invoice_model.browse(inv.rc_self_invoice_id.id)
                self_invoice.button_draft()
            if inv.rc_self_purchase_invoice_id:
                self_purchase_invoice = invoice_model.browse(
                    inv.rc_self_purchase_invoice_id.id
                )
                self_purchase_invoice.button_draft()
        return super(AccountMove, new_self).button_draft()

    def get_tax_amount_added_for_rc(self):
        res = 0
        for line in self.invoice_line_ids:
            if line.rc:
                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = line.tax_ids.compute_all(
                    price_unit,
                    self.currency_id,
                    line.quantity,
                    line.product_id,
                    self.partner_id,
                )["taxes"]
                for tax in taxes:
                    res += tax["amount"]
        return res
