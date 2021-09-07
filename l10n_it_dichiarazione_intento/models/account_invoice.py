# Copyright 2017 Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.misc import format_date


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    dichiarazione_intento_ids = fields.Many2many(
        'dichiarazione.intento', string='Declarations of intent')

    @api.multi
    def _set_fiscal_position(self):
        for invoice in self:
            if invoice.partner_id and invoice.type:
                all_dichiarazioni = self.env[
                    'dichiarazione.intento'].get_all_for_partner(
                    invoice.type.split('_')[0],
                    invoice.partner_id.commercial_partner_id.id
                    )
                if not all_dichiarazioni:
                    return
                valid_date = invoice.date_invoice or fields.Date.context_today(invoice)

                dichiarazioni_valide = all_dichiarazioni.filtered(
                    lambda d: d.date_start <= valid_date <= d.date_end
                    )
                if dichiarazioni_valide:
                    invoice.fiscal_position_id = \
                        dichiarazioni_valide[0].fiscal_position_id.id
                elif (
                    invoice.fiscal_position_id and
                    invoice.fiscal_position_id.id in [
                        d.fiscal_position_id.id for d in all_dichiarazioni]):
                    invoice.fiscal_position_id = False

    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        self._set_fiscal_position()

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        self._set_fiscal_position()
        return res

    def select_manually_declarations(self):
        self.ensure_one()
        action = self.env.ref(
            'l10n_it_dichiarazione_intento.select_manually_declarations_action'
            ).read()[0]
        return action

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        dichiarazione_model = self.env['dichiarazione.intento']
        # ------ Check if there is enough available amount on dichiarazioni
        for invoice in self:
            if invoice.dichiarazione_intento_ids:
                dichiarazioni = invoice.dichiarazione_intento_ids
            else:
                dichiarazioni = dichiarazione_model.with_context(
                    ignore_state=True if invoice.type.endswith('_refund')
                    else False).get_valid(type_d=invoice.type.split('_')[0],
                                          partner_id=invoice.partner_id.id,
                                          date=invoice.date_invoice)
            # ----- If partner hasn't dichiarazioni, do nothing
            if not dichiarazioni:
                # ----  check se posizione fiscale dichiarazione di intento
                # ---- e non ho dichiarazioni, segnalo errore
                if self.fiscal_position_id.valid_for_dichiarazione_intento:
                    raise UserError(_(
                        'Declaration of intent not found. Add new declaration or '
                        'change fiscal position and verify applied tax'))
                else:
                    continue
            available_plafond = 0.0
            if invoice.type in ['in_invoice', 'in_refund']:
                plafond = self.env.user.company_id.\
                    dichiarazione_yearly_limit_ids.filtered(
                        lambda r: r.year == str(
                            fields.first(dichiarazioni).date_start.year)
                    )
                available_plafond = plafond.limit_amount - plafond.actual_used_amount
            sign = 1 if invoice.type in ['out_invoice', 'in_invoice'] else -1
            dichiarazioni_amounts = {}
            for tax_line in invoice.tax_line_ids:
                amount = sign * tax_line.base
                for dichiarazione in dichiarazioni:
                    if dichiarazione.id not in dichiarazioni_amounts:
                        if invoice.type in ['in_invoice', 'in_refund'] and \
                                dichiarazione.available_amount > available_plafond:
                            dichiarazioni_amounts[dichiarazione.id] = available_plafond
                        else:
                            dichiarazioni_amounts[dichiarazione.id] = \
                                dichiarazione.available_amount
                    if tax_line.tax_id.id in [t.id for t
                                              in dichiarazione.taxes_ids]:
                        dichiarazioni_amounts[dichiarazione.id] -= amount
                        amount = 0.0
            dichiarazioni_residual = sum([
                dichiarazioni_amounts[da] for da in dichiarazioni_amounts])
            if dichiarazioni_residual < 0:
                raise UserError(_(
                    'Available plafond insufficent.\n'
                    'Excess value: %s') % (abs(dichiarazioni_residual)))
            # Check se con nota credito ho superato il plafond
            for dich in dichiarazioni_amounts:
                dichiarazione = dichiarazione_model.browse(dich)
                # dichiarazioni_amounts contains residual, so, if > limit_amount,
                # used_amount went < 0
                if dichiarazioni_amounts[dich] > dichiarazione.limit_amount:
                    raise UserError(_(
                        'Available plafond insufficent.\n'
                        'Excess value: %s') % (
                            abs(dichiarazioni_amounts[dich] -
                                dichiarazione.limit_amount)
                    ))
        # ----- Assign account move lines to dichiarazione for invoices
        for invoice in self:
            if invoice.dichiarazione_intento_ids:
                dichiarazioni = invoice.dichiarazione_intento_ids
            else:
                dichiarazioni = dichiarazione_model.with_context(
                    ignore_state=True if invoice.type.endswith('_refund')
                    else False).get_valid(type_d=invoice.type.split('_')[0],
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
                force_declaration = line.force_dichiarazione_intento_id
                tax = line.tax_ids[0]
                if force_declaration not in list(grouped_lines.keys()):
                    grouped_lines.update({force_declaration: {}})
                if tax not in grouped_lines[force_declaration]:
                    grouped_lines[force_declaration].update({tax: []})
                grouped_lines[force_declaration][tax].append(line)
            for force_declaration in grouped_lines.keys():
                for tax, lines in grouped_lines[force_declaration].items():
                    # ----- Create a detail in dichiarazione
                    #       for every tax group
                    if invoice.type in ('out_invoice', 'in_refund'):
                        amount = sum([sign * (line.credit - line.debit)
                                      for line in lines])
                    else:
                        amount = sum([sign * (line.debit - line.credit)
                                      for line in lines])
                    # Select right declaration(s)
                    if force_declaration:
                        declarations = [force_declaration, ]
                    else:
                        declarations = dichiarazioni
                    for dichiarazione in declarations:
                        if tax not in dichiarazione.taxes_ids:
                            continue
                        dichiarazione.line_ids = [(0, 0, {
                            'taxes_ids': [(6, 0, [tax.id, ])],
                            'move_line_ids': [(6, 0, [l.id for l in lines])],
                            'amount': amount,
                            'invoice_id': invoice.id,
                            'base_amount': invoice.amount_untaxed,
                            'currency_id': invoice.currency_id.id,
                            })]
                        # ----- Link dichiarazione to invoice
                        invoice.dichiarazione_intento_ids = [
                            (4, dichiarazione.id)]
                        if invoice.type in ("out_invoice", "out_refund"):
                            if not invoice.comment:
                                invoice.comment = ''
                            invoice.comment += (
                                "\n\nVostra dichiarazione d'intento del %s, "
                                "protocollo telematico nr %s."
                                % (
                                    format_date(
                                        self.env, dichiarazione.date),
                                    dichiarazione.telematic_protocol
                                )
                            )

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

    @api.model
    def invoice_line_move_line_get(self):
        move_lines = super(AccountInvoice, self).invoice_line_move_line_get()
        invoice_line_model = self.env['account.invoice.line']
        for move_line in move_lines:
            inv_line_id = move_line.get('invl_id', False)
            if inv_line_id:
                inv_line = invoice_line_model.browse(inv_line_id)
                if inv_line.force_dichiarazione_intento_id:
                    move_line['force_dichiarazione_intento_id'] = \
                        inv_line.force_dichiarazione_intento_id.id
        return move_lines


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    force_dichiarazione_intento_id = fields.Many2one(
        'dichiarazione.intento',
        string='Force Declaration of Intent')

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
