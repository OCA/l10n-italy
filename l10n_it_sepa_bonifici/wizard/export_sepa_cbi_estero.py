# -*- coding: utf-8 -*-
##############################################################################
#
#    SEPA Direct Debit module for Odoo
#    Copyright (C) 2013-2015 Akretion (http://www.akretion.com)
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
from openerp import workflow
from lxml import etree
import logging


logger = logging.getLogger(__name__)


class BankingExportSepaCbiEsteroWizard(models.TransientModel):
    _name = 'banking.export.sepa.cbi.estero.wizard'
    _inherit = ['banking.export.pain']
    _description = 'Export SEPA CBI Estero File'

    state = fields.Selection([
        ('create', 'Create'),
        ('finish', 'Finish'),
    ], string='State', readonly=True, default='create')
    batch_booking = fields.Boolean(
        string='Batch Booking',
        help="If true, the bank statement will display only one credit "
        "line for all the direct debits of the SEPA file ; if false, "
        "the bank statement will display one credit line per direct "
        "debit of the SEPA file.")
    charge_bearer = fields.Selection([
        ('SHAR', 'Shared'),
        ('CRED', 'Borne by Creditor'),
        ('DEBT', 'Borne by Debtor'),
    ], string='Charge Bearer', required=True, default='DEBT',
        help="Following service level : transaction charges are to be "
        "applied following the rules agreed in the service level "
        "and/or scheme (SEPA Core messages must use this). Shared : "
        "transaction charges on the creditor side are to be borne "
        "by the creditor, transaction charges on the debtor side are "
        "to be borne by the debtor. Borne by creditor : all "
        "transaction charges are to be borne by the creditor. Borne "
        "by debtor : all transaction charges are to be borne by the debtor.")
    nb_transactions = fields.Integer(
        string='Number of Transactions', readonly=True)
    total_amount = fields.Float(string='Total Amount', readonly=True)
    file = fields.Binary(string="File", readonly=True)
    filename = fields.Char(string="Filename", readonly=True)
    payment_order_ids = fields.Many2many(
        'payment.order', 'wiz_sepa_cbi_estero_payorders_rel', 'wizard_id',
        'payment_order_id', string='Payment Orders', readonly=True)

    @api.model
    def create(self, vals):
        payment_order_ids = self._context.get('active_ids', [])
        vals.update({
            'payment_order_ids': [[6, 0, payment_order_ids]],
        })
        return super(BankingExportSepaCbiEsteroWizard, self).create(vals)

    @api.model
    def generate_party_agent(self, parent_node, party_type, party_type_label,
                             order, party_name, iban, bic, eval_ctx, gen_args,
                             context=None):

        # CBI logic modified for add ABI of debitor
        # ABI and BIC code
        if party_type == 'Dbtr':
            company_bank =\
                gen_args['sepa_export'].payment_order_ids[0].mode.bank_id
            partner_debitor =\
                gen_args['sepa_export'].payment_order_ids[0].mode.bank_id.\
                partner_id
            abi_code = False
            if 'bank_abi' in company_bank:
                abi_code = company_bank.bank_abi
            # ... try from iban
            if not abi_code and company_bank.state == 'iban':
                iban = company_bank.acc_number.replace(" ", "")
                abi_code = iban[5:10]
            if not abi_code:
                raise UserError(_("Error Bank Code ABI"))
            bic_code = False
            if company_bank.bank_bic:
                bic_code = company_bank.bank_bic
            if not bic_code:
                raise UserError(_("Error Bank Code BIC"))
            party_agent = etree.SubElement(parent_node, '%sAgt' % party_type)
            party_agent_institution = etree.SubElement(
                party_agent, 'FinInstnId')
            # BIC
            party_agent_institution_BIC = etree.SubElement(
                party_agent_institution, 'BIC')
            party_agent_institution_BIC.text = bic_code
            # ABI
            party_agent_institution_sys = etree.SubElement(
                party_agent_institution, 'ClrSysMmbId')
            party_agent_institution_sys_abi = etree.SubElement(
                party_agent_institution_sys, 'MmbId')
            party_agent_institution_sys_abi.text = abi_code
            # Complete Debitor data
            debitor_node = parent_node.xpath('//Dbtr')[0]
            debitor_address_node = etree.SubElement(debitor_node, 'PstlAdr')
            debitor_country_node = etree.SubElement(debitor_address_node,
                                                    'Ctry')
            debitor_country_node.text = iban[:2]
            debitor_address_line_node = etree.SubElement(debitor_address_node,
                                                         'AdrLine')
            if partner_debitor:
                address = '%s %s %s' % (
                    partner_debitor.street or '',
                    partner_debitor.city or '',
                    partner_debitor.country_id and
                    partner_debitor.country_id.name or '',)
            debitor_address_line_node.text = address

        return True

    @api.model
    def generate_creditor_scheme_identification(
            self, parent_node, identification, identification_label,
            eval_ctx, scheme_name_proprietary, gen_args):
        #
        # CBI logic modified for not try to add other info
        #
        '''
        csi_id = etree.SubElement(parent_node, 'Id')
        csi_privateid = etree.SubElement(csi_id, 'PrvtId')
        csi_other = etree.SubElement(csi_privateid, 'Othr')
        csi_other_id = etree.SubElement(csi_other, 'Id')
        csi_other_id.text = self._prepare_field(
            identification_label, identification, eval_ctx, gen_args=gen_args)
        csi_scheme_name = etree.SubElement(csi_other, 'SchmeNm')
        csi_scheme_name_proprietary = etree.SubElement(
            csi_scheme_name, 'Prtry')
        csi_scheme_name_proprietary.text = scheme_name_proprietary
        '''
        return True

    @api.multi
    def create_sepa(self):
        """Creates the SEPA Credit Transfer file. That's the important code!"""
        sepa_export = self[0]
        pain_flavor = self.payment_order_ids[0].mode.type.code
        convert_to_ascii = \
            self.payment_order_ids[0].mode.convert_to_ascii
        if pain_flavor == 'CBIBdyCrossBorderPaymentRequest.00.01.01':
            bic_xml_tag = 'BIC'
            name_maxsize = 70
            root_xml_tag = 'CBIEnvelCBICrossBorderPaymentRequest'
            xsd_ref = 'CBICrossBorderPaymentRequestLogMsg.00.01.01'
        else:
            raise UserError(
                _("Payment Type Code '%s' is not supported. The only "
                  "Payment Type Code supported for SEPA Credit Transfers "
                  "'CBIBdyCrossBorderPaymentRequest.00.01.01'. "
                  ) % pain_flavor)
        gen_args = {
            'bic_xml_tag': bic_xml_tag,
            'name_maxsize': name_maxsize,
            'convert_to_ascii': convert_to_ascii,
            'payment_method': 'TRF',
            'file_prefix': 'sct_estero_',
            'pain_flavor': pain_flavor,
            'pain_xsd_file': 'l10n_it_sepa_bonifici/data/%s.xsd' % pain_flavor,
            'sepa_export': sepa_export,
        }
        pain_ns = {
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            None: 'urn:CBI:xsd:%s' % pain_flavor,
        }
        xml_root = etree.Element('CBIBdyCrossBorderPaymentRequest',
                                 nsmap=pain_ns)
        pain_root = etree.SubElement(xml_root, root_xml_tag)
        # Add tag x cbi
        pain_root = etree.SubElement(pain_root,
                                     'CBICrossBorderPaymentRequestLogMsg')
        pain_03_to_05 = \
            ['CBIBdyCrossBorderPaymentRequest.00.01.01']
        # A. Group header
        group_header_1_0, nb_of_transactions_1_6, control_sum_1_7 = \
            self.generate_group_header_block(pain_root, gen_args)
        # ... Add pain to group header tag (CBI required)
        GrpHdr_node = xml_root.xpath('//GrpHdr')[0]  # CBI required
        GrpHdr_node.attrib['xmlns'] = 'urn:CBI:xsd:%s' % (xsd_ref,)

        transactions_count_1_6 = 0
        total_amount = 0.0
        amount_control_sum_1_7 = 0.0
        lines_per_group = {}
        # key = (requested_date, priority, sequence type)
        # value = list of lines as objects
        # Iterate on payment orders
        for payment_order in self.payment_order_ids:
            total_amount = total_amount + payment_order.total
            for line in payment_order.bank_line_ids:
                priority = line.priority
                # The field line.date is the requested payment date
                # taking into account the 'date_prefered' setting
                # cf account_banking_payment_export/models/account_payment.py
                # in the inherit of action_open()
                key = (line.date, priority)
                if key in lines_per_group:
                    lines_per_group[key].append(line)
                else:
                    lines_per_group[key] = [line]
        for (requested_date, priority), lines in lines_per_group.items():
            # B. Payment info
            payment_info_2_0, nb_of_transactions_2_4, control_sum_2_5 = \
                self.generate_start_payment_info_block(
                    pain_root,
                    "self.payment_order_ids[0].reference + '-' "
                    "+ requested_date.replace('-', '')  + '-' + priority",
                    priority, False, False, requested_date, {
                        'self': self,
                        'priority': priority,
                        'requested_date': requested_date,
                    }, gen_args)
            # ... for CBI structure
            #     Remove priority
            InstrPrty_node = xml_root.xpath('//PmtInf//InstrPrty')[0]
            InstrPrty_node.getparent().remove(InstrPrty_node)
            #     Add pain to payment info tag (CBI required)
            PmtInf_node = xml_root.xpath('//PmtInf')[0]
            PmtInf_node.attrib['xmlns'] = 'urn:CBI:xsd:%s' % (xsd_ref,)
            #     Remove the duplicate node  NbOfTxs in payment
            NbOfTxs_node = xml_root.xpath('//PmtInf//NbOfTxs')[0]
            NbOfTxs_node.getparent().remove(NbOfTxs_node)
            # Remove the duplicate node  CtrlSum in payment
            CtrlSum_node = xml_root.xpath('//PmtInf//CtrlSum')[0]
            CtrlSum_node.getparent().remove(CtrlSum_node)
            self.generate_party_block(
                payment_info_2_0, 'Dbtr', 'B',
                'self.payment_order_ids[0].mode.bank_id.partner_id.'
                'name',
                'self.payment_order_ids[0].mode.bank_id.acc_number',
                'self.payment_order_ids[0].mode.bank_id.bank.bic or '
                'self.payment_order_ids[0].mode.bank_id.bank_bic',
                {'self': self}, gen_args)
            charge_bearer_2_24 = etree.SubElement(payment_info_2_0, 'ChrgBr')
            charge_bearer_2_24.text = self.charge_bearer
            transactions_count_2_4 = 0
            amount_control_sum_2_5 = 0.0
            for line in lines:
                transactions_count_1_6 += 1
                transactions_count_2_4 += 1
                # C. Credit Transfer Transaction Info
                credit_transfer_transaction_info_2_27 = etree.SubElement(
                    payment_info_2_0, 'CdtTrfTxInf')
                payment_identification_2_28 = etree.SubElement(
                    credit_transfer_transaction_info_2_27, 'PmtId')
                # CBI PmtTpInf (Causale bonifici)
                payment_identification_2_28_PmtTpInf = etree.SubElement(
                    credit_transfer_transaction_info_2_27, 'PmtTpInf')
                payment_identification_2_28_CtgyPurp = etree.SubElement(
                    payment_identification_2_28_PmtTpInf, 'CtgyPurp')
                payment_identification_2_28_CtgyPurp_Cd = etree.SubElement(
                    payment_identification_2_28_CtgyPurp, 'Cd')
                payment_identification_2_28_CtgyPurp_Cd.text = 'SUPP'  # gen.

                # CBI tag InstrId
                end2end_identification_2_30_InstrId = etree.SubElement(
                    payment_identification_2_28, 'InstrId')
                end2end_identification_2_30_InstrId.text = line.name

                end2end_identification_2_30 = etree.SubElement(
                    payment_identification_2_28, 'EndToEndId')
                end2end_identification_2_30.text = self._prepare_field(
                    'End to End Identification', 'line.name',
                    {'line': line}, 35, gen_args=gen_args)
                currency_name = self._prepare_field(
                    'Currency Code', 'line.currency.name',
                    {'line': line}, 3, gen_args=gen_args)
                amount_2_42 = etree.SubElement(
                    credit_transfer_transaction_info_2_27, 'Amt')
                instructed_amount_2_43 = etree.SubElement(
                    amount_2_42, 'InstdAmt', Ccy=currency_name)
                instructed_amount_2_43.text = '%.2f' % line.amount_currency
                amount_control_sum_1_7 += line.amount_currency
                amount_control_sum_2_5 += line.amount_currency
                if not line.bank_id:
                    raise UserError(
                        _("Missing Bank Account on invoice '%s' (payment "
                            "order line reference '%s')") %
                        (line.ml_inv_ref.number, line.name))
                self.generate_party_block(
                    credit_transfer_transaction_info_2_27, 'Cdtr', 'C',
                    'line.partner_id.name', 'line.bank_id.acc_number',
                    'line.bank_id.bank.bic', {'line': line}, gen_args)
                # Add info for Cross Border payment
                partner_creditor = line.partner_id
                creditor_node = credit_transfer_transaction_info_2_27\
                    .xpath('//Cdtr')[transactions_count_1_6 - 1]
                creditor_address_node = etree.SubElement(creditor_node,
                                                         'PstlAdr')
                creditor_address_country_node = etree.SubElement(
                    creditor_address_node, 'Ctry')
                iso_country = False
                if line.bank_id.state == 'iban':
                    iso_country = line.bank_id.iban[:2]
                elif partner_creditor.country_id:
                    iso_country = partner_creditor.country_id.code
                if not iso_country:
                    raise UserError(
                        _("Missing Country for Partner '%s' (payment "
                            "order line reference '%s')") %
                        (line.partner_id.name, line.name))
                creditor_address_country_node.text = iso_country
                creditor_address_line_node = etree.SubElement(
                    creditor_address_node, 'AdrLine')
                if partner_creditor:
                    address = '%s %s %s' % (
                        partner_creditor.street or '',
                        partner_creditor.city or '',
                        partner_creditor.country_id and
                        partner_creditor.country_id.name or '',)
                creditor_address_line_node.text = address[:70]

                self.generate_remittance_info_block(
                    credit_transfer_transaction_info_2_27, line, gen_args)

            if pain_flavor in pain_03_to_05:
                nb_of_transactions_2_4.text = str(transactions_count_2_4)
                control_sum_2_5.text = '%.2f' % amount_control_sum_2_5
        if pain_flavor in pain_03_to_05:
            nb_of_transactions_1_6.text = str(transactions_count_1_6)
            control_sum_1_7.text = '%.2f' % amount_control_sum_1_7
        else:
            nb_of_transactions_1_6.text = str(transactions_count_1_6)
            control_sum_1_7.text = '%.2f' % amount_control_sum_1_7
        # print(etree.tostring(xml_root, pretty_print=True))
        return self.finalize_sepa_file_creation(
            xml_root, total_amount, transactions_count_1_6, gen_args)

    @api.multi
    def save_sepa(self):
        """Save the SEPA file: send the done signal to all payment
        orders in the file. With the default workflow, they will
        transition to 'done', while with the advanced workflow in
        account_banking_payment they will transition to 'sent' waiting
        reconciliation.
        """
        for order in self.payment_order_ids:
            workflow.trg_validate(
                self._uid, 'payment.order', order.id, 'done', self._cr)
            self.env['ir.attachment'].create({
                'res_model': 'payment.order',
                'res_id': order.id,
                'name': self.filename,
                'datas': self.file,
            })
        return True
