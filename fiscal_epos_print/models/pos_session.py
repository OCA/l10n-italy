# -*- coding: utf-8 -*-

from odoo import models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.multi
    def action_pos_session_close(self):
        return super(PosSession, self.with_context(pos_rounding=True)).\
            action_pos_session_close()
