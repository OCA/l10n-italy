# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _


class FetchmailServer(orm.Model):
    _inherit = "fetchmail.server"

    _columns = {
        'is_fatturapa_pec': fields.boolean('FatturaPA PEC server'),
    }
