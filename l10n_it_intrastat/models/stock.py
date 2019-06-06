# -*- coding: utf-8 -*-
#
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
#


from openerp import models, fields, api


class stock_picking(models.Model):

    _inherit = "stock.picking"

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move, context=None):

        res = super(stock_picking, self)._get_invoice_vals(
            key, inv_type, journal_id, move)

        partner, currency_id, company_id, user_id = key

        res['intrastat'] = partner.property_account_position.intrastat

        return res
