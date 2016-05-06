# -*- coding: utf-8 -*-
# © 2016 Andrea Cometa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class DistintaReportQweb(models.AbstractModel):

    _name = 'report.l10n_it_ricevute_bancarie.distinta_qweb'

    @api.multi
    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'l10n_it_ricevute_bancarie.distinta_qweb')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'company': False,
            'docs': self.env[report.model].browse(self._ids),
        }
        return report_obj.render(
            'l10n_it_ricevute_bancarie.distinta_qweb',
            docargs)
