from openerp.osv import fields
from openerp.osv import orm
from openerp.exceptions import Warning as UserError


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def create(self, cr, uid, vals, context={}):
        inv_partner = False
        inv_fiscal_pos = False
        inv_journal = False
        fiscal_document_type_id = vals.get('fiscal_document_type_id', False)
        if not fiscal_document_type_id:
            if 'partner_id' in vals and vals['partner_id']:
                inv_partner = self.pool.get('res.partner').browse(
                    cr, uid, vals['partner_id'], context=context)
            if 'fiscal_position' in vals and vals['fiscal_position']:
                inv_fiscal_pos = self.pool.get('account.fiscal.position').browse(
                    cr, uid, vals['fiscal_position'], context=context)
            if 'journal_id' in vals and vals['journal_id']:
                inv_journal = self.pool.get('account.journal').browse(
                    cr, uid, vals['journal_id'], context=context)
            dt = self._get_document_fiscal_type(
                cr, uid, [], vals.get('type', ''), inv_partner, inv_fiscal_pos,
                inv_journal, context=context)
            if dt:
                vals['fiscal_document_type_id'] = dt[0]
        return super(AccountInvoice, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context={}):
        if isinstance(ids, (int, float, long)):
            ids = [ids]
        fiscal_document_type_id = vals.get('fiscal_document_type_id', False)
        if not fiscal_document_type_id:
            invoice_list = self.browse(cr, uid, ids, context=context)
            for invoice in invoice_list:
                if not invoice.fiscal_document_type_id:
                    if invoice.state == 'draft':
                        inv_type = invoice.type
                        inv_partner = invoice.partner_id
                        inv_fiscal_pos = invoice.fiscal_position
                        inv_journal = invoice.journal_id
                        if 'type' in vals and vals['type']:
                            inv_type = vals['type']
                        if 'partner_id' in vals and vals['partner_id']:
                            inv_partner = self.pool.get('res.partner').browse(
                                cr, uid, vals['partner_id'], context=context)
                        if 'fiscal_position' in vals and vals['fiscal_position']:
                            inv_fiscal_pos = self.pool[
                                'account.fiscal.position'].browse(
                                    cr, uid, vals['fiscal_position'], context=context)
                        if 'journal_id' in vals and vals['journal_id']:
                            inv_journal = self.pool['account.journal'].browse(
                                cr, uid, vals['journal_id'], context=context)
                        dt = self._get_document_fiscal_type(
                            cr, uid, ids, inv_type, inv_partner, inv_fiscal_pos,
                            inv_journal, context=context)
                        if dt:
                            vals['fiscal_document_type_id'] = dt[0]
        ret = super(AccountInvoice, self).write(
            cr, uid, ids, vals, context=context)
        return ret

    def _get_document_fiscal_type(
            self, cr, uid, ids, type=None, partner=None, fiscal_position=None,
            journal=None, context={}):
        dt = []
        doc_id = False
        if not type:
            type = 'out_invoice'

        # Partner
        if partner:
            if type in ('out_invoice'):
                doc_id = partner.out_fiscal_document_type.id or False
            elif type in ('in_invoice'):
                doc_id = partner.in_fiscal_document_type.id or False
        # Fiscal Position
        if not doc_id and fiscal_position:
            doc_id = fiscal_position.fiscal_document_type_id.id or False
        # Journal
        if not doc_id and journal:
            dt = self.pool.get('fiscal.document.type').search(cr, uid, [
                ('journal_ids', 'in', [journal.id])])
        if not doc_id and not dt:
            dt = self.pool.get('fiscal.document.type').search(cr, uid, [
                (type, '=', True)])
        if doc_id:
            dt.append(doc_id)
        return dt

    _columns = {
            'fiscal_document_type_id': fields.many2one(
                'fiscal.document.type',
                string="Fiscal Document Type",),
        }

