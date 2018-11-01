# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountTax(models.Model):
    _inherit = "account.tax"

    exclude_from_registries = fields.Boolean(
        string='Exclude from VAT registries')

    def get_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_balance_domain(
            state_list, type_list)
        if self.env.context.get('vat_registry_journal_ids'):
            domain.append((
                'move_id.journal_id', 'in',
                self.env.context['vat_registry_journal_ids']))
        return domain

    def get_base_balance_domain(self, state_list, type_list):
        domain = super(AccountTax, self).get_base_balance_domain(
            state_list, type_list)
        if self.env.context.get('vat_registry_journal_ids'):
            domain.append((
                'move_id.journal_id', 'in',
                self.env.context['vat_registry_journal_ids']))
        return domain
