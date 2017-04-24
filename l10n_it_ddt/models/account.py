# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Abstract (http://www.abstract.it)
#    @author Davide Corio <davide.corio@abstract.it>
#    Copyright (C) 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


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
    parcels = fields.Integer('Parcels')
    weight = fields.Float(string="Weight")
    volume = fields.Float('Volume')
    ddt_ids = fields.One2many(
        'stock.picking.package.preparation', 'invoice_id', string='DDT')

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
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
        'stock.picking.package.preparation', string='Ddt',
        related='ddt_line_id.package_preparation_id', store=True)
    ddt_line_id = fields.Many2one(
        'stock.picking.package.preparation.line', string='Ddt line')
    ddt_sequence = fields.Integer(
        string='Ddt sequence', related='ddt_line_id.sequence', store=True)
