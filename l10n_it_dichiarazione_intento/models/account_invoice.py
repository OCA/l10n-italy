# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountMove(models.Model):

    _inherit = "account.move"

    dichiarazione_intento_ids = fields.Many2many(
        "dichiarazione.intento", string="Declarations of intent"
    )

    def _set_fiscal_position(self):
        for invoice in self:
            if invoice.partner_id and invoice.move_type:
                invoice_type_short = invoice.get_type_short()
                if not invoice_type_short:
                    continue
                all_dichiarazioni = self.env[
                    "dichiarazione.intento"
                ].get_all_for_partner(
                    invoice_type_short,
                    invoice.partner_id.commercial_partner_id.id,
                )
                if not all_dichiarazioni:
                    return
                valid_date = invoice.invoice_date or fields.Date.context_today(invoice)

                dichiarazioni_valide = all_dichiarazioni.filtered(
                    lambda d: d.date_start <= valid_date <= d.date_end
                )
                if dichiarazioni_valide:
                    invoice.fiscal_position_id = dichiarazioni_valide[
                        0
                    ].fiscal_position_id.id
                elif invoice.fiscal_position_id and invoice.fiscal_position_id.id in [
                    d.fiscal_position_id.id for d in all_dichiarazioni
                ]:
                    invoice.fiscal_position_id = False

    def get_type_short(self):
        """
        Get in/out value from the invoice.

        This will then be matched with field dichiarazione.intento.type.
        For instance:
        an invoice of type `in_refund` returns `in`,
        an invoice of type `out_refund` returns `out`,
        an invoice of type `entry` returns ``.
        """
        self.ensure_one()
        invoice_type_short = ""
        if "_" in self.move_type:
            invoice_type_short = self.move_type.split("_")[0]
        return invoice_type_short

    @api.onchange("invoice_date")
    def _onchange_date_invoice(self):
        self._set_fiscal_position()

    @api.onchange("partner_id", "company_id")
    def _onchange_partner_id(self):
        res = super()._onchange_partner_id()
        self._set_fiscal_position()
        return res

    def select_manually_declarations(self):
        self.ensure_one()
        action = self.env.ref(
            "l10n_it_dichiarazione_intento.select_manually_declarations_action"
        ).read()[0]
        return action

    def action_post(self):
        res = super().action_post()
        # ------ Check if there is enough available amount on dichiarazioni
        for invoice in self:
            dichiarazioni = invoice.get_declarations()
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                # ----  check se posizione fiscale dichiarazione di intento
                # ---- e non ho dichiarazioni, segnalo errore
                if invoice.fiscal_position_id.valid_for_dichiarazione_intento:
                    raise UserError(
                        _(
                            "Declaration of intent not found. Add new declaration or "
                            "change fiscal position and verify applied tax"
                        )
                    )
                else:
                    continue

            invoice.check_declarations_amounts(dichiarazioni)

        # ----- Assign account move lines to dichiarazione for invoices
        for invoice in self:
            dichiarazioni = invoice.get_declarations()
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                continue
            # ----- Get only lines with taxes
            lines = invoice.line_ids.filtered("tax_ids")
            if not lines:
                continue
            # ----- Group lines for tax
            grouped_lines = self.get_move_lines_by_declaration(lines)
            invoice.update_declarations(dichiarazioni, grouped_lines)

        return res

    def update_declarations(self, dichiarazioni, grouped_lines):
        """
        Update the declarations adding a new line representing this invoice.

        Also add a comment in this invoice stating which declaration is into.
        """
        self.ensure_one()
        sign = -1 if self.move_type.endswith("_refund") else 1
        for force_declaration in grouped_lines.keys():
            for tax, lines in grouped_lines[force_declaration].items():
                # ----- Create a detail in dichiarazione
                #       for every tax group
                if self.move_type in ("out_invoice", "in_refund"):
                    amount = sum(sign * (line.credit - line.debit) for line in lines)
                else:
                    amount = sum(sign * (line.debit - line.credit) for line in lines)
                # Select right declaration(s)
                if force_declaration:
                    declarations = [force_declaration]
                else:
                    declarations = dichiarazioni

                for dichiarazione in declarations:
                    if tax not in dichiarazione.taxes_ids:
                        continue
                    dichiarazione.line_ids = [
                        (0, 0, self._prepare_declaration_line(amount, lines, tax)),
                    ]
                    # ----- Link dichiarazione to invoice
                    self.dichiarazione_intento_ids = [(4, dichiarazione.id)]
                    if self.move_type in ("out_invoice", "out_refund"):
                        if not self.narration:
                            self.narration = ""
                        self.narration += (
                            "\n\nVostra dichiarazione d'intento nr %s del %s, "
                            "nostro protocollo nr %s del %s, "
                            "protocollo telematico nr %s."
                            % (
                                dichiarazione.partner_document_number,
                                format_date(
                                    self.env, dichiarazione.partner_document_date
                                ),
                                dichiarazione.number,
                                format_date(self.env, dichiarazione.date),
                                dichiarazione.telematic_protocol,
                            )
                        )

    def _prepare_declaration_line(self, amount, lines, tax):
        """Dictionary used to create declaration line for this invoice."""
        self.ensure_one()
        return {
            "taxes_ids": [
                (6, 0, tax.ids),
            ],
            "move_line_ids": [
                (6, 0, lines.ids),
            ],
            "amount": amount,
            "invoice_id": self.id,
            "base_amount": self.amount_untaxed,
            "currency_id": self.currency_id.id,
        }

    @api.model
    def get_move_lines_by_declaration(self, lines):
        """Get account move lines grouped by the declaration forced in each line."""
        grouped_lines = {}
        invoice_line_model = self.env["account.move.line"]
        for line in lines:
            force_declaration = line.force_dichiarazione_intento_id
            if force_declaration not in grouped_lines:
                grouped_lines.update({force_declaration: {}})

            tax = line.tax_ids[0]
            if tax not in grouped_lines[force_declaration]:
                grouped_lines[force_declaration].update(
                    {tax: invoice_line_model.browse()}
                )

            grouped_lines[force_declaration][tax] |= line
        return grouped_lines

    def get_declarations(self):
        """Get declarations linked directly or indirectly to this invoice."""
        self.ensure_one()
        dichiarazione_model = self.env["dichiarazione.intento"]
        if self.dichiarazione_intento_ids:
            dichiarazioni = self.dichiarazione_intento_ids
        else:
            dichiarazioni = dichiarazione_model.with_context(
                ignore_state=True if self.move_type.endswith("_refund") else False
            ).get_valid(
                type_d=self.move_type.split("_")[0],
                partner_id=self.partner_id.id,
                date=self.invoice_date,
            )
        return dichiarazioni

    def check_declarations_amounts(self, declarations):
        """
        Compare this invoice's tax amounts and `declarations` plafond.

        An exception is raised if the plafond of the declarations
        is not sufficient for this invoice's taxes.
        """
        self.ensure_one()
        declarations_amounts = self.get_declaration_residual_amounts(declarations)

        declarations_residual = sum(
            [declarations_amounts[da] for da in declarations_amounts]
        )
        if declarations_residual < 0:
            raise UserError(
                _("Available plafond insufficent.\n" "Excess value: %s")
                % (abs(declarations_residual))
            )

        # Check se con nota credito ho superato il plafond
        declaration_model = self.env["dichiarazione.intento"]
        for dich in declarations_amounts:
            declaration = declaration_model.browse(dich)
            # declarations_amounts contains residual, so, if > limit_amount,
            # used_amount went < 0
            if declarations_amounts[dich] > declaration.limit_amount:
                excess = abs(declarations_amounts[dich] - declaration.limit_amount)
                raise UserError(
                    _("Available plafond insufficent.\n" "Excess value: %s") % excess
                )
        return True

    def get_declaration_residual_amounts(self, declarations):
        """Get residual amount for every `declarations`."""
        dichiarazioni_amounts = {}
        # If the tax amount is 0, then there is no line representing the tax
        # so there will be no line having tax_line_id.
        # Therefore we choose instead the lines that
        # should generate the tax line i.e. the lines that have `tax_ids`
        tax_lines = self.line_ids.filtered("tax_ids")
        for tax_line in tax_lines:
            # Move lines having `tax_ids` represent the base amount for those taxes
            amount = tax_line.price_subtotal
            for declaration in declarations:
                if declaration.id not in dichiarazioni_amounts:
                    dichiarazioni_amounts[declaration.id] = declaration.available_amount
                if any(tax in declaration.taxes_ids for tax in tax_line.tax_ids):
                    dichiarazioni_amounts[declaration.id] -= amount
        return dichiarazioni_amounts

    def button_cancel(self):
        line_model = self.env["dichiarazione.intento.line"]
        for invoice in self:
            # ----- Force unlink of dichiarazione details to compute used
            #       amount field
            lines = line_model.search([("invoice_id", "=", invoice.id)])
            if lines:
                for line in lines:
                    invoice.dichiarazione_intento_ids = [(3, line.dichiarazione_id.id)]
                lines.unlink()
        return super().button_cancel()


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    force_dichiarazione_intento_id = fields.Many2one(
        "dichiarazione.intento", string="Force Declaration of Intent"
    )

    def _compute_tax_id(self):
        for line in self:
            invoice_type = line.invoice_id.move_type
            fpos = (
                line.move_id.fiscal_position_id
                or line.move_id.partner_id.property_account_position_id
            )
            # If company_id is set, always filter taxes by the company
            if invoice_type.startswith("out_"):
                product_taxes = line.product_id.taxes_id
            elif invoice_type.startswith("in_"):
                product_taxes = line.product_id.supplier_taxes_id
            else:
                return
            taxes = product_taxes.filtered(
                lambda r: not line.company_id or r.company_id == line.company_id
            )
            line.invoice_line_tax_ids = (
                fpos.map_tax(taxes, line.product_id, line.move_id.partner_shipping_id)
                if fpos
                else taxes
            )
