# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import odoo.addons.decimal_precision as dp
from odoo.tools import float_is_zero
from odoo.tools.misc import formatLang


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

    name = fields.Char(required=True)
    sequence_id = fields.Many2one('ir.sequence', required=True)
    note = fields.Text(string='Note')
    default_carriage_condition_id = fields.Many2one(
        'stock.picking.carriage_condition',
        string='Default Carriage Condition')
    default_goods_description_id = fields.Many2one(
        'stock.picking.goods_description',
        string='Default Description of Goods')
    default_transportation_reason_id = fields.Many2one(
        'stock.picking.transportation_reason',
        string='Default Reason for Transportation')
    default_transportation_method_id = fields.Many2one(
        'stock.picking.transportation_method',
        string='Default Method of Transportation')
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=lambda self: self.env.user.company_id.id)


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'
    _rec_name = 'display_name'
    _order = 'date desc'

    @api.multi
    @api.depends('transportation_reason_id.to_be_invoiced')
    def _compute_to_be_invoiced(self):
        for ddt in self:
            ddt.to_be_invoiced = ddt.transportation_reason_id and \
                ddt.transportation_reason_id.to_be_invoiced or False

    def _default_ddt_type(self):
        return self.env['stock.ddt.type'].search([], limit=1)

    ddt_type_id = fields.Many2one(
        'stock.ddt.type', string='DdT Type', default=_default_ddt_type)
    ddt_number = fields.Char(string='DdT Number', copy=False)
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
    parcels = fields.Integer('Parcels')
    display_name = fields.Char(
        string='Name', compute='_compute_clean_display_name')
    volume = fields.Float('Volume')
    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', readonly=True, copy=False)
    to_be_invoiced = fields.Boolean(
        string='To be Invoiced', store=True, compute="_compute_to_be_invoiced",
        help="This depends on 'To be Invoiced' field of the Reason for "
             "Transportation of this DDT")
    show_price = fields.Boolean(string='Show prices on report')
    weight_manual = fields.Float(
        string="Force Net Weight",
        help="Fill this field with the value you want to be used as weight. "
             "Leave empty to let the system to compute it")
    gross_weight = fields.Float(string="Gross Weight")
    check_if_picking_done = fields.Boolean(
        compute='_compute_check_if_picking_done',
        )

    @api.multi
    @api.depends('picking_ids',
                 'picking_ids.state')
    def _compute_check_if_picking_done(self):
        for record in self:
            record.check_if_picking_done = False
            for picking in record.picking_ids:
                if picking.state == 'done':
                    record.check_if_picking_done = True

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        if self.ddt_type_id:
            addr = self.partner_id.address_get(['delivery', 'invoice'])
            self.partner_shipping_id = addr['delivery']
            self.carriage_condition_id = (
                self.partner_id.carriage_condition_id.id
                if self.partner_id.carriage_condition_id
                else self.ddt_type_id.default_carriage_condition_id)
            self.goods_description_id = (
                self.partner_id.goods_description_id.id
                if self.partner_id.goods_description_id
                else self.ddt_type_id.default_goods_description_id)
            self.transportation_reason_id = (
                self.partner_id.transportation_reason_id.id
                if self.partner_id.transportation_reason_id
                else self.ddt_type_id.default_transportation_reason_id)
            self.transportation_method_id = (
                self.partner_id.transportation_method_id.id
                if self.partner_id.transportation_method_id
                else self.ddt_type_id.default_transportation_method_id)
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
        # ----- Check if exist a stock picking whose state is 'done'
        for record_picking in self.picking_ids:
            if record_picking.state == 'done':
                raise UserError((
                    "Impossible to put in pack a picking whose state "
                    "is 'done'"))
        for package in self:
            # ----- Check if package has details
            if not package.line_ids:
                raise UserError(
                    _("Impossible to put in pack a package without details"))
            # ----- Assign ddt number if ddt type is set
            if package.ddt_type_id and not package.ddt_number:
                package.ddt_number = (
                    package.ddt_type_id.sequence_id.next_by_id())
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
                    package.ddt_type_id.sequence_id.next_by_id())
        self.write({'state': 'done', 'date_done': fields.Datetime.now()})
        return True

    @api.multi
    @api.depends(
        'name', 'ddt_number', 'partner_id.name', 'date'
    )
    def _compute_clean_display_name(self):
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
                 'package_id.quant_ids',
                 'picking_ids',
                 'picking_ids.move_lines',
                 'picking_ids.move_lines.quantity_done',
                 'weight_manual')
    def _compute_weight(self):
        super(StockPickingPackagePreparation, self)._compute_weight()
        for prep in self:
            if prep.weight_manual:
                prep.weight = prep.weight_manual
            elif not prep.package_id:
                stock_moves = []
                for picking in prep.picking_ids:
                    for move in picking.move_lines:
                        if move.quantity_done > 0:
                            stock_moves.append(move)
                weight = sum(sm.product_id.weight * sm.quantity_done
                             for sm in stock_moves)
                prep.net_weight = weight
                prep.weight = weight

    @api.multi
    def _get_sale_order_ref(self):
        """
        It returns the first sale order of the ddt.
        """
        self.ensure_one()
        sale_order = False
        for sm in self.picking_ids.mapped('move_lines'):
            if sm.sale_line_id:
                sale_order = sm.sale_line_id.order_id
                break
        return sale_order

    @api.multi
    def _prepare_invoice_description(self):
        invoice_description = ''
        lang = self.env['res.lang']._lang_get(self.env.lang)
        date_format = lang.date_format
        ddt_date_from = self._context.get('ddt_date_from', False)
        ddt_date_to = self._context.get('ddt_date_to', False)
        if ddt_date_from and ddt_date_to:
            invoice_description = '{} {} - {}'.format(
                _('Competenza:'),
                datetime.strptime(
                    ddt_date_from,
                    DEFAULT_SERVER_DATE_FORMAT).strftime(date_format),
                datetime.strptime(
                    ddt_date_to,
                    DEFAULT_SERVER_DATE_FORMAT).strftime(date_format)
            )
        return invoice_description

    @api.multi
    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order.
        This method may be
        overridden to implement custom invoice generation (making sure to call
        super() to establish
        a clean extension chain).
        """
        self.ensure_one()
        order = self._get_sale_order_ref()
        if order:
            # Most of the values will be overwritten below,
            # but this preserves inheritance chain
            res = order._prepare_invoice()
        else:
            # Initialise res with the fields in sale._prepare_invoice
            # that won't be overwritten below
            res = {
                'type': 'out_invoice',
                'partner_shipping_id':
                    self.partner_id.address_get(['delivery'])['delivery'],
                'company_id': self.company_id.id
            }
        journal_id = self._context.get('invoice_journal_id', False)
        if not journal_id:
            journal_id = self.env['account.invoice'].default_get(
                ['journal_id'])['journal_id']
        if not journal_id:
            raise UserError(
                _('Please define an accounting sale journal for this company.')
            )
        journal = self.env['account.journal'].browse(journal_id)
        invoice_partner_id = (
            order and order.partner_invoice_id.id or
            self.partner_id.address_get(['invoice'])['invoice'])
        invoice_partner = self.env['res.partner'].browse(invoice_partner_id)
        invoice_description = self._prepare_invoice_description()
        currency_id = (
            order and order.pricelist_id.currency_id.id or
            journal.currency_id.id or journal.company_id.currency_id.id)
        payment_term_id = (
            order and order.payment_term_id.id or
            self.partner_id.property_payment_term_id.id)
        fiscal_position_id = (
            order and order.fiscal_position_id.id or
            invoice_partner.property_account_position_id.id)
        res.update({
            'name': invoice_description or '',
            'origin': self.ddt_number,
            'date_invoice': self._context.get('invoice_date', False),
            'account_id': (
                invoice_partner.property_account_receivable_id.id),
            'partner_id': invoice_partner_id,
            'journal_id': journal_id,
            'currency_id': currency_id,
            'fiscal_position_id': fiscal_position_id,
            'payment_term_id': payment_term_id
        })
        # Now the rest of the fields dedicated to DDT
        res.update({
            'carriage_condition_id': self.carriage_condition_id.id,
            'goods_description_id': self.goods_description_id.id,
            'transportation_reason_id': self.transportation_reason_id.id,
            'transportation_method_id': self.transportation_method_id.id,
            'carrier_id': self.carrier_id.id,
            'parcels': self.parcels,
            'weight': self.weight,
            'gross_weight': self.gross_weight,
            'volume': self.volume,
        })
        return res

    @api.multi
    def action_invoice_create(self):
        """
        Create the invoice associated to the DDT.
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        invoices = {}
        references = {}
        for ddt in self:
            if not ddt.to_be_invoiced or ddt.invoice_id:
                continue
            order = ddt._get_sale_order_ref()

            if order:
                group_method = (
                    order and order.ddt_invoicing_group or 'shipping_partner')
                group_partner_invoice_id = order.partner_invoice_id.id
                group_currency_id = order.currency_id.id
            else:
                group_method = ddt.partner_shipping_id.ddt_invoicing_group
                group_partner_invoice_id = ddt.partner_id.id
                group_currency_id = ddt.partner_id.currency_id.id

            if group_method == 'billing_partner':
                group_key = (group_partner_invoice_id,
                             group_currency_id)
            elif group_method == 'shipping_partner':
                group_key = (ddt.partner_shipping_id.id,
                             ddt.company_id.currency_id.id)
            elif group_method == 'code_group':
                group_key = (ddt.partner_shipping_id.ddt_code_group,
                             group_partner_invoice_id)
            else:
                group_key = ddt.id

            for line in ddt.line_ids:
                if group_key not in invoices:
                    inv_data = ddt._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = ddt
                    invoices[group_key] = invoice
                    ddt.invoice_id = invoice.id
                elif group_key in invoices:
                    vals = {}

                    origin = invoices[group_key].origin
                    if origin and ddt.ddt_number not in origin.split(', '):
                        vals['origin'] = invoices[
                            group_key].origin + ', ' + ddt.ddt_number
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

        for invoice in list(invoices.values()):
            if not invoice.name:
                invoice.write({
                    'name': invoice.origin
                })
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
            # Necessary to force computation of taxes. In account_invoice,
            # they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice.message_post_with_view(
                'mail.message_origin_link',
                values={
                    'self': invoice, 'origin': references[invoice]},
                subtype_id=self.env.ref('mail.mt_note').id)
        return [inv.id for inv in list(invoices.values())]

    @api.multi
    def action_send_ddt_mail(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.\
                get_object_reference('l10n_it_ddt',
                                     'email_template_edi_ddt')[1]
        except ValueError:
            template_id = False

        try:
            compose_form_id = ir_model_data.\
                get_object_reference('mail',
                                     'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'stock.picking.package.preparation',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'mark_so_as_sent': True,
            'custom_layout':
                "l10n_it_ddt.mail_template_data_notification_email_ddt"
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

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
        related='move_id.sale_line_id',
        string='Sale order line',
        store=True, readonly=True)
    price_unit = fields.Float('Unit Price', digits=dp.get_precision(
        'Product Price'), default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    discount = fields.Float(
        string='Discount (%)', digits=dp.get_precision('Discount'),
        default=0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        super(StockPickingPackagePreparationLine, self)._onchange_product_id()
        if self.product_id:
            order = self.package_preparation_id._get_sale_order_ref()
            partner = order and order.partner_id \
                or self.package_preparation_id.partner_id
            product = self.product_id.with_context(
                lang=self.package_preparation_id.partner_id.lang,
                partner=partner.id,
                quantity=self.product_uom_qty,
                date=self.package_preparation_id.date,
                pricelist=order and order.pricelist_id.id or False,
                uom=self.product_uom_id.id
            )
            # Tax
            taxes = product.taxes_id
            fpos = order and order.fiscal_position_id or \
                self.package_preparation_id.partner_id.\
                property_account_position_id
            self.tax_ids = fpos.map_tax(
                taxes, product, partner) if fpos else taxes
            # Price and discount
            self.price_unit = product.price
            if order:
                context_partner = dict(
                    self.env.context, partner_id=partner.id)
                pricelist_context = dict(
                    context_partner, uom=self.product_uom_id.id,
                    date=order.date_order)
                price, rule_id = order.pricelist_id.with_context(
                    pricelist_context).get_product_price_rule(
                    product, self.product_uom_qty or 1.0, partner)
                new_list_price, currency_id = self.env['sale.order.line']\
                    .with_context(context_partner)._get_real_price_currency(
                    self.product_id, rule_id, self.product_uom_qty,
                    self.product_uom_id, order.pricelist_id.id)
                datas = self._prepare_price_discount(new_list_price, rule_id)
                for key in list(datas.keys()):
                    setattr(self, key, datas[key])

    @api.model
    def _prepare_price_discount(self, price, rule_id):
        """
        Use this method for other fields added in the line.
        Use key of dict to specify the field that will be updated
        """
        res = {
            'price_unit': price
        }
        # Discount
        if rule_id:
            rule = self.env['product.pricelist.item'].browse(rule_id)
            if rule.pricelist_id.discount_policy == \
                    'without_discount':
                res['discount'] = rule.price_discount
        return res

    @api.model
    def _prepare_lines_from_pickings(self, picking_ids):
        """
        Add values used for invoice creation
        """
        lines = super(StockPickingPackagePreparationLine, self). \
            _prepare_lines_from_pickings(picking_ids)
        for line in lines:
            sale_line = False
            if line['move_id']:
                move = self.env['stock.move'].browse(line['move_id'])
                sale_line = move.sale_line_id or False
            if sale_line:
                line['price_unit'] = sale_line.price_unit or 0
                line['discount'] = sale_line.discount or 0
                line['tax_ids'] = [(6, 0, [x.id]) for x in sale_line.tax_id]
        return lines

    @api.multi
    def _prepare_invoice_line(self, qty, invoice_id=None):
        """
        Prepare the dict of values to create the new invoice line for a
        ddt line.

        :param qty: float quantity to invoice
        :param invoice_id: possible existing invoice
        """
        self.ensure_one()
        res = {}
        if (
            self.sale_line_id.product_id.property_account_income_id or
            self.sale_line_id.product_id.categ_id.
            property_account_income_categ_id
        ):
            # Without property_account_income_id or
            # property_account_income_categ_id
            # _prepare_invoice_line would fail
            res = self.sale_line_id._prepare_invoice_line(qty)
        else:
            account = (
                self.product_id.property_account_income_id or
                self.product_id.categ_id.property_account_income_categ_id)
            if not account:
                if invoice_id:
                    invoice = self.env['account.invoice'].browse(invoice_id)
                    account = invoice.journal_id.default_credit_account_id
            if not account:
                raise UserError(
                    _(
                        'Please define income account for this product: "%s" '
                        '(id:%d) - or for its category: "%s".'
                    ) % (
                        self.product_id.name, self.product_id.id,
                        self.product_id.categ_id.name
                    )
                )
            fpos = None
            if self.sale_line_id:
                fpos = (
                    self.sale_line_id.order_id.fiscal_position_id or
                    self.sale_line_id.order_id.partner_id.
                    property_account_position_id
                )
            if fpos:
                account = fpos.map_account(account)
            res['account_id'] = account.id

            if self.sale_line_id.order_id.analytic_account_id:
                res[
                    'account_analytic_id'
                ] = self.sale_line_id.order_id.analytic_account_id.id
            if self.sale_line_id.analytic_tag_ids:
                res['analytic_tag_ids'] = [
                    (6, 0, self.sale_line_id.analytic_tag_ids.ids)
                ]

        res.update({
            'ddt_line_id': self.id,
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.package_preparation_id.name or '',
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom_id.id,
            'product_id': self.product_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_ids.ids)],
        })
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
                vals = line._prepare_invoice_line(
                    qty=qty, invoice_id=invoice_id)
                vals.update({'invoice_id': invoice_id})
                if line.sale_line_id:
                    vals.update(
                        {'sale_line_ids': [
                            (6, 0, [line.sale_line_id.id])
                        ]})
                self.env['account.invoice.line'].with_context(
                    skip_update_line_ids=True).create(vals)

    @api.multi
    def quantity_by_lot(self):
        """Build a dictionary mapping each lot in the current line
        to its quantity (if the product is tracked with lots)"""
        self.ensure_one()
        res = {}
        for quant in self.lot_ids.mapped('quant_ids'):
            if quant.location_id == self.move_id.location_dest_id:
                if quant.lot_id not in res:
                    res[quant.lot_id] = quant.quantity
                else:
                    res[quant.lot_id] += quant.quantity
        for lot in res:
            if lot.product_id.tracking == 'lot':
                res[lot] = formatLang(self.env, res[lot])
            else:
                # If not tracking by lots, quantity is not relevant
                res[lot] = False
        return res
