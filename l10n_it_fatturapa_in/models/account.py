from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class AccountInvoice(models.Model):
    _inherit = "account.move"

    fatturapa_attachment_in_id = fields.Many2one(
        "fatturapa.attachment.in", "E-bill Import File", ondelete="restrict", copy=False
    )
    inconsistencies = fields.Text("Import Inconsistencies", copy=False)
    e_invoice_line_ids = fields.One2many(
        "einvoice.line", "invoice_id", string="Lines Detail", readonly=True, copy=False
    )

    e_invoice_amount_untaxed = fields.Monetary(
        string="E-Invoice Untaxed Amount", readonly=True
    )
    e_invoice_amount_tax = fields.Monetary(string="E-Invoice Tax Amount", readonly=True)
    e_invoice_amount_total = fields.Monetary(
        string="E-Invoice Total Amount", readonly=True
    )

    e_invoice_reference = fields.Char(
        string="E-invoice vendor reference", readonly=True
    )

    e_invoice_date_invoice = fields.Date(string="E-invoice date", readonly=True)

    e_invoice_validation_error = fields.Boolean(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_validation_message = fields.Text(
        compute="_compute_e_invoice_validation_error"
    )

    e_invoice_force_validation = fields.Boolean(string="Force E-Invoice Validation")

    e_invoice_received_date = fields.Date(string="E-Bill Received Date")

    @api.depends(
        "line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual",
        "line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency",  # noqa: B950
        "line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual",
        "line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency",  # noqa: B950
        "line_ids.debit",
        "line_ids.credit",
        "line_ids.currency_id",
        "line_ids.amount_currency",
        "line_ids.amount_residual",
        "line_ids.amount_residual_currency",
        "line_ids.payment_id.state",
        "line_ids.full_reconcile_id",
    )
    def _compute_amount(self):
        super(AccountInvoice, self)._compute_amount()
        for inv in self:
            if inv.efatt_rounding != 0:
                inv.amount_total += inv.efatt_rounding
                sign = inv.move_type in ["in_refund", "out_refund"] and -1 or 1
                inv.amount_total_signed = inv.amount_total * sign

    def action_post(self):
        for invoice in self:
            if (
                invoice.e_invoice_validation_error
                and not invoice.e_invoice_force_validation
            ):
                raise ValidationError(
                    _("The invoice '%s' doesn't match the related e-invoice")
                    % invoice.display_name
                )
        return super().action_post()

    def e_inv_check_amount_untaxed(self):
        error_message = ""
        if (
            self.e_invoice_amount_untaxed
            and float_compare(
                self.amount_untaxed - self.efatt_rounding,
                # Using abs because odoo invoice total can't be negative,
                # while XML total can.
                # See process_negative_lines method
                abs(self.e_invoice_amount_untaxed),
                precision_rounding=self.currency_id.rounding,
            )
            != 0
        ):
            error_message = _(
                "Untaxed amount ({bill_amount_untaxed}) "
                "does not match with "
                "e-bill untaxed amount ({e_bill_amount_untaxed})"
            ).format(
                bill_amount_untaxed=self.amount_untaxed or 0,
                e_bill_amount_untaxed=self.e_invoice_amount_untaxed,
            )
        return error_message

    def e_inv_check_amount_tax(self):
        error_message = ""
        if (
            self.e_invoice_amount_tax
            and float_compare(
                self.amount_tax,
                abs(self.e_invoice_amount_tax),
                precision_rounding=self.currency_id.rounding,
            )
            != 0
        ):
            error_message = _(
                "Taxed amount ({bill_amount_tax}) "
                "does not match with "
                "e-bill taxed amount ({e_bill_amount_tax})"
            ).format(
                bill_amount_tax=self.amount_tax or 0,
                e_bill_amount_tax=self.e_invoice_amount_tax,
            )
        return error_message

    def e_inv_check_amount_total(self):
        error_message = ""
        if (
            self.e_invoice_amount_total
            and float_compare(
                self.amount_total - self.efatt_rounding,
                abs(self.e_invoice_amount_total),
                precision_rounding=self.currency_id.rounding,
            )
            != 0
        ):
            error_message = _(
                "Total amount ({bill_amount_total}) "
                "does not match with "
                "e-bill total amount ({e_bill_amount_total})"
            ).format(
                bill_amount_total=self.amount_total or 0,
                e_bill_amount_total=self.e_invoice_amount_total,
            )
        return error_message

    def e_inv_dati_ritenuta(self):
        error_message = ""
        # ftpa_withholding_type is set when DatiRitenuta is set,
        # withholding_tax is not set if no lines with Ritenuta = SI are found
        if self.ftpa_withholding_ids and not self.withholding_tax:
            error_message += _(
                "E-bill contains DatiRitenuta but no lines subjected to Ritenuta was "
                "found. Please manually check Withholding tax Amount\n"
            )
        if (
            float_compare(
                sum(self.ftpa_withholding_ids.mapped("amount")),
                self.withholding_tax_amount,
                precision_rounding=self.currency_id.rounding,
            )
            != 0
        ):
            error_message += _(
                "E-bill contains ImportoRitenuta %s but created invoice has got"
                " %s\n"
                % (
                    sum(self.ftpa_withholding_ids.mapped("amount")),
                    self.withholding_tax_amount,
                )
            )
        return error_message

    @api.depends(
        "move_type",
        "state",
        "fatturapa_attachment_in_id",
        "amount_untaxed",
        "amount_tax",
        "amount_total",
        "ref",
        "invoice_date",
    )
    def _compute_e_invoice_validation_error(self):
        self.e_invoice_validation_error = False
        self.e_invoice_validation_message = False

        bills_to_check = self.filtered(
            lambda inv: inv.is_purchase_document()
            and inv.state in ["draft", "posted"]
            and inv.fatturapa_attachment_in_id
        )
        for bill in bills_to_check:
            error_messages = list()

            error_message = bill.e_inv_check_amount_untaxed()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_check_amount_tax()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_check_amount_total()
            if error_message:
                error_messages.append(error_message)

            error_message = bill.e_inv_dati_ritenuta()
            if error_message:
                error_messages.append(error_message)

            if bill.e_invoice_reference and bill.ref != bill.e_invoice_reference:
                error_messages.append(
                    _(
                        "Vendor reference ({bill_vendor_ref}) "
                        "does not match with "
                        "e-bill vendor reference ({e_bill_vendor_ref})"
                    ).format(
                        bill_vendor_ref=bill.ref or "",
                        e_bill_vendor_ref=bill.e_invoice_reference,
                    )
                )
            if (
                bill.e_invoice_reference
                and bill.payment_reference != bill.e_invoice_reference
            ):
                error_messages.append(
                    _(
                        "Vendor reference ({bill_vendor_ref}) "
                        "does not match with "
                        "e-bill vendor reference ({e_bill_vendor_ref})"
                    ).format(
                        bill_vendor_ref=bill.payment_reference or "",
                        e_bill_vendor_ref=bill.e_invoice_reference,
                    )
                )

            if (
                bill.e_invoice_date_invoice
                and bill.e_invoice_date_invoice != bill.invoice_date
            ):
                error_messages.append(
                    _(
                        "Invoice date ({bill_date_invoice}) "
                        "does not match with "
                        "e-bill invoice date ({e_bill_date_invoice})"
                    ).format(
                        bill_date_invoice=bill.invoice_date or "",
                        e_bill_date_invoice=bill.e_invoice_date_invoice,
                    )
                )

            if not error_messages:
                continue
            bill.e_invoice_validation_error = True
            bill.e_invoice_validation_message = ",\n".join(error_messages) + "."

    def name_get(self):
        result = super(AccountInvoice, self).name_get()
        res = []
        for tup in result:
            invoice = self.browse(tup[0])
            if invoice.is_purchase_document():
                name = "{}, {}".format(tup[1], invoice.partner_id.name)
                if invoice.amount_total_signed:
                    name += ", {} {}".format(
                        invoice.amount_total_signed,
                        invoice.currency_id.symbol,
                    )
                if invoice.invoice_origin:
                    name += ", %s" % invoice.invoice_origin
                res.append((invoice.id, name))
            else:
                res.append(tup)
        return res

    def remove_attachment_link(self):
        self.ensure_one()
        self.fatturapa_attachment_in_id = False
        return {"type": "ir.actions.client", "tag": "reload"}

    @api.model
    def compute_xml_amount_untaxed(self, FatturaBody):
        amount_untaxed = 0.0
        for Riepilogo in FatturaBody.DatiBeniServizi.DatiRiepilogo:
            amount_untaxed += float(Riepilogo.ImponibileImporto or 0.0)
        return amount_untaxed

    @api.model
    def compute_xml_amount_total(self, FatturaBody, amount_untaxed, amount_tax):
        rounding = float(
            FatturaBody.DatiGenerali.DatiGeneraliDocumento.Arrotondamento or 0.0
        )
        return amount_untaxed + amount_tax + rounding

    @api.model
    def compute_xml_amount_tax(self, DatiRiepilogo):
        amount_tax = 0.0
        for Riepilogo in DatiRiepilogo:
            amount_tax += float(Riepilogo.Imposta or 0.0)
        return amount_tax

    def set_einvoice_data(self, fattura):
        self.ensure_one()
        amount_untaxed = self.compute_xml_amount_untaxed(fattura)
        amount_tax = self.compute_xml_amount_tax(fattura.DatiBeniServizi.DatiRiepilogo)
        amount_total = self.compute_xml_amount_total(
            fattura, amount_untaxed, amount_tax
        )
        reference = fattura.DatiGenerali.DatiGeneraliDocumento.Numero
        date_invoice = fields.Date.from_string(
            fattura.DatiGenerali.DatiGeneraliDocumento.Data
        )

        self.update(
            {
                "e_invoice_amount_untaxed": amount_untaxed,
                "e_invoice_amount_tax": amount_tax,
                "e_invoice_amount_total": amount_total,
                "e_invoice_reference": reference,
                "e_invoice_date_invoice": date_invoice,
            }
        )

    def process_negative_lines(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if line.price_unit >= 0:
                return
        # if every line is negative, change them all
        for line in self.invoice_line_ids:
            line.with_context(check_move_validity=False).update(
                {"price_unit": -line.price_unit}
            )
        self.with_context(check_move_validity=False)._recompute_dynamic_lines(
            recompute_all_taxes=True
        )


class FatturapaArticleCode(models.Model):
    # _position = ['2.2.1.3']
    _name = "fatturapa.article.code"
    _description = "E-bill Article Code"

    name = fields.Char("Code Type")
    code_val = fields.Char("Code Value")
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )


class AccountInvoiceLine(models.Model):
    # _position = [
    #     '2.2.1.3', '2.2.1.6', '2.2.1.7',
    #     '2.2.1.8', '2.1.1.10'
    # ]
    _inherit = "account.move.line"

    fatturapa_attachment_in_id = fields.Many2one(
        "fatturapa.attachment.in",
        "E-bill Import File",
        readonly=True,
        related="move_id.fatturapa_attachment_in_id",
    )


class DiscountRisePrice(models.Model):
    _inherit = "discount.rise.price"
    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )


