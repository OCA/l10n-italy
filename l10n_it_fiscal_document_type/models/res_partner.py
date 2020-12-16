from openerp.osv import fields
from openerp.osv import orm
from openerp.exceptions import Warning as UserError


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
            'out_fiscal_document_type': fields.many2one(
                'fiscal.document.type', string="Out Fiscal Document Type"),
            'in_fiscal_document_type': fields.many2one(
                'fiscal.document.type', string="In Fiscal Document Type"),
        }
