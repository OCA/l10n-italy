# -*- coding: utf-8 -*-
# © 2016 Andrea Cometa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class DistintaReportQweb(models.AbstractModel):

    _name = 'report.l10n_it_ricevute_bancarie.distinta_qweb'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        docargs = {
            'doc_ids': docids,
            'doc_model': 'riba.distinta',
            'docs': self.env['riba.distinta'].browse(docids),
        }
        return report_obj.render(
            'l10n_it_ricevute_bancarie.distinta_qweb',
            values=docargs)
