from openerp.osv import fields
from openerp.osv import orm
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class AccountJournal(orm.Model):
    _inherit = 'account.journal'

    def check_doc_type_relation(self, cr, uid, ids, context={}):
        doc_model = self.pool.get('fiscal.document.type')
        for journal in self.browse(cr, uid, ids, context):
            docs = doc_model.search(
                cr, uid, [('journal_ids', 'in', [journal.id])],
                context=context)
            if len(docs) > 1:
                raise UserError(
                    _("Journal %s can be linked to only 1 fiscal document "
                      "type (found in %s)") % (journal.name, ', '.join(
                        [doc_model.browse(cr, uid, d, context=context
                                          ).code for d in docs])))
