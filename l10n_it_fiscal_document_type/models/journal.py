from odoo import models, api
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.multi
    def check_doc_type_relation(self):
        doc_model = self.env['fiscal.document.type']
        for journal in self:
            docs = doc_model.search(
                [('journal_ids', 'in', [journal.id])])
            if len(docs) > 1:
                raise UserError(
                    _("Journal %s can be linked to only 1 fiscal document "
                      "type (found in %s)")
                    % (journal.name, ', '.join([d.code for d in docs])))
