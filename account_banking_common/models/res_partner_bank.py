#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#
import logging
from odoo import models, api, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    @api.model
    def get_payment_method_config(self, payment_method_code):
        raise UserError('Non implementato nella classe base')

    def _set_partner_bank_childs(self):
        res = []
        if not self.journal_is_wallet:
            ids = [journal.id for journal in self.journal_wallet_ids]
            domain = [
                ('journal_is_wallet', '=', True),
                ('journal_main_bank_account_id', 'in', ids)]
            res = self.search(domain)

        return res
    # end _set_partner_bank_childs

    def _is_wallet_default(self):
        if self.journal_is_wallet:
            return self.journal_is_wallet
        else:
            return False
        # end if

    # end _is_wallet_default

    @api.depends('bank_wallet_ids')
    def _has_children(self):
        if self.bank_wallet_ids:
            self.has_children = True
        else:
            self.has_children = False
        # end if
    # end _has_children

    bank_is_wallet = fields.Boolean(string="Conto di portafoglio",
                                    default=_is_wallet_default)

    bank_wallet_ids = fields.One2many(
        string='Conti bancari',
        comodel_name='res.partner.bank',
        inverse_name='bank_main_bank_account_id',
        default=_set_partner_bank_childs,
        readonly=True,)

    bank_main_bank_account_id = fields.Many2one(
        string='Conto padre',
        comodel_name='res.partner.bank',
        domain=[('bank_is_wallet', '=', False)],
        default=None
    )

    has_children = fields.Boolean(
        string="Padre",
        compute=_has_children
    )

    journal_is_wallet = fields.Boolean(
        string='Conto di portafoglio',
        related='journal_id.is_wallet'
    )

    journal_wallet_ids = fields.One2many(
        string='Conti di portafoglio',
        related='journal_id.wallet_ids'
    )

    journal_main_bank_account_id = fields.Many2one(
        string='Conto padre',
        related='journal_id.main_bank_account_id'
    )

    display_name = fields.Char(
        string='Name', compute='_compute_display_name',
    )

    @api.onchange('bank_is_wallet')
    def _onchange_bank_is_wallet(self):
        _logger.info('on change su bank_is_wallet')
        if self.journal_id:
            _logger.info('valore is_wallet res_partner_bank |{v}|'.format(v=self.bank_is_wallet))
            journal = self.env['account.journal'].search([('id', '=', self.journal_id.id)])
            journal.write({'is_wallet': self.bank_is_wallet})
            _logger.info('valore is_wallet account_journal {id} |{v}|'.format(v=journal.is_wallet, id=journal.id))
        else:
            _logger.info('valore is_wallet account_journal {id} |{v}|'.format(v=self.journal_id.is_wallet, id=self.journal_id.id))
        # end if
    # _onchange_bank_is_wallet

    def name_get(self):
        """
            Se il conto non ha banca (bank_id) e non è un conto di portafoglio (bank_is_wallet) eseguire solo super()
            altrimenti dopo
            Inizializzare descrizione vuota
            Se esiste il collegamento alla banca (bank_id) prelevare il nome della banca (max 10 caratteri, se portafoglio. altrimenti 20 caratteri) seguito da carattere " ("
            Se il conto è conto di portafoglio (bank_is_wallet)  leggere IBAN di portafoglio e prelevare primi 4 caratteri seguiti da carattere "*" e ultimi 3 caratteri seguiti da "/"
            Leggere IBAN corrente e prelevare primi 4 caratteri seguiti da carattere "*" e ultimi 3 caratteri
            Se esiste il collegamento alla banca (bank_id)  aggiungere carattere ")"

        """
        res = super().name_get()
        result = []
        for t_record in res:
            record = self.browse(t_record[0])
            if (not record.bank_id and record.bank_is_wallet is False) or \
                    record.acc_type != 'iban' or not record.acc_number:
                result.append(t_record)
            else:
                disp_name = ''

                chars_bank_name = 16 if (record.bank_id and record.bank_is_wallet) else 31

                if record.bank_id:
                    disp_name += record.bank_id.name[0:chars_bank_name] + ' ('
                # end if

                if record.bank_is_wallet and \
                        record.bank_main_bank_account_id.acc_number:
                    siz = len(record.bank_main_bank_account_id.acc_number) - 3
                    # father account
                    disp_name += record.bank_main_bank_account_id.acc_number[
                                 0:5]
                    disp_name += '*'
                    disp_name += record.bank_main_bank_account_id.acc_number[
                                 siz:]
                    disp_name += '/'
                # end if

                # current account
                disp_name += record.acc_number[0:5]
                disp_name += '*'
                siz = len(record.acc_number) - 3
                disp_name += record.acc_number[siz:]

                if record.bank_id:
                    disp_name += ')'
                # end if
                result.append((record.id, disp_name))
        return result
    # end name_get

