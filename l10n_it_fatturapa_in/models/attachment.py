# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 AgileBG SAGL <http://www.agilebg.com>
#    Copyright (C) 2015 innoviu Srl <http://www.innoviu.com>
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

AVAILABLE_STATES = [
    ('draft', 'Draft'),
    ('processed', 'Processed'),
    ('not_processed', 'Unprocessed'),
    ('error', 'Error')]


class FatturaPAAttachmentIn(orm.Model):
    _name = "fatturapa.attachment.in"
    _description = "FatturaPA import File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    _columns = {
        'ir_attachment_id': fields.many2one('ir.attachment', 'Attachment'),
        'state': fields.selection(AVAILABLE_STATES, 'State'),
    }

    _defaults = {
        'state': 'draft',
    }
