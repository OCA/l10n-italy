from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class RibaAccreditation(models.TransientModel):
    _inherit = "riba.accreditation"

    @api.multi
    def _get_accreditation_journal_id(self):
        if self._context.get('active_model', False) == 'riba.distinta.line':
            res = self.env['riba.configuration'].\
                get_default_value_by_list_line('accreditation_journal_id')
        else:
            res = super()._get_accreditation_journal_id()
        return res

    @api.multi
    def _get_accreditation_account_id(self):
        if self._context.get('active_model', False) == 'riba.distinta.line':
            res = (self.env['riba.configuration'].
                   get_default_value_by_list_line('accreditation_account_id'))
        else:
            res = super()._get_accreditation_account_id()
        return res

    @api.multi
    def _get_acceptance_account_id(self):
        res = self.env['riba.configuration'].\
            get_default_value_by_list_line('acceptance_account_id')
        return res

    @api.multi
    def _get_bank_account_id(self):
        if self._context.get('active_model', False) == 'riba.distinta.line':
            res = self.env['riba.configuration'].\
                get_default_value_by_list_line('bank_account_id')
        else:
            res = super()._get_bank_account_id()
        return res

    @api.multi
    def _get_bank_expense_account_id(self):
        if self._context.get('active_model', False) == 'riba.distinta.line':
            res = self.env['riba.configuration'].\
                get_default_value_by_list_line('bank_expense_account_id')
        else:
            res = super()._get_bank_expense_account_id()
        return res

    @api.multi
    def _get_accreditation_amount(self):
        amount = 0.0
        if self._context.get('active_model', False) == 'riba.distinta.line':
            riba_lines = self.env['riba.distinta.line'].browse(
                self._context['active_ids'])
            if len(riba_lines.mapped('distinta_id.config_id')) != 1:
                raise UserError(
                    _('Accreditation of only one bank configuration is possible'))
            amount = sum([l.amount for l in riba_lines if l.state == 'confirmed'])
        elif self._context.get('active_model', False) == 'riba.distinta':
            amount = super()._get_accreditation_amount()
        return amount

    @api.multi
    def skip(self):
        if self._context.get('active_model', False) == 'riba.distinta.line':
            active_ids = self._context.get('active_ids', False)
            if not active_ids:
                raise UserError(_('Error'), _('No active IDS found'))
            distinta_lines = self.env['riba.distinta.line'].browse(active_ids)
            for line in distinta_lines:
                if not line.state == "accredited":
                    line.state = 'accredited'
            # if all of line of distinta are accredited, set distinta accredited
            for distinta in distinta_lines.mapped('distinta_id'):
                if all([x == 'accredited' for x in distinta.mapped('line_ids.state')]):
                    distinta.state = 'accredited'
            return {'type': 'ir.actions.act_window_close'}
        else:
            return super().skip()

    @api.multi
    def _get_accreditation_date(self):
        res = False
        if self._context.get('active_model', False) == 'riba.distinta':
            res = self.env['riba.distinta'].browse(
                self._context['active_id']).date_accreditation
        return res

    @api.multi
    def create_move(self):
        # accredit only from distinta line
        active_ids = self.env.context.get('active_ids', False)
        if not active_ids:
            raise UserError(_('No active IDS found'))
        move_model = self.env['account.move']
        distinta_lines = self.env['riba.distinta.line'].browse(active_ids)
        distinta_ids = distinta_lines.mapped('distinta_id')
        if len(distinta_ids) != 1:
            raise UserError(_('More than 1 distinta found for this lines!'))
        distinta = distinta_ids[0]
        wizard = self
        if not wizard.accreditation_journal_id or not wizard.date_accreditation:
            raise UserError(_('Missing accreditation date or journal'))
        date_accreditation = wizard.date_accreditation or \
            fields.Date.context_today(self)

        move_vals = {
            'ref': _('C/O Credit %s') % distinta.name,
            'journal_id': wizard.accreditation_journal_id.id,
            'date': date_accreditation,
            'line_ids': [
                (0, 0, {
                    'name': _('Credit'),
                    'account_id': wizard.accreditation_account_id.id,
                    'credit': wizard.accreditation_amount,
                    'debit': 0.0,
                }),
                (0, 0, {
                    'name': _('A/C Bank'),
                    'account_id': wizard.bank_account_id.id,
                    'debit': wizard.bank_amount,
                    'credit': 0.0,
                }),
            ]
        }
        move = move_model.create(move_vals)
        vals = {
            'accreditation_move_id': move.id,
            'state': 'accredited',
        }
        distinta_lines.update(vals)
        for distinta_id in distinta_lines.mapped('distinta_id'):
            if all([x == 'accredited' for x in distinta_id.mapped('line_ids.state')]):
                distinta_id.state = 'accredited'
        return {
            'name': _('Credit Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': move.id or False,
        }

    acceptance_account_id = fields.Many2one(
        comodel_name='account.account',
        default=_get_acceptance_account_id,
        string="Ri.Ba. acceptance account")
    date_accreditation = fields.Date(
        string='Accreditation date',
        default=_get_accreditation_date)
    accreditation_amount = fields.Float(
        string='Credit amount',
        default=_get_accreditation_amount)
    bank_amount = fields.Float(
        string='Versed amount',
        default=_get_accreditation_amount)
    bank_expense_account_id = fields.Many2one(
        comodel_name='account.account',
        default=_get_bank_expense_account_id,
        string="Bank Expenses account")
    accreditation_journal_id = fields.Many2one(
        comodel_name='account.journal',
        default=_get_accreditation_journal_id,
        string="Accreditation journal",
        domain=[('type', '=', 'bank')])
    accreditation_account_id = fields.Many2one(
        comodel_name='account.account',
        default=_get_accreditation_account_id,
        string="Ri.Ba. bank account")
    bank_account_id = fields.Many2one(
        comodel_name='account.account',
        default=_get_bank_account_id,
        string="Bank account",
        domain=[('user_type_id.type', '=', 'liquidity')])
