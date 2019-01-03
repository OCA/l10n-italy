# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - FatturaPA - Emission - PEC Support
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

from osv import osv


class SendPEC(osv.osv_memory):
    _name = 'wizard.fatturapa.send.pec'
    _description = "Wizard to send multiple e-invoice PEC"

    def send_pec(self, cr, uid, ids, context=None):
        if context and context.get('active_ids'):
            self.pool['fatturapa.attachment.out'].send_via_pec(
                cr, uid, context['active_ids'], context=context)
SendPEC()