class EInvoiceLine(models.Model):
    _name = "einvoice.line"
    _description = "E-invoice line"
    invoice_id = fields.Many2one(
        "account.move", "Bill", readonly=True, ondelete="cascade"
    )
    line_number = fields.Integer("Line Number", readonly=True)
    service_type = fields.Char("Sale Provision Type", readonly=True)
    cod_article_ids = fields.One2many(
        "fatturapa.article.code", "e_invoice_line_id", "Articles Code", readonly=True
    )
    name = fields.Char("Description", readonly=True)
    qty = fields.Float("Quantity", readonly=True, digits="Product Unit of Measure")
    uom = fields.Char("Unit of measure", readonly=True)
    period_start_date = fields.Date("Period Start Date", readonly=True)
    period_end_date = fields.Date("Period End Date", readonly=True)
    unit_price = fields.Float("Unit Price", readonly=True, digits="Product Price")
    discount_rise_price_ids = fields.One2many(
        "discount.rise.price",
        "e_invoice_line_id",
        "Discount and Supplement Details",
        readonly=True,
    )
    total_price = fields.Float("Total Price", readonly=True)
    tax_amount = fields.Float("VAT Rate", readonly=True)
    wt_amount = fields.Char("Tax Withholding", readonly=True)
    tax_kind = fields.Char("Nature", readonly=True)
    admin_ref = fields.Char("Administration Reference", readonly=True)
    other_data_ids = fields.One2many(
        "einvoice.line.other.data",
        "e_invoice_line_id",
        string="Other Administrative Data",
        readonly=True,
    )


class EInvoiceLineOtherData(models.Model):
    _name = "einvoice.line.other.data"
    _description = "E-invoice line other data"

    e_invoice_line_id = fields.Many2one(
        "einvoice.line", "Related E-bill Line", readonly=True
    )
    name = fields.Char("Data Type", readonly=True)
    text_ref = fields.Char("Text Reference", readonly=True)
    num_ref = fields.Float("Number Reference", readonly=True)
    date_ref = fields.Char("Date Reference", readonly=True)
