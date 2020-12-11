# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv import orm


class AccountTax(orm.Model):

    _inherit = 'account.tax'

    _columns = {
        'kind_id': fields.many2one('account.tax.kind', string="Exemption Kind"),
        'law_reference': fields.char('Law reference'),
    }
