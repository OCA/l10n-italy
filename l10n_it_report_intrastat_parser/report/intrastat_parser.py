# -*- coding: utf-8 -*-
#
#    Andrea Cometa <a.cometa@apuliasoftware.it>
#

from openerp.report import report_sxw
from openerp import api, models
from openerp.http import request


class ReportIntrastatQweb(models.AbstractModel):

    _name = 'report.l10n_it_report_intrastat.report_intrastat_mod1'

    @api.multi
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(
            'l10n_it_report_intrastat.report_intrastat_mod1')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'objects': self.env[report.model].browse(self._ids),
        }
        # print docargs
        return report_obj.render(
            'l10n_it_report_intrastat.report_intrastat_mod1',
            docargs)
