# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#    Copyright 2014 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

from openerp.osv import fields, orm

#----------------------------------------------------------
# Folders
#----------------------------------------------------------
class message_category(orm.Model):

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    def _get_def_server(self, cr, uid, ids, context=None):
        res = {}
        user_pool=self.pool.get('res.users')
        user=user_pool.browse(
            cr, uid, [uid], context=context)[0]
        return user.allowed_server_ids[0].id


    _name = "message.category"
    _description = "Message Folder"
    _columns = {
        'name': fields.char(
            'Name', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(
            _name_get_fnc, type="char", string='Name'),
        'parent_id': fields.many2one(
            'message.category','Parent Folder',
            select=True, ondelete='cascade'),
        'child_id': fields.one2many(
            'message.category', 'parent_id', string='Child Folders'),
        'sequence': fields.integer(
            'Sequence', select=True,
            help=(
                "Gives the sequence order when displaying"
                "a list of product categories."
            )
        ),
        'type': fields.selection(
            [('view','View'), ('normal','Normal')], 'Folder Type',
            help=(
                "A folder of the view type is a virtual folder "
                "that can be used as the parent of another folder "
                "to create a hierarchical structure."
            )
        ),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'server_id': fields.many2one(
            'fetchmail.server', 'Server Pec'),
    }


    _defaults = {
        'server_id': _get_def_server,
        'type' : lambda *a : 'normal',
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from message_category where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    ]
    def child_get(self, cr, uid, ids):
        return [ids]



class MailMessage(orm.Model):
    _inherit = "mail.message"

    _columns = {
        'folder_id': fields.many2one(
            'message.category','Folder', required=False,
            change_default=True,
            help="Select category for the current product"),
    }

