# -*- coding: utf-8 -*-


from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ddt_invoice_exclude = fields.Boolean(
        string='Exclude from DDT invoicing',
        help="If flagged this service will not be automatically "
             "invoiced from DDT.")


class ResPartner(models.Model):
    _inherit = "res.partner"

    ddt_invoice_exclude = fields.Boolean(
        string='Exclude from DDT invoicing',
        help="If flagged this service will not be automatically "
             "invoiced from DDT. If set on the partner, this parameter will"
             "be automatically applied to Sale Orders.")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ddt_invoice_exclude = fields.Boolean(
        string='Exclude from DDT invoicing',
        help="If flagged this service will not be automatically "
             "invoiced from DDT. This parameter can be set on partners and "
             "automatically applied to Sale Orders.")

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.ddt_invoice_exclude = (
                self.partner_id.ddt_invoice_exclude)
        return result
