# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 ISA s.r.l. (<http://www.isa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from report import report_sxw
from osv import osv
from tools.translate import _

class central_journal_report(report_sxw.rml_parse):
    
    def _set_wizard_params(self,form_values):
        if form_values['date_move_line_from'] :
            date_move_line_from=form_values['date_move_line_from']
            filter=("date",">=",date_move_line_from)
            self.filters.append(filter)
        if form_values['date_move_line_to'] :
            date_move_line_to=form_values['date_move_line_to']
            filter=("date","<=",date_move_line_to)
            self.filters.append(filter)
        return True

    def _get_print_info(self, fiscalyear_id):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        fiscalyear_ids=fiscalyear_obj.search(self.cr,self.uid,[('id','=',fiscalyear_id),])
        fiscalyear_data=fiscalyear_obj.browse(self.cr,self.uid,fiscalyear_ids)[0]
        print_info = {
            'start_row': fiscalyear_data.progressive_line_number,
            'start_page': fiscalyear_data.progressive_page_number,
            'start_debit': fiscalyear_data.progressive_debit,
            'start_credit': fiscalyear_data.progressive_credit,
            'year_name': fiscalyear_data.name,
        }
        return print_info

    def _set_print_info(self, fiscalyear_id, end_date_print, end_row, end_page, end_debit, end_credit):
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        fiscalyear_ids=fiscalyear_obj.search(self.cr,self.uid,[('id','=',fiscalyear_id),])
        fiscalyear_data=fiscalyear_obj.browse(self.cr,self.uid,fiscalyear_ids)[0]
        print_info = {
            'date_last_print': end_date_print,
            'progressive_line_number': end_row,
            'progressive_page_number': end_page,
            'progressive_debit': end_debit,
            'progressive_credit': end_credit,
        }
        res = fiscalyear_obj.write(self.cr, self.uid, fiscalyear_ids, print_info)
        return res

    def _get_movements(self):
        move_line_obj = self.pool.get('account.move.line')
        line_ids=move_line_obj.search(self.cr,self.uid,self.filters,order="date, move_id asc")
        report_lines=move_line_obj.browse(self.cr,self.uid,line_ids)
        return report_lines

    def __init__(self, cr, uid, name, context):
        self.filters=[]
        super(central_journal_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
            'get_print_info': self._get_print_info,
            'set_print_info': self._set_print_info,
            'set_wizard_params': self._set_wizard_params,
            'get_movements': self._get_movements,
        })

report_sxw.report_sxw('report.central_journal_report',
                       'account.move.line', 
                       'addons/account_central_journal/report/central_journal_report.mako',
                       parser=central_journal_report)
