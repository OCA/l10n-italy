# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).


from odoo import fields, api, models, _
from odoo.exceptions import UserError



    # ===================================================================================== #
    #                           CLASS RIBA EFFECT RESULT                                   #
    # ===================================================================================== #
class RibaEffectResult(models.TransientModel):

    _name = "riba.effect.result"
    _description ="Wizard which let the user to choose if a effect is paid or unsolved"
    
    # ===================================================================================== #
    #                           FUNCTION COMPUTE & DEFAULT                                  #
    # ===================================================================================== #
    
    @api.depends('state')
    def _compute_riba_distinta_line_ids(self):
        '''
            @summary: Write in riba_distinta_line_ids
            field the riba.distinta.line which the user choose
        '''
        if (self._context.get('active_model',False) and
            self._context.get('active_model',False) == 'riba.distinta.line'):
            self.riba_distinta_line_ids = [(6,0,self._context.get('active_ids',[]))]
        else:
            if self._context.get('riba_distinta_line_ids',False):
                self.riba_distinta_line_ids =[(6,0,self._context.get('riba_distinta_line_ids',
                                                                     [[],[],[]])[0][2])]
            else:
                self.riba_distinta_line_ids = [(6,0,[])]

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

    # ===================================================================================== #
    #          FUNCTION ONCHANGE (it will be only used in an unsolved situation)            #
    # ===================================================================================== #

    api.onchange('bank_expense_account_id','expense_amount')
    def _onchange_account_id_expense_amount(self,new_account,new_amount):
        '''
            @summary: function  which update the wizard view when
            the fields above have been changed. If the field 'expense amount'
            has been changed, the total amount will change as well and it will
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
                    #    FUNCTION get_new_total             #
                    # ===================================== #
                    new_total = self.get_new_total()
                    note_ids.append((1,WIline.id,{'debit' : new_amount,'account_id' : new_account}))
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
            @summary: function which update in the resume table of the wizard
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
    # ===================================================================================== #
    #                                      FIELDS                                           #
    # ===================================================================================== #

    state = fields.Selection(
        (
            ('draft', 'draft'),
            ('paid', 'paid'),
            ('unsolved','unsolved'),
        ),
        default='draft')

    riba_distinta_line_ids = fields.Many2many('riba.distinta.line',
                                              string="riba distinta lines linked",
                                              readonly=True,
                                              compute='_compute_riba_distinta_line_ids')
    
    accout_move_detail_table = fields.One2many('wizard.linked_ribaeffectresult',
                                               'effect_result_id',
                                               string = 'Credit and Debit of each partner and Bank')
    
    unsolved_journal_id = fields.Many2one('account.journal',
                                          'Unsolved journal',
                                          domain=[('type', '=', 'bank')],
                                          default=_get_unsolved_journal_id)
    
    effects_account_id = fields.Many2one('account.account',
                                         'Effects account',
                                         domain=[('internal_type', '=', 'receivable')],
                                         default=_get_effects_account_id)
    
    effects_amount = fields.Float('Effects amount')
    
    riba_bank_account_id = fields.Many2one('account.account',
                                           'Ri.Ba. bank account',
                                           default=_get_riba_bank_account_id)
    
    riba_bank_amount = fields.Float('Ri.Ba. bank amount')
    
    overdue_effects_account_id = fields.Many2one('account.account',
                                                 'Overdue Effects account',
                                                 domain=[('internal_type', '=', 'receivable')],
                                                 default=_get_overdue_effects_account_id)
    
    overdue_effects_amount = fields.Float('Overdue Effects amount')
    
    bank_account_id = fields.Many2one('account.account',
                                      'Bank account',
                                      domain=[('internal_type', '=', 'liquidity')],
                                      default=_get_bank_account_id)
    
    bank_amount = fields.Float(string='Taken amount')
    
    bank_expense_account_id = fields.Many2one('account.account',
                                              'Bank Expenses account',
                                              default=_get_bank_expense_account_id)
    
    expense_amount = fields.Float(string='Expenses amount',
                                  help = '''You can change the total value 
                                  automatically by change this field''')


    # ===================================================================================== #
    #                                     FUNCTIONS                                         #
    # ===================================================================================== #
    
    # ===================================================================================== #
    #                              FUNCTIONS TO EDIT THE WIZARD                             #
    # ===================================================================================== #

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
        
        # ========================================================== #
        # FUNCTION : get_partner_detail()                            #
        # FUNCTION : organize_partner_info                           #
        # @param:([(partner_id.id,partner_debit),])                  #
        # ========================================================== #
        
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
        
        # =========================================================== #
        #        Create lines referred to bank and expense            #
        # =========================================================== #
        
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
    # ===================================================================================== #
    #                     FUNCTION TO CREATE AN ACCOUNT MOVEMENT                            #
    # ===================================================================================== #
    
    @api.multi
    def create_new_movement(self):
        '''
            @summary: This function is divided in three operation
                1 create a new account move
                2 reconcile all the lines which has the same SBF account
                3 link the overdue effects movement to all the invoice involved
            @return: the wizard of the account move created in the first operation
        '''
        keyword = self._context.get('keyword',False)
        self.check_in_function(keyword)
        
        # ========================================================== #
        # FUNCTION get_ref_and_unique_partner                        #
        # @return a list of two arguments:the first one is the       #
        #    record of the partner (if unique) and the second one    #
        #    is the reference to write in the account move           #
        # ========================================================== # 

        data_get = self.get_ref_and_unique_partner(keyword)
        new_account_move = self.create_new_account_move(data_get,keyword)
        self.reconcile_SBF_lines(new_account_move,data_get[0],keyword)
        if keyword == 'paid':
            self.link_all_invoice_involved_paid()
        else:
            self.link_all_invoice_involved_unsolved(new_account_move)
        return {
                'name': _('Operation paid'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.move',
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': new_account_move.id,
            }


    # ===================================================================================== #
    #                  FUNCTIONS USED IN BOTH PAID AND UNSOLVED MOVEMENT                    #
    # ===================================================================================== #

    @api.multi
    def check_in_function(self,keyword):
        '''
            @param keyword: 'unsolved' or 'paid' 
            @summary: This function is created to check all the
            data before the creation of the account movement and
            the reconciliation
        '''
        # ======================================== #
        #    Check if all the fields in the wizard #
        #    is compiled                           #
        # ======================================== #
        messaggio = ''
        if (
            not self.unsolved_journal_id or
            not self.effects_account_id or
            not self.riba_bank_account_id
        ):
            messaggio = 'Every account in this wizard is mandatory\n'
        
        if (keyword=='unsolved' and
            (not self.overdue_effects_account_id or
            not self.bank_account_id or
            not self.bank_expense_account_id)
            ):
            messaggio = 'Every account in this wizard is mandatory\n'
        # ======================================== #
        #    Check if all the riba line linked is  #
        #    accepted or accredited                #
        # ======================================== #
        indice = 0
        for DIline in self.riba_distinta_line_ids:
            indice += 1
            if DIline.state != 'accredited':
                messaggio += 'The line %s must be in state accredited\n' %(indice)
        
        if messaggio != '':
            messaggio = 'Attention please!!\n' + messaggio
            raise UserError(messaggio)
                
        return True
    
    @api.multi
    def get_ref_and_unique_partner(self,keyword):
        
        # ======================================== #
        #      Check if exist only one partner     #
        # ======================================== # 
        
        data = []
        indice = 0
        for DE_line in self.accout_move_detail_table:
            if DE_line.type_of_line == 'partner':
                indice += 1
        
        # ======================================== #
        #   Write or not partner and reference     #
        # ======================================== #
        
        ref_word = keyword.capitalize() + ' Ri.Ba.'
        reference = _(ref_word)
        partner_id = False
        if indice == 1:
            partner_id = self.riba_distinta_line_ids[0].partner_id or False
            if partner_id:
                reference = _(ref_word + ' - %s') % (partner_id.name)
        
        data.append(partner_id)
        data.append(reference)
        return data
    
    @api.multi
    def create_new_account_move(self,data_get,keyword):
        '''
            @param keyword: 'unsolved' or 'paid'
            @summary: this function create a single account move
            referred to all the riba distianta lines selected in 
            the wizard
            @return: the record of the new account move created
        '''
        journal_id = self.unsolved_journal_id.id
        partner = data_get[0]
        reference = data_get[1]
       
        # ========================================== #
        # Preparation of account move line in order  #
        # to create account move                     #
        #                                            #
        # FUNCTION prepare_account_move_line         #
        # @param(partner_id,keyword)                 #
        # ========================================== #
        
        data_line_ids = self.prepare_account_move_lines(partner,keyword)
        
        # ========================================== #
        #             Create account move            #
        # ========================================== #
        
        move_vals = {
            'ref' : reference,
            'journal_id' : journal_id,
            'line_ids' : data_line_ids,
            }
        
        new_account_move = self.env['account.move'].create(move_vals)
        return new_account_move
    
    @api.multi
    def reconcile_SBF_lines(self,new_account_move,partner,keyword):
        '''
            @summary: This function reconcile the account move line 
            which has the SBF account with all the movement lines in the
            distinta line which has SBF account. The values of the new
            account move line should be the same as the sum of all the 
            other distinta lines
            @param new_account_move: is the record of the account move
            just created in the operation before
            @param partner_id: it depends of the function which call this one
            it could be a record referred to res partner or a False
            @param keyword: 'unsolved' or 'paid'
        '''
        # ===================================================== #
        # FUNCTION get_right_account                            #
        # @ note: the one2many MUST have a field account_id     #
        # @ param(one2many fields, id of the account)           #
        # ===================================================== #
        
        # ====================================================== #
        # Get the new move line with the account referred to SBF #
        # ====================================================== #
        to_be_reconciled = []
        sbf_new_move_id = self.get_right_account(new_account_move.line_ids,
                                                 self.effects_account_id.id)
        to_be_reconciled.append(sbf_new_move_id)
        
        # ====================================================== #
        # Get all the line in distinta line acceptance movement  #
        #        with the account referred to SBF                #
        # ====================================================== #
        indice = 0
        for DIline in self.riba_distinta_line_ids:
            indice+=1
            if not DIline.acceptance_move_id:
                messaggio = '''Attention please!!\n Check the acceptance 
                move of the line %s''' %(indice)
                raise UserError(messaggio)
            sbf_diline_id = self.get_right_account(DIline.acceptance_move_id.line_ids,
                                                   self.effects_account_id.id)
            to_be_reconciled.append(sbf_diline_id)
            
        # ======================================================= #
        #         Reconciliation of all the lines                 #
        # ======================================================= #
        if keyword == 'unsolved':
            to_be_reconciled_lines = self.env['account.move.line'].with_context(
                {'unsolved_reconciliation': True}).browse(to_be_reconciled)
        else:
            to_be_reconciled_lines = self.env['account.move.line'].browse(
                to_be_reconciled)
        
        
        # ======================================================= #
        #    Unlink all the partner id from Riba line             #
        #    if a unique partner doesn't exist                    #
        #    otherwise is not possible to reconcile               #
        # ======================================================= # 
        if not partner:
            partner_dictionary = {}
            for ACMV_line in to_be_reconciled_lines:
                partner_dictionary[ACMV_line] = ACMV_line.partner_id
                ACMV_line.partner_id = False
            
        to_be_reconciled_lines.reconcile()
        
        # ====================================================== #
        #    Recreate the link to all partner id in the account  #
        #    move line before                                    #
        # ====================================================== #
        if not partner:
            for ACMV_line in to_be_reconciled_lines:
                if partner_dictionary[ACMV_line]:
                    ACMV_line.partner_id = partner_dictionary[ACMV_line].id
        return True
    

    
    @api.multi
    def prepare_account_move_lines(self,partner_id,keyword):
        '''
            @summary: This function has been made just to create the
            account move line in the account move create operation.
            It only check if there is a partner id to write, else it write 
            False
            @param partner_id: it depends of the function which call this one
            it could be a record referred to res partner or a False
            @param keyword: 'paid' or 'unsolved'
        '''
        wizard = self
        if partner_id:
            partner_id = partner_id.id
        
        data = [
            (0,0,{
                'name': _('Effects'),
                'account_id': wizard.effects_account_id.id,
                'partner_id': partner_id,
                'credit': wizard.effects_amount,
                'debit': 0.0,
                }),
            (0,0,{
                'name':  _('Ri.Ba. Bank'),
                'account_id': wizard.riba_bank_account_id.id,
                'debit': wizard.riba_bank_amount,
                'credit': 0.0,                
                }),
            ]
        if keyword == 'unsolved':
            extra_data = [
                (0,0,{
                'name':  _('Overdue Effects'),
                'account_id': wizard.overdue_effects_account_id.id,
                'debit': wizard.overdue_effects_amount,
                'credit': 0.0,
                'partner_id': partner_id,
                }),
            (0,0,{
                'name':  _('Bank'),
                'account_id': wizard.bank_account_id.id,
                'credit': wizard.bank_amount,
                'debit': 0.0,
                }),
            (0,0,{
                'name':  _('Expenses'),
                'account_id': wizard.bank_expense_account_id.id,
                'debit': wizard.expense_amount,
                'credit': 0.0,
                }),
            ]
            for extra in extra_data:
                data.append(extra)
        
        return data
    
    @api.multi
    def get_right_account(self,records_with_account_id,account_to_find):
        '''
            @attention: records_with_account_id MUST have a field named
            account_id
            @summary: This function find the record in a list of record 
            whose account is the same as the one given by the user
            @param records_with_account_id: list of record in which search
            the right account
            @param account_to_find: account given by the user
        '''
        result = []
        for record in records_with_account_id:
            if record.account_id.id == account_to_find:
                result.append(record.id)
        if len(result) != 1:
            message = '''Attention please!!\n There is a problem in the configuration of SBF\n
                         Or some account is different from the 
                         configuration in the Riba Line selected\n
                         The reconciliation will be impossible'''
            raise UserError (message)
        return result[0]

    # ===================================================================================== #
    #                     FUNCTION ONLY USED IN A PAID MOVEMENT                             #
    # ===================================================================================== #

    api.multi
    def link_all_invoice_involved_paid(self):
        '''
            @summary: This function only set lines' state and
            distinta's state as paid
        '''
        # ====================================================== #
        # The creation of all the link should be automatic when  #
        # the reconciliation has done.                           #
        # Only set the field as paid in distinta line and        #
        # has remained to do                                     #
        # ====================================================== #
        for DIline in self.riba_distinta_line_ids:
            DIline.write({
                'state': 'paid',
            })
            DIline.distinta_id.signal_workflow('paid')
        
        return True
    
        
    # ===================================================================================== #
    #                     FUNCTION ONLY USED IN AN UNSOLVED MOVEMENT                        #
    # ===================================================================================== #
  
    @api.multi
    def link_all_invoice_involved_unsolved(self,new_account_move):
        '''
            @summary: This function link all the invoice involved in 
            this operation to the overdue movement generated two operation
            before. And link all the riba lines selected in the wizard to the new
            account move
            @param new_account_move: is the record of the account move
            just created in the operation before
        '''
        # ====================================================== #
        # Get the new move line with the account referred to     #
        #                Overdue effects                         #
        # ====================================================== #
        
        overdue_new_move_id = self.get_right_account(new_account_move.line_ids,
                                                     self.overdue_effects_account_id.id)

        # ====================================================== #
        # Find the id of all the invoice linked to this          #
        # operation                                              #
        # ====================================================== #
        
        for DIline in self.riba_distinta_line_ids:
        # ====================================================== #
        # Write the linked account move to all the Distinta      #
        # linked to the line and set the state as unsolved       #
        # for all the distinta line and the distinta involved    #
        # ====================================================== #
            DIline.write({
                'unsolved_move_id': new_account_move.id,
                'state': 'unsolved',
            })
            DIline.distinta_id.signal_workflow('unsolved')
            for DIMV_line in DIline.move_line_ids:
                invoice_ids = []
        # ====================================================== #
        #    Try to get a direct invoice linked                  #
        # ====================================================== #
                if (DIMV_line.move_line_id and 
                    DIMV_line.move_line_id.invoice_id):
                    invoice_ids.append(DIMV_line.move_line_id.invoice_id.id)
        # ====================================================== #
        #    Try to get an unsolved invoice linked               #
        # ====================================================== #                   
                elif (DIMV_line.move_line_id and 
                    DIMV_line.move_line_id.unsolved_invoice_ids):
                    invoice_ids = [
                            i.id for i in
                            DIMV_line.move_line_id.unsolved_invoice_ids
                        ]
        # ====================================================== #
        #     Write in the record of the invoices found the      #
        #     link to the unsolved movement                      #
        # ====================================================== #
                self.env['account.invoice'].browse(invoice_ids).write({
                    'unsolved_move_line_ids': [(4, overdue_new_move_id)],
                })
                           
        return True
    
    # ===================================================================================== #
    #                   CLASS  SUPPORT  TO  WIZARD RIBA EFFECT RESULT                       #
    # ===================================================================================== #


class WizardLinked_RibaEffectResult(models.TransientModel):
    
    _name='wizard.linked_ribaeffectresult'
    _description='''This class is used to support the wizard 
                RibaEffectResult in order to show the partner 
                selected and their situation'''
    
    # ===================================================================================== #
    #                                      FIELDS                                           #
    # ===================================================================================== #
    
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
