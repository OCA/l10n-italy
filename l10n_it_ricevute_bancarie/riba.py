# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

from openerp.osv import fields, orm
import decimal_precision as dp
import netsvc
from tools.translate import _


class riba_distinta(orm.Model):

    def _get_acceptance_move_ids(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for distinta in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in distinta.line_ids:
                if (
                    line.acceptance_move_id and
                    line.acceptance_move_id.id not in move_ids
                ):
                    move_ids.append(line.acceptance_move_id.id)
            res[distinta.id] = move_ids
        return res

    def _get_unsolved_move_ids(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for distinta in self.browse(cr, uid, ids, context=context):
            move_ids = []
            for line in distinta.line_ids:
                if (
                    line.unsolved_move_id and
                    line.unsolved_move_id.id not in move_ids
                ):
                    move_ids.append(line.unsolved_move_id.id)
            res[distinta.id] = move_ids
        return res

    def _get_payment_ids(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for distinta in self.browse(cr, uid, ids, context=context):
            move_line_ids = []
            for line in distinta.line_ids:
                for payment in line.payment_ids:
                    if payment.id not in move_line_ids:
                        move_line_ids.append(payment.id)
            res[distinta.id] = move_line_ids
        return res

    _name = 'riba.distinta'
    _description = 'Distinta Riba'

    _columns = {
        'name': fields.char(
            'Reference', size=128, required=True, readonly=True,
            states={'draft': [('readonly', False)]}),
        'config': fields.many2one(
            'riba.configurazione', 'Configuration',
            select=True, required=True, readonly=True,
            states={'draft': [('readonly', False)]},
            help='Riba configuration to be used'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('accepted', 'Accepted'),
            ('accredited', 'Accredited'),
            ('paid', 'Paid'),
            ('unsolved', 'Unsolved'),
            ('cancel', 'Canceled')], 'State', select=True, readonly=True),
        'line_ids': fields.one2many(
            'riba.distinta.line', 'distinta_id',
            'Riba deadlines', readonly=True,
            states={'draft': [('readonly', False)]}),
        'user_id': fields.many2one(
            'res.users', 'User', required=True, readonly=True,
            states={'draft': [('readonly', False)]}),
        'date_created': fields.date('Creation date', readonly=True),
        'date_accepted': fields.date('Acceptance date', readonly=True),
        'date_accreditation': fields.date('Accreditation date', readonly=True),
        'date_paid': fields.date('Paid date', readonly=True),
        'date_unsolved': fields.date('Unsolved date', readonly=True),
        'company_id': fields.many2one(
            'res.company', 'Company', required=True, readonly=True,
            states={'draft': [('readonly', False)]}),
        'acceptance_move_ids': fields.function(
            _get_acceptance_move_ids, type='many2many',
            relation='account.move', method=True, string="Acceptance Entries"),
        'accreditation_move_id': fields.many2one(
            'account.move', 'Accreditation Entry', readonly=True),
        'payment_ids': fields.function(
            _get_payment_ids, relation='account.move.line', type="many2many",
            string='Payments'),
        'unsolved_move_ids': fields.function(
            _get_unsolved_move_ids, type='many2many', relation='account.move',
            method=True, string="Unsolved Entries"),
        'type': fields.related(
            'config', 'tipo', type='char', size=32, string='Type',
            readonly=True),
        'registration_date': fields.date(
            'Registration Date',
            states={'draft': [('readonly', False)],
                    'cancel': [('readonly', False)], },
            select=True,
            readonly=True,
            required=True,
            help="Keep empty to use the current date"),
    }

    _defaults = {
        'user_id': lambda self, cr, uid, context: uid,
        'date_created': fields.date.context_today,
        'name': lambda self, cr, uid, context: self.pool.get(
            'ir.sequence').get(cr, uid, 'riba.distinta'),
        'company_id': lambda self, cr, uid, c: self.pool.get(
            'res.company'
        )._company_default_get(cr, uid, 'riba.distinta', context=c),
        'registration_date': fields.date.context_today,
    }

    def unlink(self, cr, uid, ids, context=None):
        for distinta in self.browse(cr, uid, ids, context=context):
            if distinta.state not in ('draft', 'cancel'):
                raise orm.except_orm(
                    _('Error'),
                    _('Distinta %s is in state %s. You can only delete '
                      'documents in state draft or canceled')
                    % (distinta.name, distinta.state))
        super(riba_distinta, self).unlink(cr, uid, ids, context=context)
        return True

    def confirm(self, cr, uid, ids, context=None):
        line_pool = self.pool.get('riba.distinta.line')
        for distinta in self.browse(cr, uid, ids, context=context):
            line_pool.confirm(
                cr, uid, [line.id for line in distinta.line_ids],
                context=context)
        return True

    def riba_new(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'draft',
        }, context=context)
        return True

    def riba_cancel(self, cr, uid, ids, context=None):
        for distinta in self.browse(cr, uid, ids, context=context):
            # TODO remove ervery other move
            for line in distinta.line_ids:
                if line.acceptance_move_id:
                    line.acceptance_move_id.unlink()
                if line.unsolved_move_id:
                    line.unsolved_move_id.unlink()
            if distinta.accreditation_move_id:
                distinta.accreditation_move_id.unlink()
        self.write(cr, uid, ids, {
            'state': 'cancel',
        }, context=context)
        return True

    def riba_accepted(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'accepted',
            'date_accepted': fields.date.context_today(
                self, cr, uid, context),
        }, context=context)
        return True

    def riba_accredited(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'accredited',
            'date_accreditation': fields.date.context_today(
                self, cr, uid, context),
        }, context=context)
        for distinta in self.browse(cr, uid, ids, context=context):
            for line in distinta.line_ids:
                line.write({'state': 'accredited'})
        return True

    def riba_paid(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'paid',
            'date_paid': fields.date.context_today(
                self, cr, uid, context),
        }, context=context)
        return True

    def riba_unsolved(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {
            'state': 'unsolved',
            'date_unsolved': fields.date.context_today(
                self, cr, uid, context),
        }, context=context)
        return True

    def test_accepted(self, cr, uid, ids, *args):
        for distinta in self.browse(cr, uid, ids):
            for line in distinta.line_ids:
                if line.state != 'confirmed':
                    return False
        return True

    def test_unsolved(self, cr, uid, ids, *args):
        for distinta in self.browse(cr, uid, ids):
            for line in distinta.line_ids:
                if line.state != 'unsolved':
                    return False
        return True

    def test_paid(self, cr, uid, ids, *args):
        for distinta in self.browse(cr, uid, ids):
            for line in distinta.line_ids:
                if line.state != 'paid':
                    return False
        return True

    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        wf_service = netsvc.LocalService("workflow")
        for distinta_id in ids:
            wf_service.trg_delete(uid, 'riba.distinta', distinta_id, cr)
            wf_service.trg_create(uid, 'riba.distinta', distinta_id, cr)
        return True


