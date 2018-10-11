# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleCorrispettivi(WebsiteSale):

    def _checkout_form_save(self, mode, checkout, all_values):
        partner_id = super(WebsiteSaleCorrispettivi, self) \
            ._checkout_form_save(mode, checkout, all_values)
        use_invoice = all_values.get('use_invoice')

        order = request.website.sale_get_order()
        # Update the order, note that has already been retrieved using sudo()
        if order:
            order_values = self._prepare_corrispettivi_order_values(
                order, use_invoice)
            order.sudo().write(order_values)

        # Update the partner that has been created by the checkout form
        partner = request.env['res.partner'].sudo().browse(partner_id)
        partner_values = self._prepare_corrispettivi_partner_values(
            partner, use_invoice)
        partner.write(partner_values)
        return partner_id

    def _prepare_corrispettivi_partner_values(self, partner, use_invoice):
        """
        :param partner: current partner, retrieved using sudo
        :param use_invoice: if we have to use invoice or corrispettivi
          fiscal position
        """
        partner_values = {'use_corrispettivi': not use_invoice}
        if not partner.property_account_position_id:
            # No fiscal position: assign a corrispettivi fiscal position
            # if requested
            if not use_invoice:
                company = partner.company_id
                partner_values['property_account_position_id'] = \
                    request.env['account.fiscal.position'] \
                    .sudo().get_corr_fiscal_pos(company).id
        else:
            # There is a fiscal position:
            # remove it only if it is a corrispettivi one
            # and user doesn't want to use corrispettivi
            if use_invoice:
                if partner.property_account_position_id.corrispettivi:
                    partner_values['property_account_position_id'] = False
        return partner_values

    def _prepare_corrispettivi_order_values(self, order, use_invoice):
        """
        :param order: current order, retrieved using sudo
        :param use_invoice: if we have to use invoice or corrispettivi
          fiscal position
        """
        order_values = {'corrispettivi': not use_invoice}
        if not order.fiscal_position_id:
            # No fiscal position: assign a corrispettivi fiscal position
            # if requested
            if not use_invoice:
                company = order.company_id
                order_values['fiscal_position_id'] = \
                    request.env['account.fiscal.position'] \
                    .sudo().get_corr_fiscal_pos(company).id
        else:
            # There is a fiscal position:
            # remove it only if it is a corrispettivi one
            # and user doesn't want to use corrispettivi
            if use_invoice:
                if order.fiscal_position_id.corrispettivi:
                    order_values['fiscal_position_id'] = False
        return order_values
