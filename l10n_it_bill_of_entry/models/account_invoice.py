from odoo import fields, models, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    customs_doc_type = fields.Selection([
        ('bill_of_entry', 'Bill of Entry'),
        ('supplier_invoice', 'Supplier Invoice'),
        ('forwarder_invoice', 'Forwarder Invoice'),
    ], 'Customs Doc Type', readonly=True)
    supplier_bill_of_entry_ids = fields.Many2many(
        'account.invoice', 'sboe_invoice_rel', 'sboe_id', 'invoice_id',
        'Supplier Bill of Entries', readonly=True, copy=False)
    supplier_invoice_ids = fields.Many2many(
        'account.invoice', 'sboe_invoice_rel', 'invoice_id', 'sboe_id',
        'Supplier Invoices', copy=False)
    forwarder_invoice_id = fields.Many2one(
        'account.invoice', 'Forwarder Invoice', copy=False)
    forwarder_bill_of_entry_ids = fields.One2many(
        'account.invoice', 'forwarder_invoice_id',
        'Forward Bill of Entries', readonly=True, copy=False)
    bill_of_entry_storno_id = fields.Many2one(
        'account.move', 'Bill of Entry Storno', readonly=True, copy=False)
    bill_of_entries_count = fields.Integer(
        "Bill of entries number", compute="_compute_bill_of_entries_count")
    extra_supplier_invoices_count = fields.Integer(
        "Supplier invoices number", compute="_compute_extra_supplier_invoices_count")
    forwarder_bill_of_entries_count = fields.Integer(
        "Bill of entries for forwarder",
        compute="_compute_forwarder_bill_of_entries_count")

    @api.multi
    def _compute_bill_of_entries_count(self):
        for inv in self:
            inv.bill_of_entries_count = len(inv.supplier_bill_of_entry_ids)

    @api.multi
    def _compute_extra_supplier_invoices_count(self):
        for inv in self:
            inv.extra_supplier_invoices_count = len(inv.supplier_invoice_ids)

    @api.multi
    def _compute_forwarder_bill_of_entries_count(self):
        for inv in self:
            inv.forwarder_bill_of_entries_count = len(inv.forwarder_bill_of_entry_ids)

    @api.multi
    def action_view_bill_of_entries(self):
        boes = self.mapped('supplier_bill_of_entry_ids')
        action = self.env.ref('account.action_vendor_bill_template').read()[0]
        if len(boes) > 1:
            action['domain'] = [('id', 'in', boes.ids)]
        elif len(boes) == 1:
            form_view = [(self.env.ref('account.invoice_supplier_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [
                    (state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = boes.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_view_extra_supplier_invoices(self):
        invoices = self.mapped('supplier_invoice_ids')
        action = self.env.ref('account.action_vendor_bill_template').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.invoice_supplier_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [
                    (state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_view_forwarder_bill_of_entries(self):
        boes = self.mapped('forwarder_bill_of_entry_ids')
        action = self.env.ref('account.action_vendor_bill_template').read()[0]
        if len(boes) > 1:
            action['domain'] = [('id', 'in', boes.ids)]
        elif len(boes) == 1:
            form_view = [(self.env.ref('account.invoice_supplier_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [
                    (state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = boes.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()

        AccountMove = self.env['account.move']
        AccountMoveLine = self.env['account.move.line']
        for invoice in self:
            if invoice.customs_doc_type == 'forwarder_invoice':
                if not invoice.forwarder_bill_of_entry_ids:
                    raise UserError(_("No bill of entries found for this invoice"))
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    if bill_of_entry.state not in ('open', 'paid'):
                        raise UserError(
                            _('Bill of entry %s is in state %s')
                            % (
                                bill_of_entry.partner_id.name,
                                bill_of_entry.state)
                        )
                advance_customs_vat_line = False
                for line in invoice.invoice_line_ids:
                    if line.advance_customs_vat:
                        advance_customs_vat_line = True
                        break
                boe_tax_rates = invoice.forwarder_bill_of_entry_ids.mapped(
                    "invoice_line_ids.invoice_line_tax_ids.amount")
                boe_amounts = invoice.forwarder_bill_of_entry_ids.mapped(
                    "amount_total")

                # In caso di dichiarazione d'intento inviata alla dogana,
                # la dogana non addebita IVA.
                # La bolla doganale ha righe positive e negative, il cui totale è 0
                if list(set(boe_amounts)) == [0.0]:
                    # Nessuna registrazione di storno è necessaria
                    continue

                if (
                    not advance_customs_vat_line
                    and list(set(boe_tax_rates)) != [0.0]
                ):
                    raise UserError(
                        _("Forwarder invoice %s does not have lines with "
                          "'Advance Customs Vat'")
                        % invoice.number)
                if not invoice.company_id.bill_of_entry_journal_id:
                    raise UserError(
                        _('No Bill of entry Storno journal configured')
                    )
                move_vals = {
                    'journal_id': (
                        invoice.company_id.bill_of_entry_journal_id.id),
                    'date': invoice.date_invoice,
                }
                move_lines = []
                for inv_line in invoice.invoice_line_ids:
                    if inv_line.advance_customs_vat:
                        line_vals = {
                            'name': _("Customs expenses"),
                            'account_id': inv_line.account_id.id,
                            'debit': 0.0,
                            'credit': inv_line.price_subtotal,
                            'partner_id': inv_line.partner_id.id,
                        }
                        if inv_line.product_id:
                            line_vals['product_id'] = inv_line.product_id.id
                        move_lines.append((0, 0, line_vals))
                for bill_of_entry in invoice.forwarder_bill_of_entry_ids:
                    line_vals = {
                        'name': _("Customs supplier"),
                        'account_id': bill_of_entry.account_id.id,
                        'debit': bill_of_entry.amount_total,
                        'credit': 0.0,
                        'partner_id': bill_of_entry.partner_id.id,
                    }
                    move_lines.append((0, 0, line_vals))
                    for boe_line in bill_of_entry.invoice_line_ids:
                        if boe_line.invoice_line_tax_ids:
                            if len(boe_line.invoice_line_tax_ids) > 1:
                                raise UserError(
                                    _("Can't handle more than 1 tax for line "
                                      "%s") % boe_line.name)

                        line_vals = {
                            'name': _("Extra UE expenses"),
                            'account_id': boe_line.account_id.id,
                            'debit': 0.0,
                            'credit': boe_line.price_subtotal,
                            'partner_id': boe_line.partner_id.id,
                        }
                        if boe_line.product_id:
                            line_vals['product_id'] = boe_line.product_id.id
                        move_lines.append((0, 0, line_vals))
                move_vals['line_ids'] = move_lines
                move = AccountMove.create(move_vals)
                move.action_post()
                invoice.write(
                    {'bill_of_entry_storno_id': move.id})

                reconcile_ids = []
                for move_line in move.line_ids:
                    for boe in invoice.forwarder_bill_of_entry_ids:
                        if (
                            move_line.account_id.id ==
                            boe.account_id.id
                        ):
                            reconcile_ids.append(move_line.id)
                            for boe_move_line in boe.move_id.line_ids:
                                if (
                                    boe_move_line.account_id.id ==
                                    boe.account_id.id
                                ):
                                    reconcile_ids.append(boe_move_line.id)

                AccountMoveLine.browse(reconcile_ids).reconcile()
        return res

    def action_cancel(self):
        res = super(AccountInvoice, self).action_cancel()
        for invoice in self:
            for boe in invoice.forwarder_bill_of_entry_ids:
                move = boe.move_id
                rec_lines = move.mapped('line_ids').filtered(
                    'full_reconcile_id'
                ).mapped('full_reconcile_id.reconciled_line_ids')
                rec_lines.remove_move_reconcile()
            if invoice.bill_of_entry_storno_id:
                invoice.bill_of_entry_storno_id.button_cancel()
                invoice.bill_of_entry_storno_id.unlink()
        return res

    def _check_no_taxes(self):
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids:
                raise (_("Extra UE supplier invoice must have no taxes"))

    def generate_bill_of_entry(self):
        self.ensure_one()
        if self.customs_doc_type != "supplier_invoice":
            raise UserError(_(
                "You can generate bill of entry from extra UE supplier invoice only"))
        if not self.company_id.bill_of_entry_tax_id:
            raise UserError(_(
                "Please set 'Bill of entry tax' in accounting configuration"))
        if not self.company_id.bill_of_entry_partner_id:
            raise UserError(_(
                "Please set 'Bill of entry partner' in accounting configuration"))
        self._check_no_taxes()
        boe_inv = self.copy(default={
            "partner_id": self.company_id.bill_of_entry_partner_id.id,
            "customs_doc_type": "bill_of_entry",
        })
        for line in boe_inv.invoice_line_ids:
            tax = self.company_id.bill_of_entry_tax_id
            if line.product_id.supplier_taxes_id:
                tax = line.product_id.supplier_taxes_id[0]
            line.invoice_line_tax_ids = [(6, 0, [tax.id])]
        boe_inv.supplier_invoice_ids = [(4, self.id)]
        boe_inv.compute_taxes()
        action = self.env.ref('account.action_vendor_bill_template').read()[0]
        form_view = [(self.env.ref('account.invoice_supplier_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [
                (state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = boe_inv.ids[0]
        return action


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    advance_customs_vat = fields.Boolean("Advance Customs Vat")
