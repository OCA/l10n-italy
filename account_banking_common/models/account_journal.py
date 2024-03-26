#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.addons.account_banking_common.utils import domains


class AccountJournal(models.Model):
    _inherit = "account.journal"

    _DEFAULT_FINANCING_PCT = {
        'invoice_amount': 80,
        'taxable_amount': 100,
    }

    @api.depends('effetti_allo_sconto')
    def _importo_effetti(self):
        for rec in self:
            if rec.effetti_allo_sconto and rec.effetti_allo_sconto.id:
                query_select_account_balance = """
                 SELECT 
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move 
                    WHERE account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state = 'posted'
                """.format(account_id=rec.effetti_allo_sconto.id)

                self.env.cr.execute(query_select_account_balance)

                anticipo = [r[0] for r in self.env.cr.fetchall()]
                rec.importo_effetti_sbf = anticipo[0]
            else:
                rec.importo_effetti_sbf = 0.0
            # end if
        # end for
    # end _importo_effetti

    @api.depends('portafoglio_sbf')
    def _impegno_effetti(self):
        for rec in self:
            if rec.portafoglio_sbf and rec.portafoglio_sbf.id:
                query_select_account_balance = """
                    SELECT 
                    SUM(debit) - SUM(credit) as balance
                    FROM account_move_line, account_move 
                    WHERE account_move_line.account_id = {account_id}
                    and account_move_line.move_id = account_move.id
                    and account_move.state = 'posted'
                """.format(account_id=rec.portafoglio_sbf.id)

                self.env.cr.execute(query_select_account_balance)

                impegno = [r[0] for r in self.env.cr.fetchall()]
                rec.impegno_effetti_sbf = impegno[0]
            else:
                rec.impegno_effetti_sbf = 0.0
            # end if
        # end for
    # end _impegno_effetti

    @api.depends('limite_effetti_sbf', 'importo_effetti_sbf')
    def _disponibilita_effetti(self):
        for rec in self:
            residuo = (
                    rec.limite_effetti_sbf -
                    (rec.importo_effetti_sbf +
                     rec.impegno_effetti_sbf)
            )

            if residuo > 0:
                rec.disponibilita_effetti_sbf = residuo
            else:
                rec.disponibilita_effetti_sbf = 0.0
            # end if
        # end for
    # end _disponibilita_effetti

    def _set_main_bank_account_id_default(self):
        return self.env['account.journal']

    # end _set_main_bank_account_id_default

    def _set_wallet_ids_default(self):
        domain = [
            ('type', 'in', ['bank', 'cash']),
            ('is_wallet', '=', True),
            ('main_bank_account_id', '=', self.id),
        ]

        return self.search(domain)

    # end _set_wallet_ids_default

    def is_wallet_default(self):
        if self.bank_account_id:
            return self.bank_account_id.bank_is_wallet
        else:
            return False
        # end if

    # end is_wallet_default

    @api.depends('wallet_ids')
    def _has_children(self):
        if self.wallet_ids:
            self.has_children = True
        else:
            self.has_children = False
        # end if

    # end _has_children

    is_wallet = fields.Boolean(string="Conto di portafoglio", default=is_wallet_default)

    wallet_ids = fields.One2many(
        comodel_name='account.journal',
        inverse_name='main_bank_account_id',
        string='Conti di portafoglio',
        default=_set_wallet_ids_default,
        readonly=True,
    )

    main_bank_account_id = fields.Many2one(
        comodel_name='account.journal',
        string='Conto padre',
        domain=[
            ('type', 'in', ['bank', 'cash']),
            ('is_wallet', '=', False),
        ],
        default=_set_main_bank_account_id_default,
    )

    has_children = fields.Boolean(string="Conto padre", compute='_has_children')

    # ACCOUNTS

    invoice_financing_evaluate = fields.Selection(
        [
            ('invoice_amount', 'percentuale su totale'),
            ('taxable_amount', 'imponibile su imponibile')
        ],
        string='Metodo calcolo anticipo fatture'
    )

    invoice_financing_percent = fields.Float(
        string='Percentuale di anticipo fatture',
        default=None,
    )

    sezionale = fields.Many2one(
        string='Sezionale',
        comodel_name='account.journal',
        domain=domains.transfer_journal,
    )

    effetti_allo_sconto = fields.Many2one(
        string='Effetti allo sconto',
        comodel_name='account.account',
        domain=lambda self: domains.domain_effetti_allo_sconto(self.env),
    )

    portafoglio_sbf = fields.Many2one(
        string='Conto portafoglio SBF',
        comodel_name='account.account',
        domain=lambda self: domains.domain_portafoglio_sbf(),
    )

    default_bank_expenses_account = fields.Many2one(
        string='Conto di default per spese bancarie',
        comodel_name='account.account',
        domain=lambda self: domains.get_bank_expenses_account(self.env),
    )

    limite_effetti_sbf = fields.Float(
        string='Affidamento bancario SBF',
        default=0.0
    )

    importo_effetti_sbf = fields.Float(
        string='Portafoglio utilizzato',
        compute='_importo_effetti'
    )

    impegno_effetti_sbf = fields.Float(
        string='Importo da presentare',
        compute='_impegno_effetti'
    )

    disponibilita_effetti_sbf = fields.Float(
        string='Disponibilità residua',
        compute='_disponibilita_effetti'
    )

    @api.model
    def create(self, vals):
        result = super().create(vals)
        self._validate_invoice_financing_percent()
        return result

    # end if

    @api.multi
    def write(self, vals):
        result = super().write(vals)

        for journal in self:
            journal._validate_invoice_financing_percent()
        # end for

        return result

    # end if

    @api.onchange('is_wallet')
    def _on_change_is_wallet(self):
        if not self.is_wallet:
            # empty parent
            if self.main_bank_account_id:
                self.main_bank_account_id = self._set_main_bank_account_id_default()
            # end if
        # end if
        if self.bank_account_id:
            bank_account = self.env['res.partner.bank'].browse(self.bank_account_id.id)
            bank_account.write({'bank_is_wallet': self.is_wallet})
        # end if

    # end _on_change_portafolio_account

    @api.model
    def get_payment_method_config(self):
        return {
            'sezionale': self.sezionale,
            'transfer_journal': self.sezionale,
            'transfer_account': self.portafoglio_sbf,
            'banca_conto_effetti': self.portafoglio_sbf,
            'conto_effetti_attivi': self.portafoglio_sbf,
            'effetti_allo_sconto': self.effetti_allo_sconto,
            'conto_spese_bancarie': self.default_bank_expenses_account,
        }

    @api.onchange('invoice_financing_evaluate')
    def _onchange_invoice_financing_evaluate(self):

        method = self.invoice_financing_evaluate
        pct_default = self._DEFAULT_FINANCING_PCT.get(method, 0)
        pct_set = bool(self.invoice_financing_percent)

        if not pct_set or not method:
            self.invoice_financing_percent = pct_default
        # end if
    # _onchange_invoice_financing_evaluate

    @api.model
    def _validate_invoice_financing_percent(self):

        ife_set = self.invoice_financing_evaluate is not False
        pct_set = self.invoice_financing_percent not in [False, 0]

        if ife_set and not pct_set:
            raise UserError(
                'Percentuale anticipo non impostata! '
                'La percentuale deve essere maggiore di zero'
            )
        # end if
    # end _validate_invoice_financing_percent
