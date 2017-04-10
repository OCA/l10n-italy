# -*- coding: utf-8 -*-
# Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError

from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

import odoo.addons.decimal_precision as dp


class StockPickingCarriageCondition(models.Model):

    _name = "stock.picking.carriage_condition"
    _description = "Carriage Condition"

    name = fields.Char(string='Carriage Condition', required=True)
    note = fields.Text(string='Note')


class StockPickingGoodsDescription(models.Model):

    _name = 'stock.picking.goods_description'
    _description = "Description of Goods"

    name = fields.Char(string='Description of Goods', required=True)
    note = fields.Text(string='Note')


class StockPickingTransportationReason(models.Model):

    _name = 'stock.picking.transportation_reason'
    _description = 'Reason for Transportation'

    name = fields.Char(string='Reason For Transportation', required=True)
    note = fields.Text(string='Note')
    to_be_invoiced = fields.Boolean(string='To be Invoiced')


class StockPickingTransportationMethod(models.Model):

    _name = 'stock.picking.transportation_method'
    _description = 'Method of Transportation'

    name = fields.Char(string='Method of Transportation', required=True)
    note = fields.Text(string='Note')


class StockDdtType(models.Model):

    _name = 'stock.ddt.type'
    _description = 'Stock DdT Type'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    sequence_id = fields.Many2one('ir.sequence', required=True)
    note = fields.Text(string='Note')


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'
    _rec_name = 'display_name'
    _order = 'date desc'

    @api.multi
    @api.depends('transportation_reason_id')
    def _compute_to_be_invoiced(self):
        for ddt in self:
            ddt.to_be_invoiced = ddt.transportation_reason_id and \
                ddt.transportation_reason_id.to_be_invoiced or False

    def _default_ddt_type(self):
        return self.env['stock.ddt.type'].search([], limit=1)

    ddt_type_id = fields.Many2one(
        'stock.ddt.type', string='DdT Type', default=_default_ddt_type)
    ddt_number = fields.Char(string='DdT Number')
    partner_shipping_id = fields.Many2one(
        'res.partner', string="Shipping Address")
    carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition', string='Carriage Condition')
    goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Description of Goods')
    transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Reason for Transportation')
    transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Method of Transportation')
    carrier_id = fields.Many2one(
        'res.partner', string='Carrier')
    parcels = fields.Integer()
    display_name = fields.Char(string='Name', compute='_compute_display_name')
    volume = fields.Float('Volume')
    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', readonly=True)
    to_be_invoiced = fields.Boolean(
        string='To be Invoiced', store=True, compute="_compute_to_be_invoiced")
    show_price = fields.Boolean(string='Show prices on report')

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        if self.ddt_type_id:
            addr = self.partner_id.address_get(['delivery', 'invoice'])
            self.partner_shipping_id = addr['delivery']
            self.carriage_condition_id = \
                self.partner_id.carriage_condition_id.id \
                if self.partner_id.carriage_condition_id else False
            self.goods_description_id = \
                self.partner_id.goods_description_id.id \
                if self.partner_id.goods_description_id else False
            self.transportation_reason_id = \
                self.partner_id.transportation_reason_id.id \
                if self.partner_id.transportation_reason_id else False
            self.transportation_method_id = \
                self.partner_id.transportation_method_id.id \
                if self.partner_id.transportation_method_id else False
            self.show_price = self.partner_id.ddt_show_price

    @api.model
    def check_linked_picking(self, picking):
        ddt = self.search([('picking_ids', '=', picking.id)])
        if ddt:
            raise UserError(
                _("Selected Picking is already linked to DDT: %s")
                % ddt.display_name
            )

    @api.multi
    def action_put_in_pack(self):
        for package in self:
            # ----- Check if package has details
            if not package.line_ids:
                raise UserError(
                    _("Impossible to put in pack a package without details"))
            # ----- Assign ddt number if ddt type is set
            if package.ddt_type_id and not package.ddt_number:
                package.ddt_number = (
                    package.ddt_type_id.sequence_id.next_by_code(
                        package.ddt_type_id.sequence_id.code))
        return super(StockPickingPackagePreparation, self).action_put_in_pack()

    @api.multi
    def set_done(self):
        for picking in self.picking_ids:
            if picking.state != 'done':
                raise UserError(
                    _("Not every picking is in done status"))
        for package in self:
            if not package.ddt_number:
                package.ddt_number = (
                    package.ddt_type_id.sequence_id.next_by_code(
                        package.ddt_type_id.sequence_id.code))
        self.write({'state': 'done', 'date_done': fields.Datetime.now()})
        return True

    @api.multi
    def _compute_display_name(self):
        for prep in self:
            name = u''
            if prep.name:
                name = prep.name
            if prep.ddt_number and prep.name:
                name = u'[%s] %s' % (prep.name, prep.ddt_number)
            if prep.ddt_number and not prep.name:
                name = prep.ddt_number
            if not name:
                name = u'%s - %s' % (prep.partner_id.name, prep.date)
            prep.display_name = name

    @api.multi
    @api.depends('package_id',
                 'package_id.children_ids',
                 'package_id.quant_ids',
                 'picking_ids',
                 'picking_ids.move_lines',
                 'picking_ids.move_lines.quant_ids')
    def _compute_weight(self):
        super(StockPickingPackagePreparation, self)._compute_weight()
        for prep in self:
            if not prep.package_id:
                quants = self.env['stock.quant']
                for picking in prep.picking_ids:
                    for line in picking.move_lines:
                        for quant in line.quant_ids:
                            if quant.qty >= 0:
                                quants |= quant
                weight = sum(l.product_id.weight * l.qty for l in quants)
                prep.net_weight = weight
                prep.weight = weight

    def _get_sale_order_ref(self):
        """
        It returns the first sale order of the ddt.
        """
        sale_order = False
        for picking in self.picking_ids:
            for sm in picking.move_lines:
                if sm.procurement_id and sm.procurement_id.sale_line_id:
                    sale_order = sm.procurement_id.sale_line_id.order_id
                    return sale_order
        return sale_order

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        order = self._get_sale_order_ref()
        journal_id = self.env['account.invoice'].default_get(
            ['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(
                _('Please define an accounting sale journal for this company.'))
        invoice_vals = {
            # 'name': self.client_order_ref or '',
            # 'origin': self.name,
            'name': self.ddt_number or '',
            'origin': self.ddt_number,
            'type': 'out_invoice',
            'account_id': order.partner_invoice_id.property_account_receivable_id.id,
            'partner_id': order.partner_invoice_id.id,
            'partner_shipping_id': self.partner_id.id,
            'journal_id': journal_id,
            'currency_id': order.pricelist_id.currency_id.id,
            # TO DO 'comment': self.note,
            'payment_term_id': order.payment_term_id.id,
            'fiscal_position_id': order.fiscal_position_id.id or self.partner_invoice_id.property_account_position_id.id,
            'company_id': self.company_id.id,
            'user_id': order.user_id and self.user_id.id,
            'team_id': order.team_id.id
        }
        return invoice_vals

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        invoices = {}
        references = {}
        for ddt in self:
            if not ddt.to_be_invoiced or ddt.invoice_id:
                continue
            order = ddt._get_sale_order_ref()

            group_method = order.ddt_invoicing_group or 'shipping_partner'

            if group_method == 'billing_partner':
                group_key = (order.partner_invoice_id.id, order.currency_id.id)
            elif group_method == 'shipping_partner':
                group_key = (ddt.partner_id.id, ddt.company_id.currency_id.id)
            elif group_method == 'code_group':
                group_key = (ddt.partner_id.ddt_code_group)
            else:
                group_key = ddt.id

            for line in ddt.line_ids:
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = ddt
                    invoices[group_key] = invoice
                    ddt.invoice_id = invoice.id
                elif group_key in invoices:
                    vals = {}

                    if ddt.ddt_number not in invoices[group_key].origin.split(', '):
                        vals['origin'] = invoices[
                            group_key].origin + ', ' + ddt.ddt_number
                    """
                    if order.client_order_ref and order.client_order_ref not in invoices[group_key].name.split(', '):
                        vals['name'] = invoices[group_key].name + \
                            ', ' + order.client_order_ref"""
                    invoices[group_key].write(vals)
                    ddt.invoice_id = invoices[group_key].id

                if line.product_uom_qty > 0:
                    line.invoice_line_create(
                        invoices[group_key].id, line.product_uom_qty)
            if references.get(invoices.get(group_key)):
                if ddt not in references[invoices[group_key]]:
                    references[invoice] = references[invoice] | ddt

        if not invoices:
            raise UserError(_('There is no invoicable line.'))

        for invoice in invoices.values():
            if not invoice.invoice_line_ids:
                raise UserError(_('There is no invoicable line.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_untaxed < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={
                                               'self': invoice, 'origin': references[invoice]},
                                           subtype_id=self.env.ref('mail.mt_note').id)
        return [inv.id for inv in invoices.values()]

    @api.multi
    def unlink(self):
        for ddt in self:
            if ddt.invoice_id:
                raise UserError(
                    _("Document {d} has invoice linked".format(
                        d=ddt.ddt_number)))
        return super(StockPickingPackagePreparation, self).unlink()


class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'

    sale_line_id = fields.Many2one(
        related='move_id.procurement_id.sale_line_id', string='Company',
        store=True, readonly=True)
    price_unit = fields.Float('Unit Price', digits=dp.get_precision(
        'Product Price'), default=0.0)
    tax_id = fields.Many2many('account.tax', string='Taxes', domain=[
                              '|', ('active', '=', False),
                              ('active', '=', True)])
    discount = fields.Float(
        string='Discount (%)', digits=dp.get_precision('Discount'),
        default=0.0)

    @api.model
    def _prepare_lines_from_pickings(self, picking_ids):
        """
        Add values used for invoice creation
        """
        lines = super(StockPickingPackagePreparationLine, self).\
            _prepare_lines_from_pickings(picking_ids)
        for line in lines:
            sale_line = False
            if line['move_id']:
                move = self.env['stock.move'].browse(line['move_id'])
                sale_line = move.procurement_id.sale_line_id or False
            if sale_line:
                line['price_unit'] = sale_line.price_unit or 0
                line['discount'] = sale_line.discount or 0
                line['tax_id'] = [(6, 0, [x.id]) for x in sale_line.tax_id]
        return lines

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a ddt line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                            (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.sale_line_id.order_id.fiscal_position_id or\
            self.sale_line_id.order_id.partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)

        res = {
            'ddt_id': self.package_preparation_id.id,
            'ddt_line_id': self.id,
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.sale_line_id.order_id.name or '',
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom_id.id,
            'product_id': self.product_id.id or False,
            # 'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.sale_line_id.order_id.project_id.id or False,
            'analytic_tag_ids': [(6, 0, self.sale_line_id.analytic_tag_ids.ids)],
        }
        return res

    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        """
        :param invoice_id: integer
        :param qty: float quantity to invoice
        """
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = line._prepare_invoice_line(qty=qty)
                if line.sale_line_id:
                    vals.update(
                        {'invoice_id': invoice_id, 'sale_line_ids': [(6, 0, [line.sale_line_id.id])]})
                self.env['account.invoice.line'].create(vals)
