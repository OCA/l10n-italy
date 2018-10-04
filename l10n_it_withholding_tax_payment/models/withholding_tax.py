# Copyright 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WithholdingTaxMove(models.Model):
    _inherit = 'withholding.tax.move'

    wt_move_payment_id = fields.Many2one(
        'withholding.tax.move.payment', 'Move Payment', readonly=True)

    def unlink(self):
        for rec in self:
            if rec.wt_move_payment_id:
                raise ValidationError(
                    _(('Warning! Withholding tax move in payment {}: \
                    you can not delete it').format(
                        rec.wt_move_payment_id.name)))
        return super(WithholdingTaxMove, self).unlink()

    @api.multi
    def check_unlink(self):
        wt_moves_not_eresable = []
        for move in self:
            if move.wt_move_payment_id:
                wt_moves_not_eresable.append(move)
        if wt_moves_not_eresable:
            raise ValidationError(
                _('Warning! Withholding Tax moves in a payment: {}'.format(
                    wt_moves_not_eresable[0].sudo().wt_move_payment_id.name
                )))
        super(WithholdingTaxMove, self).check_unlink()


class WithholdingTaxMovePayment(models.Model):
    _name = 'withholding.tax.move.payment'
    _description = 'Withholding Tax Move Payment'

    @api.depends('line_ids.amount', 'line_ids.wt_move_payment_id')
    def _compute_total(self):
        for mp in self:
            tot_wt_amount = 0
            for wt_move in mp.line_ids:
                tot_wt_amount += wt_move.amount
            mp.amount = tot_wt_amount

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], 'Status', readonly=True, copy=False, default='draft')
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self:
        self.env['res.company']._company_default_get('account.account'))
    name = fields.Char('Name')
    date = fields.Char('Date')
    date_payment = fields.Date('Date Payment')
    date_start = fields.Date('Date Start', readonly=True)
    date_stop = fields.Date('Date Stop', readonly=True)
    move_id = fields.Many2one('account.move', string='Account move')
    account_id = fields.Many2one('account.account', string='Account')
    journal_id = fields.Many2one('account.journal', string='Journal')
    line_ids = fields.One2many(
        'withholding.tax.move', 'wt_move_payment_id', string='Lines')
    amount = fields.Float('WT amount', compute='_compute_total')

    def create_account_move(self):
        account_move_obj = self.env['account.move']
        for mp in self:
            if not mp.date_payment \
                    or not mp.journal_id\
                    or not mp.account_id:
                raise ValidationError(
                    _('Warning! Datas required for account move creation: \
                        Date payment, journal, account'))
            # WT Moves
            wt_move_balance = 0
            move_lines = []
            for wt_move in mp.line_ids:
                debit = 0
                credit = 0
                if wt_move.amount > 0:
                    debit = wt_move.amount
                else:
                    credit = wt_move.amount
                vals = {
                    'name': _('Withholding Tax Payment %s')
                    % wt_move.partner_id.name,
                    'account_id':
                        wt_move.withholding_tax_id.account_payable_id.id,
                    'credit': credit,
                    'debit': debit,
                }
                move_lines.append((0, 0, vals))
                # Balance
                wt_move_balance += wt_move.amount
            # WT payment
            if wt_move_balance:
                debit = 0
                credit = 0
                if wt_move_balance > 0:
                    credit = wt_move_balance
                else:
                    debit = wt_move_balance * -1
                vals = {
                    'name': _('Withholding Tax Payment'),
                    'account_id': mp.account_id.id,
                    'credit': credit,
                    'debit': debit,
                }
                move_lines.append((0, 0, vals))
            # Move create
            move = account_move_obj.create({
                'ref': _('Withholding Tax Payment'),
                'journal_id': mp.journal_id.id,
                'date': mp.date_payment,
                'line_ids': move_lines,
            })
            move.post()
            # Ref on payement
            mp.move_id = move.id

    def generate_from_moves(self, wt_moves):
        # Moves must have the same company
        if wt_moves and len(wt_moves.mapped('company_id')) > 1:
            raise ValidationError(
                _("The selected moves must have the same company!"))
        sequence_obj = self.env['ir.sequence']
        for wt_move in wt_moves:
            if wt_move.state == 'paid':
                raise ValidationError(
                    _("Wt move already paid! - %s - %s - %s")
                    % (wt_move.partner_id.name,
                       wt_move.date,
                       str(wt_move.amount)))
            if wt_move.wt_move_payment_id:
                raise ValidationError(
                    _("Wt move already in a move payment! \
                        Move paym. %s -Ref WT: %s - %s - %s")
                    % (str(wt_move.wt_move_payment_id.id),
                       wt_move.partner_id.name,
                       wt_move.date,
                       str(wt_move.amount)))
        # Create Move payment
        wt_payment = False
        if wt_moves:
            val = {
                'name': sequence_obj.get('withholding.tax.move.payment'),
                'date': fields.Date.today(),
                'line_ids': [(6, 0, wt_moves.ids)]
            }
            wt_payment = self.create(val)
            # Update ref on moves
            for wt_move in wt_moves:
                wt_move.wt_move_payment_id = wt_payment.id
        return wt_payment

    def action_confirmed(self):
        for move in self:
            if move.state in ['draft']:
                move.state = 'confirmed'
                # Wt move set to due
                for wt_move in move.line_ids:
                    wt_move.action_paid()

    def action_set_to_draft(self):
        for move in self:
            if move.state in ['confirmed']:
                move.state = 'draft'
                # Wt move set to due
                for wt_move in move.line_ids:
                    wt_move.action_set_to_draft()

    @api.multi
    def unlink(self):
        for payment in self:
            if payment.state != 'draft':
                raise ValidationError(_("You can only delete draft payments"))
        return super(WithholdingTaxMovePayment, self).unlink()
