# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Alessandro Camilli
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


class wizard_of_import_lead(models.TransientModel):
    _name = "wizard.import.aci.table"
    _description = "Wizard to import ACI table"

    operation = fields.Selection([
        ('new', 'New Table'),
        ('update', 'Update Table'),
    ], string='Operation', required=True)
    table_to_update_id = fields.Many2one('fleet.fringe.benefit.version',
                                         string='ACI table to update')
    file_to_import = fields.Binary(string='File CSV to import',  required=True)
    field_separator_csv = fields.Char(string='Field separator for csv',
                                      required=True, default=",")
    name = fields.Char(string='Name')
    date = fields.Date(string='Date')

    @api.multi
    def execute_import(self):
        data = {}
        for wiz_obj in self:
            if 'form' not in data:
                data['form'] = {}
            data['form']['operation'] = wiz_obj['operation']
            data['form']['table_to_update_id'] = wiz_obj[
                'table_to_update_id'] and wiz_obj[
                'table_to_update_id'][0] or False
            data['form']['file_to_import'] = wiz_obj['file_to_import']
            data['form']['field_separator_csv'] = wiz_obj[
                'field_separator_csv']
            data['form']['name'] = wiz_obj['name']
            data['form']['date'] = wiz_obj['date']

            self.env['fleet.fringe.benefit.version'].import_from_csv(data)

        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
