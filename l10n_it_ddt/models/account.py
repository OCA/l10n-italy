# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

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
    carrier_tracking_ref = fields.Char(string='Tracking Reference', copy=False)
    dimension = fields.Char()
    parcels = fields.Integer('Parcels')
    weight = fields.Float(string="Weight")
    gross_weight = fields.Float(string="Gross Weight")
    volume = fields.Float('Volume')
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
    ddt_ids = fields.One2many(
        'stock.picking.package.preparation', 'invoice_id', string='TD')

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        if self.env.context.get('skip_onchange_partner_id'):
            return res
        if self.partner_id:
            self.carriage_condition_id = (
                self.partner_id.carriage_condition_id.id)
            self.goods_description_id = self.partner_id.goods_description_id.id
            self.transportation_reason_id = (
                self.partner_id.transportation_reason_id.id)
            self.transportation_method_id = (
                self.partner_id.transportation_method_id.id)
        return res


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    ddt_id = fields.Many2one(
        'stock.picking.package.preparation', string='TD',
        related='ddt_line_id.package_preparation_id', store=True)
    ddt_line_id = fields.Many2one(
        'stock.picking.package.preparation.line', string='TD line')
    ddt_sequence = fields.Integer(
        string='TD sequence', related='ddt_line_id.sequence', store=True)
