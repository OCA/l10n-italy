# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - SdI channel
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class FetchmailServer(orm.Model):
    _inherit = "fetchmail.server"

    _columns = {
        'is_fatturapa_pec': fields.boolean('FatturaPA PEC server'),
    }
