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
from openerp.osv import orm


class ResPartner(orm.Model):

    # inherit partner because PEC mails are not supposed to be associate to
    # generic models
    _inherit = "res.partner"

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        if context.get('show_pec_email'):
            for record in self.browse(cr, uid, ids, context=context):
                name = record.name
                if (
                    record.parent_id and not
                    record.is_company
                ):
                    name = "%s, %s" % (record.parent_name, name)
                if record.pec_mail:
                    name = "%s <%s>" % (name, record.pec_mail)
                res.append((record.id, name))
            return res
        else:
            return super(ResPartner, self).name_get(
                cr, uid, ids, context=context)
