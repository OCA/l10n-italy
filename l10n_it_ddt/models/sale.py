# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api

TD_INVOICING_GROUPS = [('nothing', 'One TD - One Invoice'),
                       ('billing_partner', 'Billing Partner'),
                       ('shipping_partner', 'Shipping Partner'),
                       ('code_group', 'Code group')]


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.multi
    def _compute_ddt_ids(self):
        for so in self:
            so.ddt_ids = so.mapped('picking_ids.ddt_ids').ids

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
    ddt_carrier_id = fields.Many2one(
        'res.partner', string='Carrier')
    parcels = fields.Integer('Parcels')
    weight = fields.Float(string="Weight")
    gross_weight = fields.Float(string="Gross Weight")
    volume = fields.Float('Volume')
    ddt_ids = fields.Many2many(
        'stock.picking.package.preparation',
        string='Related TDs',
        compute='_compute_ddt_ids')
    create_ddt = fields.Boolean('Automatically create the TD')
    ddt_invoicing_group = fields.Selection(
        TD_INVOICING_GROUPS, 'TD invoicing group',
        default='billing_partner',
        required=True,
    )
    ddt_show_price = fields.Boolean(
        string='TD show prices', help='Show prices and discounts in TD report')
    ddt_invoice_exclude = fields.Boolean(
        string='DDT do not invoice services',
        help="If flagged services from this SO will not be automatically "
             "invoiced from DDT. This parameter can be set on partners and "
             "automatically applied to Sale Orders.")

    weight_manual_uom_id = fields.Many2one(
        'uom.uom', 'Net Weight UoM',
        default=lambda self: self.env.ref(
            'uom.product_uom_kgm', raise_if_not_found=False))
    gross_weight_uom_id = fields.Many2one(
        'uom.uom', 'Gross Weight UoM',
        default=lambda self: self.env.ref(
            'uom.product_uom_kgm', raise_if_not_found=False))
    volume_uom_id = fields.Many2one(
        'uom.uom', 'Volume UoM',
        default=lambda self: self.env.ref(
            'uom.product_uom_litre', raise_if_not_found=False))

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.carriage_condition_id = (
                self.partner_id.carriage_condition_id.id)
            self.goods_description_id = self.partner_id.goods_description_id.id
            self.transportation_reason_id = (
                self.partner_id.transportation_reason_id.id)
            self.transportation_method_id = (
                self.partner_id.transportation_method_id.id)
            self.ddt_invoicing_group = (
                self.partner_id.ddt_invoicing_group)
            self.ddt_invoice_exclude = (
                self.partner_id.ddt_invoice_exclude)
            self.ddt_show_price = self.partner_id.ddt_show_price
        return result

    @api.multi
    def _prepare_invoice(self):
        vals = super(SaleOrder, self)._prepare_invoice()
        vals.update({
            'carriage_condition_id': self.carriage_condition_id.id,
            'goods_description_id': self.goods_description_id.id,
            'transportation_reason_id': self.transportation_reason_id.id,
            'transportation_method_id': self.transportation_method_id.id,
            'carrier_id': self.ddt_carrier_id.id,
            'parcels': self.parcels,
            'weight': self.weight,
            'gross_weight': self.gross_weight,
            'volume': self.volume,
            'weight_manual_uom_id': self.weight_manual_uom_id.id,
            'gross_weight_uom_id': self.gross_weight_uom_id.id,
            'volume_uom_id': self.volume_uom_id.id,
        })
        return vals

    def _preparare_ddt_data(self):
        picking_ids = self.picking_ids.ids
        return {
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'carriage_condition_id': self.carriage_condition_id.id,
            'goods_description_id': self.goods_description_id.id,
            'transportation_reason_id':
            self.transportation_reason_id.id,
            'to_be_invoiced': self.transportation_reason_id.to_be_invoiced,
            'transportation_method_id':
            self.transportation_method_id.id,
            'carrier_id': self.ddt_carrier_id.id,
            'parcels': self.parcels,
            'weight_manual': self.weight,
            'gross_weight': self.gross_weight,
            'volume': self.volume,
            'picking_ids': [(6, 0, picking_ids)],
            'ddt_show_price': self.ddt_show_price,
        }

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        ddt_model = self.env['stock.picking.package.preparation']
        for order in self:
            if order.create_ddt:
                ddt_data = order._preparare_ddt_data()
                ddt_model.create(ddt_data)
        return res

    @api.multi
    def action_view_ddt(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']

        result = mod_obj.get_object_reference(
            'stock_picking_package_preparation',
            'action_stock_picking_package_preparation')
        ddt_id = result and result[1] or False
        result = act_obj.browse(ddt_id).read()[0]

        ddt_ids = []
        for so in self:
            ddt_ids += [ddt.id for ddt in so.ddt_ids]

        if len(ddt_ids) > 1:
            result['domain'] = "[('id','in',[" + ','.join(
                map(str, ddt_ids)) + "])]"
        else:
            res = mod_obj.get_object_reference(
                'stock_picking_package_preparation',
                'stock_picking_package_preparation_form')
            result['views'] = [(res and res[1] or False, 'form')]
            result['res_id'] = ddt_ids and ddt_ids[0] or False
        return result

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        return super(SaleOrder, self.with_context(
            skip_onchange_partner_id=True
        )).action_invoice_create(grouped, final)
