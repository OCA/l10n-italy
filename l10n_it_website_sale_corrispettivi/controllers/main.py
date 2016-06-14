# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.website_sale.controllers.main import website_sale
from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.addons.l10n_it_website_sale_fiscalcode.controllers.main \
    import WebsiteSaleFiscalCode


class WebsiteSale(website_sale):

    def checkout_form_save(self, checkout):
        res = super(WebsiteSale, self).checkout_form_save(checkout)
        if checkout.get('invoice_or_receipt') == 'receipt':
            cr, context, = request.cr, request.context
            order = request.website.sale_get_order(context=context)
            order_obj = request.registry.get('sale.order')
            order_obj.write(
                cr, SUPERUSER_ID, [order.id], {'corrispettivo': True},
                context=context)
        return res

    def checkout_values(self, data=None):
        res = super(WebsiteSale, self).checkout_values(data=data)
        if data and data.get('invoice_or_receipt'):
            res['checkout']['invoice_or_receipt'] = data['invoice_or_receipt']
        return res


class WebsiteSaleFiscalCode(WebsiteSaleFiscalCode):

    def checkout_form_validate(self, data):
        res = super(WebsiteSaleFiscalCode, self).checkout_form_validate(
            data=data)
        if (request.params['invoice_or_receipt'] == 'receipt' and
                request.params['partner_type'] == 'individual' and not (
                request.params['fiscalcode'])):
            res['fiscalcode'] = ''
        return res
