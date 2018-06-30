# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSaleFiscalCode(website_sale):

    def checkout_form_save(self, checkout):
        super(WebsiteSaleFiscalCode, self).checkout_form_save(
            checkout=checkout)
        partner_id = request.website.sale_get_order(
            context=request.context).partner_id
        partner_dict = {'fiscalcode': request.params['fiscalcode']}
        partner_id.write(partner_dict)

    def checkout_values(self, data=None):
        res = super(WebsiteSaleFiscalCode, self).checkout_values(
            data=data)
        cr, uid, context, registry = (
            request.cr, request.uid, request.context, request.registry)
        orm_user = registry.get('res.users')
        partner = orm_user.browse(
            cr, SUPERUSER_ID, uid, context).partner_id
        if data and 'fiscalcode' in data:
            res['checkout']['fiscalcode'] = data['fiscalcode']
        else:
            res['checkout']['fiscalcode'] = partner.fiscalcode
        return res
