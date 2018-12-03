# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - SdI channel
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class IrMailServer(orm.Model):
    _inherit = "ir.mail_server"

    _columns = {
        'is_fatturapa_pec': fields.boolean('FatturaPA PEC server'),
        'email_from_for_fatturaPA': fields.char('Sender Email Address', size=250),
    }
