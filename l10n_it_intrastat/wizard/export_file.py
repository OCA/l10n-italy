# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Openforce di Camilli Alessandro (www.openforce.it)
#    Copyright (C) 2015
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

from openerp import models, api, fields
import base64
import contextlib
import cStringIO

from openerp import tools
from openerp.tools.translate import _
from openerp.tools.misc import get_iso_codes

class account_intrastat_export_file(models.TransientModel):
    _name = "account.intrastat.export.file"
    
    name = fields.Char(string='File Name', readonly=True)
    data = fields.Binary(string='File', readonly=True)
    state = fields.Selection([('choose', 'choose'), 
                              ('get', 'get')], 
                             string='State', default='choose')

    @api.multi
    def act_getfile(self):
        
        statement_id = self.env.context.get('active_id')
        statement = self.env['account.intrastat.statement'].browse(statement_id)
        file = statement.generate_file_export()
        filename = statement._get_file_name()
        # file = self.env['account.intrastat.statement'].\
        #     browse(statement_id).generate_file_export()
        out = base64.encodestring(file)
        
        view = self.env['ir.model.data'].get_object_reference(
            'l10n_it_intrastat', 'wizard_account_intrastat_export_file')
        view_id = view[1] or False
            
        # name = "%s.%s" % (filename, extension)
        self.write({ 'state': 'get', 'data': out, 'name': filename })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.intrastat.export.file',
            'view_mode': 'form',
            'view_type': 'form',
            'name': _('Export Intrastat File'),
            'res_id': self.id,
            'nodestroy': True,
            #'views': [(False, 'form')],
            'view_id': [view_id],
            'target': 'new',
        }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