class riba_distinta_line(orm.Model):

    def _get_line_values(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {}
            res[line.id]['amount'] = 0.0
            res[line.id]['invoice_date'] = ''
            res[line.id]['invoice_number'] = ''
            for move_line in line.move_line_ids:
                res[line.id]['amount'] += move_line.amount
                if not res[line.id]['invoice_date']:
                    res[line.id]['invoice_date'] = str(
                        move_line.move_line_id.invoice.date_invoice)
                else:
                    res[line.id]['invoice_date'] += ', ' + str(
                        move_line.move_line_id.invoice.date_invoice)
                if not res[line.id]['invoice_number']:
                    res[line.id]['invoice_number'] = str(
                        move_line.move_line_id.invoice.internal_number)
                else:
                    res[line.id]['invoice_number'] += ', ' + str(
                        move_line.move_line_id.invoice.internal_number)
        return res

    def _reconciled(self, cr, uid, ids, name, args, context=None):
        wf_service = netsvc.LocalService("workflow")
        res = {}
        for rec_id in ids:
            res[rec_id] = self.test_paid(cr, uid, [rec_id])
            if res[rec_id]:
                self.write(cr, uid, rec_id, {'state': 'paid'}, context=context)
                wf_service.trg_validate(
                    uid, 'riba.distinta',
                    self.browse(cr, uid, rec_id).distinta_id.id, 'paid', cr)
        return res

    def move_line_id_payment_gets(self, cr, uid, ids, *args):
        res = {}
        if not ids:
            return res
        cr.execute('SELECT distinta_line.id, l.id '
                   'FROM account_move_line l '
                   'LEFT JOIN riba_distinta_line distinta_line ON '
                   '(distinta_line.acceptance_move_id=l.move_id) '
                   'WHERE distinta_line.id IN %s '
                   'AND l.account_id=distinta_line.acceptance_account_id',
                   (tuple(ids),))
        for r in cr.fetchall():
            res.setdefault(r[0], [])
            res[r[0]].append(r[1])
        return res

    # return the ids of the move lines which has the same account than the
    # statement whose id is in ids
    def move_line_id_payment_get(self, cr, uid, ids, *args):
        if not ids:
            return []
        result = self.move_line_id_payment_gets(cr, uid, ids, *args)
        return result.get(ids[0], [])

    def test_paid(self, cr, uid, ids, *args):
        for line in self.browse(cr, uid, ids):
            if line.state == 'unsolved':
                return False
        res = self.move_line_id_payment_get(cr, uid, ids)
        if not res:
            return False
        ok = True
        for rec_id in res:
            cr.execute(
                'select reconcile_id from account_move_line where id=%s',
                (rec_id,))
            ok = ok and bool(cr.fetchone()[0])
        return ok

    def _get_riba_line_from_move_line(self, cr, uid, ids, context=None):
        move = {}
        for line in self.pool.get('account.move.line').browse(
            cr, uid, ids, context=context
        ):
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    move[line2.move_id.id] = True
            if line.reconcile_id:
                for line2 in line.reconcile_id.line_id:
                    move[line2.move_id.id] = True
        line_ids = []
        if move:
            line_ids = self.pool.get('riba.distinta.line').search(
                cr, uid, [('acceptance_move_id', 'in', move.keys())],
                context=context)
        return line_ids

    def _get_line_from_reconcile(self, cr, uid, ids, context=None):
        move = {}
        for r in self.pool.get('account.move.reconcile').browse(
            cr, uid, ids, context=context
        ):
            for line in r.line_partial_ids:
                move[line.move_id.id] = True
            for line in r.line_id:
                move[line.move_id.id] = True
        line_ids = []
        if move:
            line_ids = self.pool.get('riba.distinta.line').search(
                cr, uid, [('acceptance_move_id', 'in', move.keys())],
                context=context)
        return line_ids

    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for riba_line in self.browse(cr, uid, ids, context=context):
            src = []
            lines = []
            if riba_line.acceptance_move_id:
                for m in riba_line.acceptance_move_id.line_id:
                    temp_lines = []
                    if m.reconcile_id and m.credit == 0.0:
                        temp_lines = map(
                            lambda x: x.id, m.reconcile_id.line_id)
                    elif m.reconcile_partial_id and m.credit == 0.0:
                        temp_lines = map(
                            lambda x: x.id,
                            m.reconcile_partial_id.line_partial_ids)
                    lines += [x for x in temp_lines if x not in lines]
                    src.append(m.id)

            lines = filter(lambda x: x not in src, lines)
            result[riba_line.id] = lines
        return result

    # TODO estendere la account_due_list per visualizzare e filtrare in base
    # alle riba ?
    _name = 'riba.distinta.line'
    _description = 'Riba details'
    _rec_name = 'sequence'

    _columns = {
        'sequence': fields.integer('Number'),
        'move_line_ids': fields.one2many(
            'riba.distinta.move.line', 'riba_line_id', 'Credit move lines'),
        'acceptance_move_id': fields.many2one(
            'account.move', 'Acceptance Entry', readonly=True),
        'unsolved_move_id': fields.many2one(
            'account.move', 'Unsolved Entry', readonly=True),
        'acceptance_account_id': fields.many2one(
            'account.account', 'Acceptance Account'),
        'amount': fields.function(
            _get_line_values, method=True, string="Amount", multi="line"),
        'bank_id': fields.many2one('res.partner.bank', 'Debitor Bank'),
        'iban': fields.related(
            'bank_id', 'iban', type='char', string='IBAN', store=False,
            readonly=True),
        'distinta_id': fields.many2one(
            'riba.distinta', 'Distinta', required=True, ondelete='cascade'),
        'partner_id': fields.many2one('res.partner', "Cliente", readonly=True),
        'invoice_date': fields.function(
            _get_line_values, string="Invoice Date", type='char', size=256,
            method=True, multi="line"),
        'invoice_number': fields.function(
            _get_line_values, string="Invoice Number", type='char', size=256,
            method=True, multi="line"),
        'due_date': fields.date("Due date", readonly=True),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('accredited', 'Accredited'),
            ('paid', 'Paid'),
            ('unsolved', 'Unsolved'),
        ], 'State', select=True, readonly=True),
        'reconciled': fields.function(
            _reconciled, string='Paid/Reconciled', type='boolean',
            store={
                'riba.distinta.line': (lambda self, cr, uid, ids, c={}: ids, [
                    'acceptance_move_id'], 50),
                'account.move.line': (_get_riba_line_from_move_line, None, 50),
                'account.move.reconcile': (_get_line_from_reconcile, None, 50),
            },
            help="It indicates that the line has been paid and the journal "
                 "entry of the line has been reconciled with one or several "
                 "journal entries of payment."),
        'payment_ids': fields.function(
            _compute_lines, relation='account.move.line', type="many2many",
            string='Payments'),
        'type': fields.related(
            'distinta_id', 'type', type='char', size=32, string='Type',
            readonly=True),
    }

    def confirm(self, cr, uid, ids, context=None):
        move_pool = self.pool.get('account.move')
        move_line_pool = self.pool.get('account.move.line')
        wf_service = netsvc.LocalService("workflow")
        for line in self.browse(cr, uid, ids, context=context):
            journal = line.distinta_id.config.acceptance_journal_id
            total_credit = 0.0
            move_id = move_pool.create(cr, uid, {
                'ref': 'Ri.Ba. %s - line %s' % (
                    line.distinta_id.name, line.sequence),
                'journal_id': journal.id,
                'date': line.distinta_id.registration_date,
            }, context=context)
            to_be_reconciled = []
            for riba_move_line in line.move_line_ids:
                total_credit += riba_move_line.amount
                move_line_id = move_line_pool.create(cr, uid, {
                    'name': (
                        riba_move_line.move_line_id.invoice and
                        riba_move_line.move_line_id.invoice.number or
                        riba_move_line.move_line_id.name
                    ),
                    'partner_id': line.partner_id.id,
                    'account_id': riba_move_line.move_line_id.account_id.id,
                    'credit': riba_move_line.amount,
                    'debit': 0.0,
                    'move_id': move_id,
                }, context=context)
                to_be_reconciled.append(
                    [move_line_id, riba_move_line.move_line_id.id])
            move_line_pool.create(
                cr, uid, {
                    'name': 'Ri.Ba. %s - line %s' % (
                        line.distinta_id.name, line.sequence),
                    'account_id': (
                        line.acceptance_account_id.id or
                        line.distinta_id.config.acceptance_account_id.id
                        # in questo modo se la riga non ha conto accettazione
                        # viene prelevato il conto in configurazione riba
                    ),
                    'partner_id': line.partner_id.id,
                    'date_maturity': line.due_date,
                    'credit': 0.0,
                    'debit': total_credit,
                    'move_id': move_id,
                }, context=context)
            move_pool.post(cr, uid, [move_id], context=context)
            for reconcile_ids in to_be_reconciled:
                move_line_pool.reconcile_partial(
                    cr, uid, reconcile_ids, context=context)
            line.write({
                'acceptance_move_id': move_id,
                'state': 'confirmed',
            })
            wf_service.trg_validate(
                uid, 'riba.distinta', line.distinta_id.id, 'accepted', cr)
        return True


class riba_distinta_move_line(orm.Model):

    _name = 'riba.distinta.move.line'
    _description = 'Riba details'
    _rec_name = 'amount'

    _columns = {
        'amount': fields.float(
            'Amount', digits_compute=dp.get_precision('Account')),
        'move_line_id': fields.many2one(
            'account.move.line', 'Credit move line'),
        'riba_line_id': fields.many2one(
            'riba.distinta.line', 'Distinta line', ondelete='cascade'),
    }
