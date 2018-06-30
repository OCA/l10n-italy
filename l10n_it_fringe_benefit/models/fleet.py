# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Author(s): Alessandro Camilli (alessandrocamilli@openforce.it)
#               Andrea Colangelo (andreacolangelo@openforce.it)
#
#    Copyright © 2016 Openforce di Camilli Alessandro (www.openforce.it)
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
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/agpl-3.0.txt.
#
##############################################################################


from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
import base64
import csv


class fleet_vehicle_model(models.Model):
    _inherit = 'fleet.vehicle.model'

    @api.multi
    @api.depends('fringe_benefit_ids')
    def _compute_fb_cost_km(self):
        for vm in self:
            domain = [('model_id', '=', vm.id)]
            fb = self.env['fleet.fringe.benefit'].search(
                domain, order='date desc', limit=1)
            vm.fringe_benefit_cost_km = fb.cost_km or 0.0

    fringe_benefit_ids = fields.One2many('fleet.fringe.benefit',
                                         'model_id',
                                         string='Fringe Benefit')
    fringe_benefit_cost_km = fields.Float(string='Fringe Benefit Cost Km',
                                          compute="_compute_fb_cost_km",
                                          store=True)


class fleet_fringe_benefit_version(models.Model):
    _name = 'fleet.fringe.benefit.version'

    date = fields.Date('Date', required=True)
    name = fields.Char('Name', required=True)
    line_ids = fields.One2many(
        'fleet.fringe.benefit', 'version_id', string='Fleet Forecasts')

    def _import_prepare_row(self, data):
        '''
        To extend for redifine row values
        '''
        return data

    def _import_csv_prepare_column_name(self, row_col):
        '''
        To extend for redifine columns name
        '''
        return row_col

    def import_from_csv(self, data):
        #
        # Setup Cols
        #
        csvfile = base64.decodestring(
            data['form']['file_to_import']).splitlines()
        if data['form']['field_separator_csv'] \
                and data['form']['field_separator_csv'][:1] == ';':
            reader = csv.reader(csvfile, delimiter=';')
        else:
            reader = csv.reader(csvfile)

        row_data = {}
        row_data2 = {}
        lines = []
        rownum = 0

        # Set columns
        for row in reader:
            if rownum == 0:
                row = self._import_csv_prepare_column_name(row)
                header = row
            else:
                colnum = 0
                row_data2 = row_data.copy()
                for col in row:
                    field = header[colnum]
                    row_data2[field] = col
                    colnum += 1
                lines.append(row_data2)
            rownum += 1

        # Version
        table_version = False
        if data['form']['operation'] == 'new':
            val = {
                'name': data['form']['name'],
                'date': data['form']['date']
            }
            table_version = self.create(val)
        else:
            table_version = data['form']['table_to_update_id']

        for row in lines:
            # Avoid subhead
            if 'MODELLO' not in row or not row['MODELLO']:
                continue
            # Brand
            brand_obj = self.env['fleet.vehicle.model.brand']
            domain = [('name', 'ilike', row['MARCA'])]
            brand = brand_obj.search(domain, limit=1)
            if not brand:
                val = {
                    'name': row['MARCA']
                }
                brand = brand_obj.create(val)
            # Model
            modelname = '%s - %s' % (row['MODELLO'], row['SERIE'])
            model_obj = self.env['fleet.vehicle.model']
            domain = [
                ('brand_id', '=', brand.id),
                ('modelname', 'ilike', modelname)
            ]
            model = model_obj.search(domain, limit=1)
            if not model:
                val = {
                    'brand_id': brand.id,
                    'modelname': modelname
                }
                model = model_obj.create(val)
            # Cost
            cost_km = 0
            if 'COSTO CHILOMETRICO 15.000 KM' in row and\
                    row['COSTO CHILOMETRICO 15.000 KM']:
                cost_km = float(row['COSTO CHILOMETRICO 15.000 KM']
                                .replace('.', '').replace(',', '.'))
            # Fringe Benefits
            fringe_benefits_year = 0
            if 'FRINGE BENEFIT ANNUALE' in row and\
                    row['FRINGE BENEFIT ANNUALE']:
                fringe_benefits_year = float(
                    row['FRINGE BENEFIT ANNUALE'].replace('.', '')
                    .replace(',', '.'))
            # Serie
            series = 'SERIE' in row and row['SERIE'] or False
            # ACI datas
            aci_data = {
                'version_id': table_version.id,
                'brand_id': brand.id,
                'model_id': model.id,
                'series': series,
                'cost_km': cost_km,
                'fringe_benefits_year': fringe_benefits_year,
            }
            domain = [
                ('version_id', '=', table_version.id),
                ('brand_id', '=', brand.id),
                ('model_id', '=', model.id),
                ('series', '=', series),
            ]
            aci_line_id = self.env['fleet.fringe.benefit'].search(domain)
            if aci_line_id:
                aci_line_id.write(aci_data)
            else:
                aci_line_id = self.env['fleet.fringe.benefit'].create(aci_data)


class fleet_fringe_benefit(models.Model):
    _name = 'fleet.fringe.benefit'

    @api.multi
    @api.depends('version_id.date')
    def _compute_date_version(self):
        for fb in self:
            fb.date = fb.version_id.date

    version_id = fields.Many2one(
        'fleet.fringe.benefit.version', string='Version', ondelete="cascade",
        readonly=True)
    date = fields.Date('Date Version', compute="_compute_date_version",
                       store=True)
    brand_id = fields.Many2one('fleet.vehicle.model.brand', string='Brand',
                               required=True)
    model_id = fields.Many2one(
        'fleet.vehicle.model', string='Model', required=True)
    series = fields.Char(string='Series')
    cost_km = fields.Float(
        string='Cost Km', digits=dp.get_precision('Fringe Benefit cost km'))
    fringe_benefits_year = fields.Float(string='Firnge benefit year')
