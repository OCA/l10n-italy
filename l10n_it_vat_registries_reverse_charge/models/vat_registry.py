# -*- coding: utf-8 -*-
# Copyright 2017 Lara Baggio - Link IT srl
# (<http://www.linkgroup.it/>)
# Copyright 2014-2017 Lorenzo Battistini - Agile Business Group
# (<http://www.agilebg.com>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class ReportRegistroIva(models.AbstractModel):
    _inherit = 'report.l10n_it_vat_registries.report_registro_iva'

    @api.model
    def render_html(self, docids, data=None):
        # docids required by caller but not used
        # see addons/account/report/account_balance.py

        data['form']['get_invoice_supplier'] = self._get_invoice_supplier

        return super(ReportRegistroIva, self).render_html(docids, data)



    def _get_invoice_supplier(self, move):
        rc_supplier = {
            'name': '',
            'vat': ''
            }
        invoice = self._get_invoice_from_move(move)

        if invoice.rc_partner_supplier_id:
            p = invoice.rc_partner_supplier_id
            rc_supplier['name'] = p.name.strip()
            rc_supplier['vat'] = (p.vat or "").strip()

        return rc_supplier
