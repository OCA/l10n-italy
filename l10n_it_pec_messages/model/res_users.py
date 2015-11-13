# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014-2015 Agile Business Group http://www.agilebg.com
#    @authors
#       Alessio Gerace <alessio.gerace@gmail.com>
#       Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#       Roberto Onnis <roberto.onnis@innoviu.com>
#
#   About license see __openerp__.py
#
##############################################################################
from openerp.osv import fields, orm


class res_users(orm.Model):
    _inherit = 'res.users'

    _columns = {
        'allowed_server_ids': fields.many2many(
            'fetchmail.server', 'fetchmail_server_user_rel',
            'user_id', 'server_id',
            'Fetchmail servers allowed to be used'),
    }
