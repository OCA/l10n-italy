# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
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

from openerp.osv import fields, orm


class FatturaPAAttachment(orm.Model):
    _name = "fatturapa.attachment"
    _description = "FatturaPA Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    _columns = {
        'ir_attachment_id': fields.many2one('ir.attachment', 'Attachment'),
        'state': fields.selection(
            (('draft', 'Draft'),
                ('sent', 'Sent'),
                ('rejected', 'Rejected'),
                ('accepted', 'Accepted')),
            'State'),
    }

    _defaults = {
        'state': 'draft',
    }
