# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountTaxRegistry(models.Model):
    _name = 'account.tax.registry'
    _description = 'Tax registry'
    name = fields.Char('Name', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'account.tax.registry'))
    journal_ids = fields.One2many(
        'account.journal', 'tax_registry_id', 'Journals', readonly=True)
    layout_type = fields.Selection([
        ('customer', 'Customer Invoices'),
        ('supplier', 'Supplier Invoices'),
        ('corrispettivi', 'Sums due'),
        ], 'Layout', required=True)
