# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).

from odoo import fields, api, models, _
from odoo.exceptions import UserError

    # ===================================== #
    #       CLASS RIBA EFFECT RESULT       #
    # ===================================== #
class RibaEffectResult(models.TransientModel):

    _name = "riba.effect.result"
    _description =''''Wizard which let the user to 
                choose if a effect is paid or unsolved
                '''
    # ============================================ #
    #       FUNCTION COMPUTE & DEFAULT          #
    # ============================================ #
    
    @api.model
    def default_get(self, default_fields):
        res = super(RibaEffectResult,self).default_get(default_fields)
        if self._context.get('active_model',False) == 'riba.distinta.line':
            res['riba_distinta_line_ids'] = [(6,0,self._context.get('active_ids',[]))]
        return res
       
            
        
    
    #@api.depends('state')
    #def _compute_riba_distinta_line_ids(self):
        #'''
            #@summary: Write in riba_distinta_line_ids
            #field the riba.distinta.line which the user choose
        #'''
        #if (self._context.get('active_model',False) and
            #self._context.get('active_model',False) == 'riba.distinta.line'):
            #self.riba_distinta_line_ids = [(6,0,self._context.get('active_ids',[]))]
        #else:
            #if self._context.get('riba_distinta_line_ids',False):
                #self.riba_distinta_line_ids = [
                    #(6,0,self._context.get('riba_distinta_line_ids',[[],[],[]])[0][2])
                    #]
            #else:
                #self.riba_distinta_line_ids = [(6,0,[])]

    @api.model
    def _get_unsolved_journal_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('unsolved_journal_id')

    @api.model
    def _get_effects_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('acceptance_account_id')

    @api.model
    def _get_riba_bank_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('accreditation_account_id')

    @api.model
    def _get_overdue_effects_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('overdue_effects_account_id')

    @api.model
    def _get_bank_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('bank_account_id')

    @api.model
    def _get_bank_expense_account_id(self):
        return self.env[
            'riba.configuration'
        ].get_default_value_by_list_line('protest_charge_account_id')

    # ======================================= #
    #          FUNCTION ONCHANGE            #
    # ======================================= #

    api.onchange('bank_expense_account_id','expense_amount')
    def _onchange_account_id_expense_amount(self,new_account,new_amount):
        '''
            @summary: function  which update the wizard view when
            the fields above have been changed. If the field 'expense amount'
            has been changed, 
            the total amount will change as well and it will
            suggest a bank amount in relation with the new value.
        '''
        value = {}
        if self.id:
            note_ids = []
            for WIline in self.accout_move_detail_table:
                if WIline.type_of_line == 'expense':
                    WIline.write({
                         'debit' : new_amount,
                         })
                    # ===================================== #
                    #    FUNCTION get_new_total                #
                    # ===================================== #
                    new_total = self.get_new_total()
                    note_ids.append((1,WIline.id,{
                                    'debit' : new_amount,
                                    'account_id' : new_account,
                                    }
                                    ))
                elif WIline.type_of_line == 'bank':
                    note_ids.append((1,WIline.id,{'credit' : new_total}))
                else:
                    note_ids.append((1,WIline.id,{}))
                    
            value.update(accout_move_detail_table=note_ids)
            value.update({
                'bank_amount' : new_total,
                })
            return {'value':value}

    api.onchange('bank_account_id')
    def _onchange_account_id_bank(self,new_account):
        '''
            @summary: function which update in the 
            resume table of the wizard
            the field account of the bank, if it has been changed 
        '''
        value = {}
        if self.id:
            note_ids = []
            for WIline in self.accout_move_detail_table:
                if WIline.type_of_line == 'bank':
                    note_ids.append((1,WIline.id,{'account_id' : new_account}))
                else:
                    note_ids.append((1,WIline.id,{}))
            value.update(accout_move_detail_table=note_ids)
            return {'value':value}
    
    api.multi
    def get_new_total(self):
        '''
            @return: compute and return the sum of all the debts
            in the table
        '''
        debit = 0
        for WIline in self.accout_move_detail_table:
            if WIline.type_of_line != 'bank':
                debit += WIline.debit
        return debit
    # =================== #
    #       FIELDS         #
    # =================== #

    state = fields.Selection(
        (
            ('draft', 'draft'),
            ('paid', 'paid'),
            ('unsolved','unsolved'),
        ),
        default='draft')

    #riba_distinta_line_ids = fields.Many2many(
        #'riba.distinta.line', string="riba distinta lines linked", readonly=True,
        #compute='_compute_riba_distinta_line_ids', store=True)
    
    riba_distinta_line_ids = fields.Many2many(
        'riba.distinta.line', string="riba distinta lines linked", readonly=True,
        relation="wizard_effect_dis_line_rel", column1="wizard_effect_id",
        column2="distinta_line_id")

    accout_move_detail_table = fields.One2many(
        'wizard.linked_ribaeffectresult', 'effect_result_id',
        string = 'Credit and Debit of each partner and Bank')
    
    unsolved_journal_id = fields.Many2one(
        'account.journal', 'Unsolved journal', domain=[('type', '=', 'bank')],
        default=_get_unsolved_journal_id)
    
    effects_account_id = fields.Many2one(
        'account.account', 'Effects account', 
        domain=[('internal_type', '=', 'receivable')], 
        default=_get_effects_account_id)
    
    effects_amount = fields.Float('Effects amount')
    
    riba_bank_account_id = fields.Many2one(
        'account.account', 'Ri.Ba. bank account', 
        default=_get_riba_bank_account_id)
    
    riba_bank_amount = fields.Float('Ri.Ba. bank amount')
    
    overdue_effects_account_id = fields.Many2one(
        'account.account', 'Overdue Effects account',
        domain=[('internal_type', '=', 'receivable')], 
        default=_get_overdue_effects_account_id)
    
    overdue_effects_amount = fields.Float('Overdue Effects amount')
    
    bank_account_id = fields.Many2one(
        'account.account', 'Bank account', 
        domain=[('internal_type', '=', 'liquidity')], default=_get_bank_account_id)
    
    bank_amount = fields.Float(string='Taken amount')
    
    bank_expense_account_id = fields.Many2one(
        'account.account', 'Bank Expenses account',
        default= _get_bank_expense_account_id)
    
    expense_amount = fields.Float(
        string='Expenses amount', 
        help = '''You can change the total value 
            automatically by change this field''')


    # ========================= #
    #         FUNCTIONS         #
    # ========================= #
    
    # =================================== #
    #   FUNCTIONS TO EDIT THE WIZARD   #
    # =================================== #

    @api.multi
    def action_payment_executed(self):
        '''
            @note: This function allow to change the 
            state of the class in paid
        '''
        self.write({'state' : 'paid'})
        partner_INFO = self.get_detail_riba_partner_INFO()
        totale_importo = self.create_link_to_Linked_Wiz_RiBa(partner_INFO,'paid')
        self.write_in_amount_related_fields(totale_importo)
        return {
            'name': _('Unsolved Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'riba.effect.result',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }
    
    @api.multi
    def action_unsolved_payment(self):
        '''
            @summary: write in field state unsolved
            @return: the same wizard view to get 
            more information about the unsolved payments
        '''
        self.write({'state' : 'unsolved'})
        partner_INFO = self.get_detail_riba_partner_INFO()
        totale_importo = self.create_link_to_Linked_Wiz_RiBa(partner_INFO,'unsolved')
        self.write_in_amount_related_fields(totale_importo)
        return {
            'name': _('Unsolved Payment'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'riba.effect.result',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    @api.multi
    def get_detail_riba_partner_INFO(self):
        '''
            @return: A list of tuple which is contained all the information in.
        '''
        
        # ==================================================== #
        # FUNCTION : get_partner_detail()                            #
        # FUNCTION : organize_partner_info                          #
        # @param:([(partner_id.id,partner_debit),])                       #
        # =================================================== #
        
        partner_amount = self.get_partner_detail()
        partner_amount = self.organize_partner_info(partner_amount)
        
        return partner_amount

    @api.multi
    def create_link_to_Linked_Wiz_RiBa(self,partner_INFO,situation='paid'):
        '''
            @summary: Create in the support class for this wizard
            all the information about the partner
            @return: totale la somma di tutti i debiti
        '''
        totale = 0
        # =========================================================== #
        #             Create lines referred to partners               #
        # =========================================================== #
        
        for partner_amount in partner_INFO:
        # ========================================================== #
        # FUNCTION : get_dictionary_to_create                        #
        # @param:(partner_id.id,account_id.id,debit,credit,          #
        #            type_of_line)                                   #
        # ========================================================== #
            data = self.get_dictionary_to_create(partner_amount[0],False,
                                                 partner_amount[1],0.00,'partner')
            totale += partner_amount[1]
            self.env['wizard.linked_ribaeffectresult'].create(data)
        
        # =================================================== #
        #        Create lines referred to bank and expense            #
        # ================================ =================== #
        
        if situation == 'unsolved':
            totale += self.expense_amount
            data = self.get_dictionary_to_create(False,self.bank_expense_account_id.id,
                                                 self.expense_amount,0.00,'expense')
            self.env['wizard.linked_ribaeffectresult'].create(data)
        
        data = self.get_dictionary_to_create(False,self.bank_account_id.id,0.00,totale,'bank')
        self.env['wizard.linked_ribaeffectresult'].create(data)
            
        
        return totale
    
    @api.multi
    def write_in_amount_related_fields(self,totale_importo):
        '''
            @summary: write in the fields of amount
            all the amount. This function replace the old
            function  _get_effects_amount in the previous wizard
        '''
        self.write({
            'effects_amount' : totale_importo,
            'riba_bank_amount' : totale_importo,
            'overdue_effects_amount': totale_importo,
            'bank_amount' : totale_importo,
            })
        
        return True

    @api.multi
    def get_partner_detail(self):
        '''
            @return: a list of tuple about all the distinta line
            selected, it shows the partner and his amount
        '''
        list_of_data = []
        for De_line in self.riba_distinta_line_ids:
            list_of_data.append((De_line.partner_id.id,De_line.amount,))
        return list_of_data

    @api.multi
    def organize_partner_info(self,list_to_organize):
        '''
            @summary: organize a len = 2 list of tuple 
            adding the second member to the second member 
            of each tupla which has the same first member
            @return: a list of tuple
        '''
        organized_list = []
        for INfo in list_to_organize:
            if len(INfo) != 2 or type(INfo[1]) != float:
                continue
            indice = 0
            new_data = INfo
            for ordered_data in organized_list:
                if INfo[0] == ordered_data[0]:
                    new_data = (INfo[0],INfo[1] + ordered_data[1])
                    del organized_list[indice]
                indice += 1
            organized_list.append(new_data)
        
        return organized_list
            
    @api.multi
    def get_dictionary_to_create(self,partner,account,debit,credit,type):
        return {
            'partner_id' : partner,
            'account_id' :account,
            'debit' : debit,
            'credit' : credit,
            'type_of_line' : type,
            'effect_result_id' : self.id,
            }

    # ========================================================= #
    #       FUNCTION TO SKIP THE  ACCOUNT MOVEMENT          #
    # ========================================================= #
    @api.multi
    def skip(self):
        '''
        @summary: function to change the state of each distinta line in
        unsolved. With this function the account move will not be created.
        '''
        for line in self.riba_distinta_line_ids:
            line.state = 'unsolved'
            line.distinta_id.signal_workflow('unsolved')
        return {'type': 'ir.actions.act_window_close'}

    # ========================================================== #
    #       FUNCTION TO CREATE AN ACCOUNT MOVEMENT          #
    # ========================================================== #
    @api.multi
    def create_new_movement(self):
        '''
        @summary: Firstable all the riba distinta line will be checked, to 
        verify their state is in accredited, and all the fields which are 
        mandatory are not NULL.
        @summary: Second a new account move will be created: the new
        account move will contain all the effects of a single unsolved moved,
        but the overdue and the bank lines will be the sum of each 
        movement
        @summary: Third, all the correct lines in this account move will be 
        reconciled with the correct lines of the acceptance move
        @summary: In the end, all the invoice involved will be linked to this
        movement
        @return: the current view of the account move created in the first 
        operation
        '''
        
        self.check_in_function()

        # ================================= #
        #       ACCOUNT MOVE CREATION    #
        # ================================= #
        data_line_ids = [
            (0,0,{
                'name':  _('Bank'),
                'account_id': self.bank_account_id.id,
                'credit': self.bank_amount,
                'debit': 0.0,
                }),
            (0,0,{
                'name':  _('Expenses'),
                'account_id': self.bank_expense_account_id.id,
                'debit': self.expense_amount,
                'credit': 0.0,
                }),
        ]
        reference = 'Unsolved '
        for DI_line in self.riba_distinta_line_ids:
            reference += 'Ri.Ba. %s - line %s ' %(
                DI_line.distinta_id.name, DI_line.sequence)
            #ricordarsi di mettere unsolved_distinta_line_id nella creazione
            lines_to_create = self.prepare_move_lines(DI_line)
            data_line_ids.extend(lines_to_create)
        move_vals = {
            'ref' : _(reference),
            'journal_id' : self.unsolved_journal_id.id,
            'line_ids' : data_line_ids,
            }
        new_account_move = self.env['account.move'].create(move_vals)

        # ================================= #
        #       RECONCILE OPERATION        #
        # ================================= #
        move_line_model = self.env['account.move.line']
        invoice_model = self.env['account.invoice']
        for move_line in new_account_move.line_ids:
            to_be_reconciled = []
            DI_line = move_line.unsolved_distinta_line_id
            if move_line.account_id == self.effects_account_id:
                to_be_reconciled.append(move_line.id)

                for ac_move_line in DI_line.acceptance_move_id.line_ids:
                    if (ac_move_line.account_id.id == self.effects_account_id.id):
                        to_be_reconciled.append(ac_move_line.id)

                DI_line.write({
                    'unsolved_move_id': new_account_move.id,
                    'state': 'unsolved',
                    })
                to_be_reconciled_lines = move_line_model.with_context(
                    {'unsolved_reconciliation': True}).browse(to_be_reconciled)
                to_be_reconciled_lines.reconcile()
                DI_line.distinta_id.signal_workflow('unsolved')

        # ================================= #
        #       LINK INVOICE OPERATION     #
        # ================================= #
            if move_line.account_id.id == self.overdue_effects_account_id.id:
                for riba_move_line in DI_line.move_line_ids:
                    invoice_ids = []
                    if riba_move_line.move_line_id.invoice_id:
                        invoice_ids = [
                            riba_move_line.move_line_id.invoice_id.id
                        ]
                    elif riba_move_line.move_line_id.unsolved_invoice_ids:
                        invoice_ids = [
                            i.id for i in
                            riba_move_line.move_line_id.unsolved_invoice_ids
                        ]
                    invoice_model.browse(invoice_ids).write({
                        'unsolved_move_line_ids': [(4, move_line.id)],
                    })

        return {
                'name': _('Operation paid'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': new_account_move.id,
            }
    
    @api.multi
    def check_in_function(self):
        '''
        @summary: This function check if all the mandatory fields are 
        valorized
        '''
        if (
            not self.unsolved_journal_id or
            not self.effects_account_id or
            not self.riba_bank_account_id or
            not self.overdue_effects_account_id or
            not self.bank_account_id or
            not self.bank_expense_account_id
        ):
            raise UserError(_('Every account is mandatory'))
        return True
    
    @api.multi
    def prepare_move_lines(self,DI_line):
        return [
                (0, 0, {
                    'name':  _('Effects'),
                    'account_id': self.effects_account_id.id,
                    'partner_id': DI_line.partner_id.id,
                    'credit': DI_line.amount,
                    'debit': 0.0,
                    'unsolved_distinta_line_id' : DI_line.id,
                }),
                (0, 0, {
                    'name':  _('Ri.Ba. Bank'),
                    'account_id': self.riba_bank_account_id.id,
                    'debit': DI_line.amount,
                    'credit': 0.0,
                    'unsolved_distinta_line_id' : DI_line.id,
                }),
                (0, 0, {
                    'name':  _('Overdue Effects'),
                    'account_id': self.overdue_effects_account_id.id,
                    'debit': DI_line.amount,
                    'credit': 0.0,
                    'partner_id': DI_line.partner_id.id,
                    'date_maturity': DI_line.due_date,
                    'unsolved_distinta_line_id' : DI_line.id,
                }),
            ]
    # ================================================ #
    #  CLASS SUPPORT TO WIZARD RIBA EFFECT RESULT  #
    # ================================================ #
class WizardLinked_RibaEffectResult(models.TransientModel):
    
    _name='wizard.linked_ribaeffectresult'
    _description='''This class is used to support the wizard 
                RibaEffectResult in order to show the partner 
                selected and their situation'''
    
    # ==================================================== #
    #                       FIELDS                             #
    # ==================================================== #
    
    effect_result_id = fields.Many2one('riba.effect.result')
    partner_id = fields.Many2one('res.partner',
                                 string='Partner')
    account_id = fields.Many2one('account.account',
                                 string="Account")
    debit = fields.Float(string = 'Debit')
    credit = fields.Float(string = 'Credit')
    
    type_of_line = fields.Selection(
        (
            ('partner', 'Partner'),
            ('expense', 'Expense'),
            ('bank','Bank'),
        ),
        )
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    unsolved_distinta_line_id = fields.Many2one(
        comodel_name='riba.distinta.line', string='Dettaglio RiBa Unsolved')
    
class RibaListLine(models.Model):
    _inherit = "riba.distinta.line"

    unsolve_line_ids = fields.One2many(
        'account.move.line', inverse_name='unsolved_distinta_line_id', 
        string='Credit move lines')
