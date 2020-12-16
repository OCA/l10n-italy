from openerp.osv import fields
from openerp.osv import orm


class AccountFiscalPosition(orm.Model):
    _inherit = 'account.fiscal.position'

    _columns = {
            'fiscal_document_type_id': fields.many2one(
                'fiscal.document.type', string="Fiscal Document Type",
                readonly=False),
        }
