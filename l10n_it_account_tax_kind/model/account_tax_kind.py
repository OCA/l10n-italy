
from openerp.osv import fields
from openerp.osv import orm


class AccountTaxKind(orm.Model):

    _name = 'account.tax.kind'
    _description = 'Tax exemption kind'

    _columns = {
        'code': fields.char(string='Code', size=4, required=True),
        'name': fields.char(string='Name', required=True),
    }

    def name_get(self, cr, uid, ids, context={}):
        res = []
        for tax_kind in self.browse(cr, uid, ids, context=context):
            res.append(
                (tax_kind.id, '[%s] %s' % (tax_kind.code, tax_kind.name)))
        return res

    def name_search(self, cr, uid, name='', args=None, operator='ilike', limit=100, context={}):
        if not args:
            args = []
        if name:
            records = self.search(cr, uid, [
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit)
        else:
            records = self.search(cr, uid, args, limit=limit)
        return self.name_get(cr, uid, records)
