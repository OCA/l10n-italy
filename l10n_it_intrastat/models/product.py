# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Apruzzese Francesco (f.apruzzese@apuliasoftware.it)
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


from openerp import models, fields, api


class product_category(models.Model):
    _inherit = 'product.category'

    intrastat_code_id = fields.Many2one('report.intrastat.code',
                                        string='Intrastat Code')


class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    def get_intrastat_id(self):
        '''
        It Returns the intrastat code with the following priority:
        - Intrastat Code on product template
        - Intrastat Code on product category
        '''
        intrastat_id = False
        # From Product
        if self.intrastat_id:
            intrastat_id = self.intrastat_id.id
        elif self.categ_id and self.categ_id.intrastat_code_id: 
            intrastat_id = self.intrastat_code_id.id
        return intrastat_id
