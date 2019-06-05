from odoo import models, fields, api


class TrialBalanceReportWizard(models.TransientModel):
    _inherit = 'trial.balance.report.wizard'
    cee_balance = fields.Boolean("Civil code statutory financial statements")

    @api.onchange('cee_balance')
    def onchange_cee_balance(self):
        if self.cee_balance:
            self.hierarchy_on = 'relation'

    def move_cee_groups_to_groups(self):
        accounts = self.env['account.account'].search([])
        old_vals = {}
        for account in accounts:
            old_vals[account.id] = account.group_id.id
            account.group_id = account.cee_group_id.id
        return old_vals

    def get_old_group_values_back(self, old_vals):
        for account_id in old_vals:
            self.env['account.account'].browse(
                account_id).group_id = old_vals[account_id]

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        if self.cee_balance:
            old_vals = self.move_cee_groups_to_groups()
        res = super(TrialBalanceReportWizard, self.with_context(
            cee_balance=self.cee_balance)).button_export_html()
        if self.cee_balance:
            self.get_old_group_values_back(old_vals)
        return res

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        if self.cee_balance:
            old_vals = self.move_cee_groups_to_groups()
        res = super(TrialBalanceReportWizard, self.with_context(
            cee_balance=self.cee_balance)).button_export_pdf()
        if self.cee_balance:
            self.get_old_group_values_back(old_vals)
        return res

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        if self.cee_balance:
            old_vals = self.move_cee_groups_to_groups()
        res = super(TrialBalanceReportWizard, self.with_context(
            cee_balance=self.cee_balance)).button_export_xlsx()
        if self.cee_balance:
            self.get_old_group_values_back(old_vals)
        return res
