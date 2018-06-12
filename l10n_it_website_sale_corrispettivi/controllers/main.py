# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCorrispettivi(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        res = super(WebsiteSaleCorrispettivi, self) \
            ._checkout_form_save(mode, checkout, all_values)
        use_invoice = all_values.get('use_invoice')
        # Update order
        order = request.website.sale_get_order()
        order_values = \
            self._prepare_corrispettivi_order_values(order, use_invoice)
        order.write(order_values)

        # Update partner
        partner = request.env['res.partner'].browse(res)
        partner_values = \
            self._prepare_corrispettivi_partner_values(partner, use_invoice)
        partner.sudo().write(partner_values)
        return res

    def _prepare_corrispettivi_partner_values(self, partner, use_invoice):
        partner_values = {'use_corrispettivi': not use_invoice}
        if not partner.property_account_position_id:
            # No fiscal position: assign a corrispettivi fiscal position
            # if requested
            if not use_invoice:
                company = partner.company_id or \
                    partner.default_get(['company_id'])['company_id']
                partner_values['property_account_position_id'] = \
                    request.env['account.fiscal.position'] \
                    .get_corr_fiscal_pos(company).id
        else:
            # There is a fiscal position:
            # remove it only if it is a corrispettivi one
            # and user doesn't want to use corrispettivi
            if use_invoice:
                if partner.property_account_position_id.corrispettivi:
                    partner_values['property_account_position_id'] = False
        return partner_values

    def _prepare_corrispettivi_order_values(self, order, use_invoice):
        order_values = {'corrispettivi': not use_invoice}
        if not order.fiscal_position_id:
            # No fiscal position: assign a corrispettivi fiscal position
            # if requested
            if not use_invoice:
                company = order.company_id or \
                    order.default_get(['company_id'])['company_id']
                order_values['fiscal_position_id'] = \
                    request.env['account.fiscal.position'] \
                    .get_corr_fiscal_pos(company).id
        else:
            # There is a fiscal position:
            # remove it only if it is a corrispettivi one
            # and user doesn't want to use corrispettivi
            if use_invoice:
                if order.fiscal_position_id.corrispettivi:
                    order_values['fiscal_position_id'] = False
        return order_values
