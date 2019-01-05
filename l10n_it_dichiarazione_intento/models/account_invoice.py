# -*- coding: utf-8 -*-
# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    dichiarazione_intento_ids = fields.Many2many(
        'dichiarazione.intento', string='Dichiarazioni di Intento', copy=False)
    exclude_from_dichiarazione_intento = fields.Boolean(
        "Escludi da dich. d'intento")

    @api.multi
    def _set_fiscal_position(self):
        for invoice in self:
            if invoice.partner_id and invoice.date_invoice and invoice.type:
                dichiarazioni = self.env['dichiarazione.intento'].get_valid(
                    invoice.type.split('_')[0],
                    invoice.partner_id.id,
                    invoice.date_invoice)
                if dichiarazioni:
                    invoice.fiscal_position_id = \
                        dichiarazioni.fiscal_position_id.id

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        self._set_fiscal_position()
        return res

    @api.onchange('payment_term_id', 'date_invoice')
    def _onchange_payment_term_date_invoice(self):
        res = super(AccountInvoice, self)._onchange_payment_term_date_invoice()
        self._set_fiscal_position()
        return res

    @api.onchange('fiscal_position_id')
    def _onchange_fiscal_position(self):
        """
        Trigger the recompute of the taxes if the fiscal position is changed
        on the invoice.
        """
        for invoice in self:
            invoice.invoice_line_ids._compute_tax_id()

    @api.multi
    def compute_dichiarazione_intento(self):
        dichiarazione_model = self.env['dichiarazione.intento']
        # ------ Check if there is enough available amount on dichiarioni
        for invoice in self:
            if invoice.exclude_from_dichiarazione_intento:
                continue
            dichiarazioni = dichiarazione_model.with_context(
                ignore_state=True if invoice.type.endswith('_refund')
                else False).get_valid(type=invoice.type.split('_')[0],
                                      partner_id=invoice.partner_id.id,
                                      date=invoice.date_invoice)
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                continue
            sign = 1 if invoice.type.endswith('_invoice') else -1
            dichiarazioni_amounts = {}
            for tax_line in invoice.tax_line_ids:
                amount = sign * tax_line.base
                for dichiarazione in dichiarazioni:
                    if dichiarazione.id not in dichiarazioni_amounts:
                        dichiarazioni_amounts[dichiarazione.id] = \
                            dichiarazione.available_amount
                    if tax_line.tax_id.id in [t.id for t
                                              in dichiarazione.taxes_ids]:
                        dichiarazioni_amounts[dichiarazione.id] -= amount
            dichiarazioni_residual = sum([
                dichiarazioni_amounts[da] for da in dichiarazioni_amounts])
            if dichiarazioni_residual < 0:
                raise UserError(_(
                    'Available plafond insufficent.\n'
                    'Excess value: %s' % (abs(dichiarazioni_residual))))

        # ----- Assign account move lines to dichiarazione for invoices
        for invoice in self:
            dichiarazioni = dichiarazione_model.with_context(
                ignore_state=True if invoice.type.endswith('_refund')
                else False).get_valid(type=invoice.type.split('_')[0],
                                      partner_id=invoice.partner_id.id,
                                      date=invoice.date_invoice)
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                continue
            # ----- Get only lines with taxes
            lines = invoice.move_id.line_ids.filtered(
                lambda l: l.tax_ids)
            if not lines:
                continue
            # ----- Group lines for tax
            grouped_lines = {}
            sign = -1 if invoice.type.endswith('_refund') else 1
            # sign = 1 if invoice.type in ('in_invoice', 'out_refund') else -1
            for line in lines:
                tax = line.tax_ids[0]
                if tax not in grouped_lines.keys():
                    grouped_lines.update({tax: []})
                grouped_lines[tax].append(line)
            # ----- Create a detail in dichiarazione for every tax group
            for tax, lines in grouped_lines.iteritems():
                for dichiarazione in dichiarazioni:
                    if tax not in dichiarazione.taxes_ids:
                        continue
                    dich_lines = self.env['dichiarazione.intento.line'].search(
                        [
                            ('dichiarazione_id', '=', dichiarazione.id),
                            ('invoice_id', '=', invoice.id),
                            ('taxes_ids', 'in', [tax.id])
                        ])
                    if dich_lines:
                        # Line already present
                        if invoice.exclude_from_dichiarazione_intento:
                            # if present, remove
                            invoice.dichiarazione_intento_ids = [
                                (2, dichiarazione.id)]
                            dich_lines.unlink()
                        continue
                    if invoice.exclude_from_dichiarazione_intento:
                        continue
                    dichiarazione.line_ids = [(0, 0, {
                        'taxes_ids': [(6, 0, [tax.id, ])],
                        'move_line_ids': [(6, 0, [l.id for l in lines])],
                        'amount': sum([sign * abs(l.balance) for l in lines]),
                        'invoice_id': invoice.id,
                        'base_amount': invoice.amount_untaxed,
                        'currency_id': invoice.currency_id.id,
                        })]
                    # ----- Link dichiarazione to invoice
                    invoice.dichiarazione_intento_ids = [
                        (4, dichiarazione.id)]

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        self.compute_dichiarazione_intento()
        return res

    @api.multi
    def action_invoice_cancel(self):
        line_model = self.env['dichiarazione.intento.line']
        for invoice in self:
            # ----- Force unlink of dichiarazione details to compute used
            #       amount field
            lines = line_model.search([('invoice_id', '=', invoice.id)])
            if lines:
                for line in lines:
                    invoice.dichiarazione_intento_ids = [
                        (3, line.dichiarazione_id.id)]
                lines.unlink()
        return super(AccountInvoice, self).action_invoice_cancel()


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    @api.multi
    def _compute_tax_id(self):
        for line in self:
            invoice_type = line.invoice_id.type
            fpos = line.invoice_id.fiscal_position_id or \
                line.invoice_id.partner_id.property_account_position_id
            # If company_id is set, always filter taxes by the company
            if invoice_type.startswith('out_'):
                product_taxes = line.product_id.taxes_id
            elif invoice_type.startswith('in_'):
                product_taxes = line.product_id.supplier_taxes_id
            else:
                return
            taxes = product_taxes.filtered(
                lambda r: not line.company_id or
                r.company_id == line.company_id)
            line.invoice_line_tax_ids = fpos.map_tax(
                taxes, line.product_id,
                line.invoice_id.partner_shipping_id) if fpos else taxes
