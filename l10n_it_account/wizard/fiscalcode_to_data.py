# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2010-2012 Associazione OpenERP Italia
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

from osv import fields, osv
from tools.translate import _
from datetime import datetime


class wizard_fiscalcode_to_data(osv.osv_memory):

    _name = "wizard.fiscalcode.to.data"
    _description = "Compute missing data from Fiscal Code"
    _columns = {
        'update_birth_date': fields.boolean('Update date of birth'),
        'update_birth_city': fields.boolean('Update city of birth'),
        'update_sex': fields.boolean('Update sex'),
        'relax_fc': fields.boolean('Ignore invalid Fiscal Code'),
    }

    _defaults = {
        'update_birth_date': True,
        'update_birth_city': True,
        'update_sex': True,
    }

    def compute(self, cr, uid, ids, context):
        partner_obj = self.pool.get('res.partner')
        city_obj = self.pool.get('res.city')
        # leading space so that position is the month number
        month_codes = ' ABCDEHLMPRST'
        for wiz in self.browse(cr, uid, ids):
            for partner in partner_obj.browse(cr, uid, context['active_ids']):
                if partner.fiscalcode and len(partner.fiscalcode) == 16:
                    # maybe check fiscalcode sanity here?
                    data = {}
                    fc = partner.fiscalcode.upper()
                    if wiz.update_sex:
                        try:
                            day = int(fc[9:11])
                        except Exception:
                            ### XXX handle insane fc here
                            if wiz.relax_fc:
                                continue
                            else:
                                raise
                        sex = day > 40 and 'F' or 'M'
                        data['sex'] = sex
                    if wiz.update_birth_city:
                        cadaster_code = fc[11:15]
                        birth_city = city_obj.search(cr, uid, [
                            ('cadaster_code', '=', cadaster_code)
                        ])
                        if not birth_city:
                            if wiz.relax_fc:
                                continue
                            else:
                                raise osv.except_osv(
                                    _('Error'),
                                    _('City with cadaster code %s not found')
                                    % cadaster_code
                                )
                        if len(birth_city) > 1:
                            if wiz.relax_fc:
                                continue
                            else:
                                raise osv.except_osv(
                                    _('Error'),
                                    _('More than one city '
                                        'with cadaster code %s')
                                    % cadaster_code
                                )
                        data['birth_city'] = birth_city[0]
                    if wiz.update_birth_date:
                        try:
                            year = int(fc[6:8])
                            day = int(fc[9:11])
                        except ValueError:
                            if wiz.relax_fc:
                                continue
                            else:
                                raise osv.except_osv(
                                    _('Error'),
                                    _('Invalid Fiscal code: %s')
                                    % (fc)
                                )
                        day = day > 40 and day - 40 or day
                        month = month_codes.find(fc[8])
                        if month == -1:
                            if wiz.relax_fc:
                                continue
                            else:
                                raise osv.except_osv(
                                    _('Error'),
                                    _('Fiscal code %s: Invalid month code %s')
                                    % (fc, fc[8])
                                )

                        # Don't format the date string directly to work out
                        # the century
                        try:
                            d = datetime.strptime(
                                '{}{}{}'.format(year, month, day), '%y%m%d'
                            )
                        except ValueError:
                            if wiz.relax_fc:
                                continue
                            else:
                                raise osv.except_osv(
                                    _('Error'),
                                    _('Invalid Fiscal code: %s')
                                    % (fc)
                                )

                        if d > datetime.now():
                            d = datetime(d.year - 100, d.month, d.day)
                        data['birth_date'] = d.strftime('%Y-%m-%d')
                    if data:
                        partner_obj.write(cr, uid, partner.id, data)

        return {}
