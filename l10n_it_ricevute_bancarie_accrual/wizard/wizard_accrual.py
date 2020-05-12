from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class RibaAccreditation(models.TransientModel):
    _inherit = "riba.accreditation"
    _name = 'riba.accrual'

    @api.multi
    def _get_accrual_date(self):
        res = False
        if self._context.get('active_model', False) == 'riba.distinta':
            res = self.env['riba.distinta'].browse(
                self._context['active_id']).date_accreditation
        return res

    @api.multi
    def _get_accrual_amount(self):
        amount = 0.0
        if self._context.get('active_model', False) == 'riba.distinta.line':
            riba_lines = self.env['riba.distinta.line'].browse(
                self._context['active_ids'])
            if len(riba_lines.mapped('distinta_id.config_id')) != 1:
                raise UserError(
                    _('It is only possible to accrue one bank configuration'))
            amount = sum([l.amount for l in riba_lines if l.state == 'accredited'])
        return amount

    @api.multi
    def create_accrue_move(self):
        self.ensure_one()
        # accrue only from distinta lines
        active_ids = self.env.context.get('active_ids', False)
        if not active_ids:
            raise UserError(_('Error'), _('No active IDS found'))
        move_model = self.env['account.move']
        distinta_lines = self.env['riba.distinta.line'].browse(active_ids)
        ref = ' '.join(distinta_lines.mapped('distinta_id.name'))
        wizard = self
        if not wizard.accreditation_journal_id or not wizard.date_accrual:
            raise UserError(
                _('Missing accrual date or journal'))
        if not wizard.bank_account_id or not wizard.accreditation_account_id:
            raise UserError(_(
                'Missing bank account or accreditation account'))
        date_accrual = wizard.date_accrual

        move_vals = {
            'ref': _('Accrual C/O %s') % ref,
            'journal_id': wizard.accreditation_journal_id.id,
            'date': date_accrual,
            'line_ids': [
                (0, 0, {
                    'name': _('Credit'),
                    'account_id': wizard.acceptance_account_id.id,
                    'credit': wizard.accrual_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name': _('A/C Bank'),
                    'account_id': wizard.accreditation_account_id.id,
                    'debit': wizard.accrual_amount,
                    'credit': 0.0,
                }),
            ]
        }
        move = move_model.create(move_vals)
        vals = {
            'accrual_move_id': move.id,
            'state': 'accrued',
        }
        distinta_lines.update(vals)
        for distinta_id in distinta_lines.mapped('distinta_id'):
            if all([x == 'accrued' for x in distinta_id.mapped('line_ids.state')]):
                distinta_id.state = 'accrued'
        return {
            'name': _('C/O Accrue move'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id or False,
        }

    date_accrual = fields.Date(
        string='Accrual date',
        default=_get_accrual_date,
        oldname='date_accruement'
    )
    accrual_amount = fields.Float(
        string='Accrue amount',
        default=_get_accrual_amount,
        oldname='accruement_amount'
    )
