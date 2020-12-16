# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2013
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    Copyright (c) 2013 Agile Business Group (http://www.agilebg.com)
#    @author Lorenzo Battistini
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from report import report_sxw
import time


class DeliverySlip(report_sxw.rml_parse):

    def _get_invoice_address(self, picking):
        if picking.sale_id:
            return picking.sale_id.partner_invoice_id
        partner_obj = self.pool.get('res.partner')
        invoice_address_id = picking.partner_id.address_get(
            adr_pref=['invoice']
        )['invoice']
        return partner_obj.browse(
            self.cr, self.uid, invoice_address_id)

    def __init__(self, cr, uid, name, context):
        super(DeliverySlip, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'invoice_address': self._get_invoice_address,
        })


report_sxw.report_sxw('report.ddt_webkit',
                      'stock.picking',
                      'addons/l10n_it_DDT_webkit/report/ddt.mako',
                      parser=DeliverySlip)
