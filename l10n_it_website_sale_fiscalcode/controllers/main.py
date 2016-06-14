# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_sale_partner_type.controllers.main \
    import WebsiteSalePartnerType


class WebsiteSaleFiscalCode(WebsiteSalePartnerType):

    def checkout_form_save(self, checkout):
        super(WebsiteSaleFiscalCode, self).checkout_form_save(
            checkout=checkout)
        partner_id = request.website.sale_get_order(
            context=request.context).partner_id
        partner_dict = {'fiscalcode': request.params['fiscalcode']}
        if request.params['partner_type'] == 'association':
            partner_dict['association'] = True
            partner_dict['is_company'] = True
        partner_id.write(partner_dict)

    def checkout_form_validate(self, data):
        res = super(WebsiteSaleFiscalCode, self).checkout_form_validate(
            data=data)
        partner_id = request.website.sale_get_order(
            context=request.context).partner_id
        partner_dict = {'fiscalcode': request.params['fiscalcode']}
        if request.params['partner_type'] == 'association':
            partner_dict['association'] = True
            partner_dict['is_company'] = True
        elif request.params['partner_type'] == 'individual':
            partner_dict['is_company'] = False
            partner_dict['association'] = False
        elif request.params['partner_type'] == 'company':
            partner_dict['association'] = False 
            partner_dict['is_company'] = True
        partner_id.write(partner_dict)
        if (request.params['partner_type'] == 'association' and
            not (request.params['fiscalcode'] or
                 request.params['vat'])):
            res['vat'] = 'error'
            res['fiscalcode'] = 'error'
        if (request.params['partner_type'] == 'company'
                and not request.params['fiscalcode']
                and not request.params['vat']):
            res['vat'] = 'error'
            res['fiscalcode'] = 'error'

        if (request.params['partner_type'] == 'individual'
                and not request.params['fiscalcode']):
            res['fiscalcode'] = 'error'
        return res

    def checkout_values(self, data=None):
        res = super(WebsiteSaleFiscalCode, self).checkout_values(
            data=data)
        cr, uid, context, registry = (
            request.cr, request.uid, request.context, request.registry)
        orm_user = registry.get('res.users')
        partner = orm_user.browse(
            cr, SUPERUSER_ID, uid, context).partner_id
        if partner.association:
            res['checkout']['partner_type'] = "association"
        if partner.fiscalcode:
            res['checkout']['fiscalcode'] = partner.fiscalcode
        return res
