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
# Categories
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

    def _get_def_server(self, cr, uid, ids, *a):
        res = {}
        user_pool=self.pool.get('res.users')
        user=user_pool.browse(cr, uid, [uid])[0]
        return user.allowed_server_ids[0].id


    _name = "message.category"
    _description = "Message Category"
    _columns = {
        'name': fields.char(
            'Name', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(
            _name_get_fnc, type="char", string='Name'),
        'parent_id': fields.many2one(
            'message.category','Parent Category',
            select=True, ondelete='cascade'),
        'child_id': fields.one2many(
            'message.category', 'parent_id', string='Child Categories'),
        'sequence': fields.integer(
            'Sequence', select=True,
            help=(
                "Gives the sequence order when displaying"
                "a list of product categories."
            )
        ),
        'type': fields.selection(
            [('view','View'), ('normal','Normal')], 'Category Type',
            help=(
                "A category of the view type is a virtual category "
                "that can be used as the parent of another category "
                "to create a hierarchical structure."
            )
        ),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'server_id': fields.many2one(
            'fetchmail.server', 'Server Pec', readonly=True),
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

    def _get_out_server(self, cr, uid, ids, *a):
        res = {}
        for id in self.browse(cr, uid, ids):
            res[id.id] = False
            if id.server_id:
                if id.server_id.out_server_id:
                    res[id.id] = id.server_id.out_server_id[0].id
        return res

    _columns = {
        'server_id': fields.many2one(
            'fetchmail.server', 'Server Pec', readonly=True),
        'out_server_id': fields.function(
            _get_out_server, type='many2one',
            relation='ir.mail_server',
            string='Related Outgoing Server'),
        'pec_type': fields.selection([
            ('posta-certificata', 'Pec Mail'),
            ('accettazione', 'Reception'),
            ('non-accettazione', 'No Reception'),
            ('presa-in-carico', 'In Progress'),
            ('avvenuta-consegna', 'Delivery'),
            ('errore-consegna', 'Delivery Error'),
            ('preavviso-errore-consegna', 'Notice Delivery Error'),
            ('rilevazione-virus', 'Virus Detected'),
            ], 'Pec Type', readonly=True),
        'error': fields.boolean('Reception Delivery Error'),
        'cert_datetime': fields.datetime(
            'Certified Date and Time ', readonly=True),
        'pec_msg_id': fields.char(
            'PEC-Message-Id',
            help='Message unique identifier', select=1, readonly=True),
        'ref_msg_id': fields.char(
            'ref-Message-Id',
            help='Ref Message unique identifier', select=1, readonly=True),

        'inprogress_message_id': fields.many2one(
            'mail.message', 'Message In Progress', readonly=True),
        'reception_message_id': fields.many2one(
            'mail.message', 'Reception Message', readonly=True),
        'no_reception_message_id': fields.many2one(
            'mail.message', 'No Reception Message', readonly=True),
        'notice_delivery_err_message_id': fields.many2one(
            'mail.message', 'Notice Error Delivery Message', readonly=True),
        'delivery_message_id': fields.many2one(
            'mail.message', 'Delivery Message', readonly=True),
        'delivery_err_message_id': fields.many2one(
            'mail.message', 'Error Delivery Message', readonly=True),
        'virus_message_id': fields.many2one(
            'mail.message', 'Virus Detected', readonly=True),


        'main_msg_progress_message_ids': fields.one2many(
            'mail.message', 'inprogress_message_id',
            'Main messages',  readonly=True),
        'main_msg_delivery_message_ids': fields.one2many(
            'mail.message', 'delivery_message_id',
            'Main messages',  readonly=True),
        'main_msg_delivery_err_message_ids': fields.one2many(
            'mail.message', 'delivery_err_message_id',
            'Main messages',  readonly=True),
        'main_msg_notice_delivery_err_message_ids': fields.one2many(
            'mail.message', 'notice_delivery_err_message_id',
            'Main messages',  readonly=True),
        'main_msg_reception_message_ids': fields.one2many(
            'mail.message', 'reception_message_id',
            'Main messages', readonly=True),
        'main_msg_no_reception_message_ids': fields.one2many(
            'mail.message', 'no_reception_message_id',
            'Main messages', readonly=True),
        'main_msg_virus_message_ids': fields.one2many(
            'mail.message', 'virus_message_id',
            'Main messages', readonly=True),
        'folder_id': fields.many2one(
            'message.category','Folder', required=False,
            change_default=True,
            help="Select category for the current product"),
    }

    def _search(
        self, cr, uid, args, offset=0, limit=None, order=None,
        context=None, count=False, access_rights_uid=None
    ):
        if context is None:
            context = {}
        if context.get('pec_messages'):
            return super(orm.Model, self)._search(
                cr, uid, args, offset=offset, limit=limit, order=order,
                context=context, count=count,
                access_rights_uid=access_rights_uid)
        else:
            return super(MailMessage, self)._search(
                cr, uid, args, offset=offset, limit=limit, order=order,
                context=context, count=count,
                access_rights_uid=access_rights_uid)

    def check_access_rule(self, cr, uid, ids, operation, context=None):
        if context is None:
            context = {}
        print context
        if context.get('pec_messages'):
            return super(orm.Model, self).check_access_rule(
                cr, uid, ids, operation, context=context)
        else:
            return super(MailMessage, self).check_access_rule(
                cr, uid, ids, operation, context=context)
