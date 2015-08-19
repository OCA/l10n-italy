# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@openforce.it)
#    Copyright (C) 2015
#    Apulia Software srl - info@apuliasoftware.it - www.apuliasoftware.it
#    Openforce di Camilli Alessandro - www.openforce.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class res_company(models.Model):
    _inherit = 'res.company'
    
    intrastat_uom_kg_id = fields.Many2one(
        'product.uom', string="Unit of measure for Kg",
        )
    intrastat_ua_code = fields.Char(string="User ID (UA Code)", size=4)
    intrastat_delegated_vat = fields.Char(string="Delegated person VAT",
                                          size=16)
    intrastat_delegated_name = fields.Char(string="Delegated person", size=255)
    intrastat_export_file_name = fields.Char(string="File name for export")

    ### default values sale section
    intrastat_sale_statistic_amount = fields.Integer(
        string='Statistic Amount Euro', digits=dp.get_precision('Account'))
    intrastat_sale_transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_sale_delivery_code_id = fields.Many2one(
        'stock.incoterms', string='Delivery')
    intrastat_sale_transport_code_id = fields.Many2one(
        'account.intrastat.transport', string='Transport')
    #intrastat_sale_country_destination_id = fields.Many2one(
    #    'res.country', string='Country Destination')

    ### default values purchase section
    intrastat_purchase_statistic_amount = fields.Integer(
        string='Statistic Amount Euro', digits=dp.get_precision('Account'))
    intrastat_purchase_transation_nature_id = fields.Many2one(
        'account.intrastat.transation.nature', string='Transation Nature')
    intrastat_purchase_delivery_code_id = fields.Many2one(
        'stock.incoterms', string='Delivery')
    intrastat_purchase_transport_code_id = fields.Many2one(
        'account.intrastat.transport', string='Transport')
