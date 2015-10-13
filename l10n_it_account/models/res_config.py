# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#
#    About license, see __openerp__.py
#
##############################################################################

from openerp import fields, models, api


class L10nItConfigSettings(models.TransientModel):
    _inherit = 'l10n_it.config.settings'

    def _default_company(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        'res.company', 'Company', required=True, default=_default_company)
    skip_it_account_check = fields.Boolean(
        "Skip Italian checks",
        help="Set this for not Italian companies, "
             "to skip checking things like tax codes consistencies",
        related='company_id.skip_it_account_check')

    @api.onchange('company_id')
    def onchange_company_id(self):
        self.skip_it_account_check = self.company_id.skip_it_account_check


class ResCompany(models.Model):
    _inherit = 'res.company'
    skip_it_account_check = fields.Boolean(
        "Skip Italian checks",
        help="Set this for not Italian companies, "
             "to skip checking things like tax codes consistencies")
