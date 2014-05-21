# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
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

import time
from report import report_sxw
from datetime import datetime
from osv import osv
from osv import fields


class report_riba_webkit(report_sxw.rml_parse):

    def group_riba_data(self, objects):
        res = {}
        for distinta in objects:
            for line in distinta.line_ids:
                if not line.due_date in res:
                    res.update({line.due_date: [line]})
                else:
                    res[line.due_date] = res[line.due_date] + [line]
        print res
        return res

    def page_number(self, lines, row_limit):
        if not lines or not row_limit:
            return 0
        division = float(len(lines)) / float(row_limit)
        pn = int(ceil(division))
        return pn

    def newlined_text(self, text):
        if text:
            return text.replace('\n', '<br/>')

    def __init__(self, cr, uid, name, context):
        super(report_riba_webkit, self).__init__(cr, uid, name,
                                                 context=context)
        self.localcontext.update({
            'datetime': datetime,
            'time': time,
            'cr': cr,
            'uid': uid,
            'group_riba_data': self.group_riba_data,
            'newlined_text': self.newlined_text,
            'page_number': self.page_number,
        })

report_sxw.report_sxw(
    'report.riba.report.riepilogo_scadenze', 'riba',
    'l10n_it_ricevute_bancarie_report/template/\
riepilogo_scadenze_distinte_riba.mako',
    parser=report_riba_webkit)
