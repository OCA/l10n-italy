from openerp.osv import fields
from openerp.osv import orm
from openerp.exceptions import Warning as UserError


class FiscalDocumentType(orm.Model):
    _name = 'fiscal.document.type'
    _description = 'Fiscal document type'

    _columns = {
        'code': fields.char(string='Code', size=5, required=True),
        'name': fields.char(string='Name', size=150, required=True),
        'out_invoice': fields.boolean(string='Customer Invoice'),
        'in_invoice': fields.boolean(string='Vendor Bill'),
        'out_refund': fields.boolean(string='Customer Credit Note'),
        'in_refund': fields.boolean(string='Vendor Credit Note'),
        'priority': fields.integer(string='Priority', default='3'),
        'journal_ids': fields.many2many(
            'account.journal',
            'account_journal_fiscal_doc_type_rel',
            'fiscal_document_type_id',
            'journal_id',
            'Journals'
        ),
    }

    _order = 'code, priority asc'

    def create(self, cr, uid, vals, context={}):
        res = super(FiscalDocumentType, self).create(
            cr, uid, vals, context=context)
        journal_ids = self.browse(cr, uid, res, context=context).journal_ids
        jids = []
        for jid in journal_ids:
            jids.append(jid.id)
        self.pool.get('account.journal').check_doc_type_relation(
            cr, uid, jids, context)
        return res

    def write(self, cr, uid, ids, vals, context={}):
        res = super(FiscalDocumentType, self).write(
            cr, uid, ids, vals, context=context)
        for doc in self.browse(cr, uid, ids, context):
            journal_ids = []
            for journal in doc.journal_ids:
                journal_ids.append(journal.id)
            self.pool.get('account.journal').check_doc_type_relation(
                cr, uid, journal_ids, context)
        return res

    def name_get(self, cr, uid, ids, context={}):
        res = []
        for doc_type in self.browse(cr, uid, ids, context):
            res.append(
                (doc_type.id, '[%s] %s' % (doc_type.code, doc_type.name)))
        return res

    def name_search(self, cr, uid, name='', args=None, operator='ilike',
                    limit=100, context={}):
        if not args:
            args = []
        if name:
            records = self.search(cr, uid, [
                '|', ('name', operator, name), ('code', operator, name)
                ] + args, limit=limit, context=context)
        else:
            records = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, records, context=context)
