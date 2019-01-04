# -*- coding: utf-8 -*-

from openerp import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fatturapa_pt_id = fields.Many2one(
        string=_('Fiscal Payment Term'),
        comodel_name='fatturapa.payment_term',
        compute='_compute_fatturapa_pt_id'
    )

    fatturapa_pm_id = fields.Many2one(
        string=_('Fiscal Payment Method'),
        comodel_name='fatturapa.payment_method',
        compute='_compute_fatturapa_pm_id'
    )

    @api.one
    def _compute_fatturapa_pt_id(self):
        if self.payment_term and self.payment_term.fatturapa_pt_id:
            self.fatturapa_pt_id = self.payment_term.fatturapa_pt_id

    @api.one
    def _compute_fatturapa_pm_id(self):
        if self.payment_term and self.payment_term.fatturapa_pm_id:
            self.fatturapa_pm_id = self.payment_term.fatturapa_pm_id
