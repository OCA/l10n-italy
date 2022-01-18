# Copyright 2016 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _set_rc_flag(self, invoice):
        self.ensure_one()
        if invoice.is_purchase_document():
            fposition = invoice.fiscal_position_id
            self.rc = bool(fposition.rc_type_id)

    rc = fields.Boolean("RC")

    @api.onchange("tax_ids")
    def onchange_rc_tax_ids(self):
        self._set_rc_flag(self.move_id)


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

    @api.onchange("fiscal_position_id")
    def onchange_rc_fiscal_position_id(self):
        for line in self.invoice_line_ids:
            line._set_rc_flag(self)

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        # In some cases (like creating the invoice from PO),
        # fiscal position's onchange is triggered
        # before than being changed by this method.
        self.onchange_rc_fiscal_position_id()
        return res

    def rc_inv_line_vals(self, line):
        return {
            "product_id": line.product_id.id,
            "name": line.name,
            "product_uom_id": line.product_id.uom_id.id,
            "price_unit": line.price_unit,
            "quantity": line.quantity,
            "discount": line.discount,
        }

    def rc_inv_vals(self, partner, rc_type, lines, currency):
        if self.move_type == "in_invoice":
            move_type = "out_invoice"
        else:
            move_type = "out_refund"

        narration = _(
            "Reverse charge self invoice.\n"
            "Supplier: %s\n"
            "Reference: %s\n"
            "Date: %s\n"
            "Internal reference: %s"
        ) % (
            self.partner_id.display_name,
            self.ref or "",
            self.date,
            self.name,
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
            "name": rc_type.self_invoice_text,
            "currency_id": currency.id,
            "fiscal_position_id": False,
            "invoice_payment_term_id": False,
            "narration": narration,
        }

    def get_inv_line_to_reconcile(self):
        for inv_line in self.line_ids:
            if ((self.move_type == "in_invoice") and inv_line.credit) or (
                (self.move_type == "in_refund") and inv_line.debit
            ):
                return inv_line
        return False

    def get_rc_inv_line_to_reconcile(self, invoice):
        for inv_line in invoice.line_ids:
            if ((self.move_type == "out_invoice") and inv_line.debit) or (
                (self.move_type == "out_refund") and inv_line.credit
            ):
                return inv_line
        return False

    def compute_rc_amount_tax(self):
        rc_amount_tax = 0.0
        round_curr = self.currency_id.round
        rc_lines = self.invoice_line_ids.filtered(lambda l: l.rc)
        for rc_line in rc_lines:
            price_unit = rc_line.price_unit * (1 - (rc_line.discount or 0.0) / 100.0)
            taxes = rc_line.tax_ids.compute_all(
                price_unit,
                self.currency_id,
                rc_line.quantity,
                product=rc_line.product_id,
                partner=rc_line.partner_id,
            )["taxes"]
            rc_amount_tax += sum([tax["amount"] for tax in taxes])

        # convert the amount to main company currency, as
        # compute_rc_amount_tax is used for debit/credit fields
        invoice_currency = self.currency_id.with_context(date=self.invoice_date)
        main_currency = self.company_currency_id.with_context(date=self.invoice_date)
        if invoice_currency != main_currency:
            round_curr = main_currency.round
            rc_amount_tax = invoice_currency.compute(rc_amount_tax, main_currency)

        return round_curr(rc_amount_tax)

    def reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        payment_reg = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.ids)
            .create(
                {
                    "payment_date": self.date,
                    "amount": self.amount_total,
                    "journal_id": rc_type.payment_journal_id.id,
                    "currency_id": self.currency_id.id,
                }
            )
        )
        self.payment_id = payment_reg._create_payments()

        return True

    def partially_reconcile_supplier_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        amount = self.get_tax_amount_added_for_rc()
        payment_reg = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=self.ids)
            .create(
                {
                    "payment_date": self.date,
                    "amount": amount,
                    "journal_id": rc_type.payment_journal_id.id,
                    "currency_id": self.currency_id.id,
                }
            )
        )
        self.payment_id = payment_reg._create_payments()

        return True

    def reconcile_rc_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        rc_invoice = self.rc_self_invoice_id
        payment_reg = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=rc_invoice.ids)
            .create(
                {
                    "payment_date": rc_invoice.date,
                    "amount": rc_invoice.amount_total,
                    "journal_id": rc_type.payment_journal_id.id,
                    "currency_id": rc_invoice.currency_id.id,
                }
            )
        )
        rc_invoice.payment_id = payment_reg._create_payments()

        return True

    def generate_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if not rc_type.payment_journal_id.default_account_id:
            raise UserError(
                _("There is no default credit account defined \n" 'on journal "%s".')
                % rc_type.payment_journal_id.name
            )
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
                        _("Invoice %s, line\n%s\nis RC but has not tax")
                        % ((self.name or self.partner_id.display_name), line.name)
                    )
                tax_ids = list()
                for tax_mapping in rc_type.tax_ids:
                    for line_tax_id in line_tax_ids:
                        if tax_mapping.purchase_tax_id == line_tax_id:
                            tax_ids.append(tax_mapping.sale_tax_id.id)
                if not tax_ids:
                    raise UserError(
                        _("Tax code used is not a RC tax.\nCan't " "find tax mapping")
                    )
                if line_tax_ids:
                    rc_invoice_line["tax_ids"] = [(6, False, tax_ids)]
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
                # rc_invoice.period_id = False
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
                    self.partially_reconcile_supplier_invoice()

    def generate_supplier_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if not len(rc_type.tax_ids) == 1:
            raise UserError(_("Can't find 1 tax mapping for %s" % rc_type.name))
        supplier_invoice_vals = self.copy_data()[0]
        supplier_invoice = False
        if self.rc_self_purchase_invoice_id:
            supplier_invoice = self.rc_self_purchase_invoice_id
            for line in supplier_invoice.line_ids:
                line.remove_move_reconcile()
            supplier_invoice.invoice_line_ids.unlink()

        supplier_invoice_vals["partner_bank_id"] = None
        # because this field has copy=False
        supplier_invoice_vals["date"] = self.date
        supplier_invoice_vals["invoice_date"] = self.date
        supplier_invoice_vals["partner_id"] = rc_type.partner_id.id
        supplier_invoice_vals["journal_id"] = rc_type.supplier_journal_id.id
        # temporary disabling self invoice automations
        supplier_invoice_vals["fiscal_position_id"] = None

        if not supplier_invoice:
            supplier_invoice = self.create(supplier_invoice_vals)
        for inv_line in supplier_invoice.invoice_line_ids:
            inv_line.tax_ids = [(6, 0, [rc_type.tax_ids[0].purchase_tax_id.id])]
            inv_line.account_id = rc_type.transitory_account_id.id
        self.rc_self_purchase_invoice_id = supplier_invoice.id

        supplier_invoice.action_post()
        supplier_invoice.fiscal_position_id = self.fiscal_position_id.id

    def action_post(self):
        super(AccountMove, self).action_post()
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
        return False

    def remove_rc_payment(self, delete_self_invoice=True):
        rc_invoice = self.rc_self_invoice_id
        rc_invoice.remove_invoice_payment()

        if delete_self_invoice:
            # unlink self invoice
            self_invoice = self.with_context(force_delete=True).browse(rc_invoice.id)
            self_invoice.unlink()

    def remove_invoice_payment(self):
        if self.payment_id:
            move = self.payment_id.move_id
            for line in move.line_ids:
                line.remove_move_reconcile()
            self.payment_id.unlink()

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
        return super(AccountMove, self).button_cancel()

    def button_draft(self):
        new_self = self.with_context(rc_set_to_draft=True)
        invoice_model = new_self.env["account.move"]
        for inv in new_self:
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
