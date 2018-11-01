# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    tax_registry_id = fields.Many2one(
        'account.tax.registry', 'VAT registry',
        help="You can group several journals within 1 registry. In printing "
             "wizard, you will be able to select the registry in order to load"
             " that group of journals")
