# -*- coding: utf-8 -*-
#
#    Copyright (C) 2017 Apulia Software s.r.l. (http://www.apuliasoftware.it)
#    @author Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
#   Andrea Cometa <a.cometa@apuliasoftware.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class AccountTaxKind(orm.Model):

    _name = 'account.tax.kind'
    _rec_name = 'display_name'

    #@api.depends('code', 'name')
    #@api.multi
    def _compute_display_name(self, cr, uid, ids, name, args, context={}):
        display_name = {}
        for record in self.browse(cr, uid, ids, context=context):
            display_name[record.id] = u'[%s] %s' % (record.code, record.name)
        return display_name

    _columns = {
        'code': fields.char(string="Code", size=3, required=True),
        'name': fields.char(string="Name", size=252, required=True),
        'display_name': fields.function(
            _compute_display_name, string="Name", size=255, type='char',
            store=True)
    }

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                    context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            records = self.search(cr, uid, [
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(cr, uid, args, limit=limit)
        return self.name_get(cr, uid, records, context=context)
