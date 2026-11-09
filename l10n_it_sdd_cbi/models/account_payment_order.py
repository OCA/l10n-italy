# Copyright 2024 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountPaymentOrderInherit(models.Model):
    _inherit = "account.payment.order"

    scheme = fields.Selection(
        [
            ("CORE", "Basic (CORE)"),
            ("B2B", "Enterprise (B2B)"),
        ],
        default=lambda self: self.env.user.company_id.sepa_payment_order_schema,
        tracking=True,
    )

    @api.model
    def _create_creditor_agent_node(self, parent_node, partner_bank):
        party_agent = etree.SubElement(parent_node, "CdtrAgt")
        institution_node = etree.SubElement(party_agent, "FinInstnId")
        member_id_node = etree.SubElement(institution_node, "ClrSysMmbId")
        member_id_text = etree.SubElement(member_id_node, "MmbId")

        member_id_text.text = partner_bank.bank_abi or "NOTPROVIDED"

    @api.model
    def _is_italian_bank(self, partner_bank):
        return (
            partner_bank.acc_type == "iban"
            and partner_bank.sanitized_acc_number.upper().startswith("IT")
        )

    @api.model
    def generate_party_agent(
        self, parent_node, party_type, order, partner_bank, gen_args, bank_line=None
    ):
        if gen_args.get("pain_flavor").startswith("CBIBdySDDReq"):
            if party_type == "Cdtr":
                self._create_creditor_agent_node(parent_node, partner_bank)
                return True

            if self._is_italian_bank(partner_bank):
                return True

        return super().generate_party_agent(
            parent_node=parent_node,
            party_type=party_type,
            order=order,
            partner_bank=partner_bank,
            gen_args=gen_args,
            bank_line=bank_line,
        )

    def generate_pain_nsmap(self):
        self.ensure_one()
        pain_flavor = self.payment_mode_id.payment_method_id.pain_version
        if pain_flavor.startswith("CBIBdySDDReq"):
            nsmap = {
                "xsi": "http://www.w3.org/2001/XMLSchema-instance",
                None: f"urn:CBI:xsd:{pain_flavor}",
            }
            return nsmap

        return super().generate_pain_nsmap()

    def _prepare_generation_args(self):
        pain_flavor = self.payment_method_id.pain_version

        if not pain_flavor.startswith("CBIBdySDDReq"):
            raise UserError(
                self.env._(
                    "Payment Type Code '%s' is not supported. "
                    "Only 'CBIBdySDDReq' is allowed for CBI SDD Italy.",
                    pain_flavor,
                )
            )

        pay_method = self.payment_mode_id.payment_method_id
        version = pain_flavor.replace("CBIBdySDDReq", "")
        if version.endswith(".00"):
            bic_xml_tag = "BIC"
        else:
            bic_xml_tag = "BICFI"
        return {
            "bic_xml_tag": bic_xml_tag,
            "name_maxsize": 70,
            "convert_to_ascii": pay_method.convert_to_ascii,
            "payment_method": "DD",
            "file_prefix": "sdd_",
            "pain_flavor": pain_flavor,
            "version": version,
            "pain_xsd_file": pay_method.get_xsd_file_path(),
        }

    def generate_payment_file(self):
        """
        Creates the CBI SDD Italy.
        That's the important code!
        """
        self.ensure_one()
        if not self.payment_method_id.code.startswith("cbi_sdd_italy"):
            return super().generate_payment_file()

        initiating_party_issuer = (
            self.payment_mode_id.initiating_party_issuer
            or self.payment_mode_id.company_id.initiating_party_issuer
        )
        if not initiating_party_issuer or initiating_party_issuer != "CBI":
            raise UserError(
                self.env._(
                    "Missing 'Initiating Party Issuer' must be set to 'CBI' "
                    "for the company '%s'.",
                    self.company_id.name,
                )
            )
        if not self.sepa:
            raise UserError(
                self.env._(
                    "Please check the IBAN of the company's and partner's bank account."
                    " To generate the SDD file, the account must be of type IBAN."
                )
            )

        gen_args = self._prepare_generation_args()
        nsmap = self.generate_pain_nsmap()
        attrib = self.generate_pain_attrib()
        xml_root = etree.Element("CBIBdySDDReq", nsmap=nsmap, attrib=attrib)

        phyMsgInf = etree.SubElement(xml_root, "PhyMsgInf")
        phyMsgTpCd = etree.SubElement(phyMsgInf, "PhyMsgTpCd")

        if self.scheme == "CORE":
            phyMsgTpCd.text = "INC-SDDC-01"
        elif self.scheme == "B2B":
            phyMsgTpCd.text = "INC-SDDB-01"
        else:
            raise UserError(
                self.env._("Invalid CBI SDD Italy Order Scheme %s", self.scheme)
            )

        numLogMsg = etree.SubElement(phyMsgInf, "NbOfLogMsg")
        numLogMsg.text = "1"

        envel_pay_req = etree.SubElement(xml_root, "CBIEnvelSDDReqLogMsg")
        pain_root = etree.SubElement(envel_pay_req, "CBISDDReqLogMsg")

        # A. Group header
        (__, nb_of_transactions_a, control_sum_a) = self.generate_group_header_block(
            pain_root, gen_args
        )
        grp_hdr_node = pain_root.xpath("//GrpHdr")[0]
        grp_hdr_node.attrib["xmlns"] = (
            f"urn:CBI:xsd:CBISDDReqLogMsg{gen_args['version']}"
        )

        amount_control_sum_a = 0.0
        lines_per_group, transactions_count_a = self._grouping_payments()

        for (
            (requested_date, priority, categ_purpose, sequence_type, scheme),
            lines,
        ) in list(lines_per_group.items()):
            # B. Payment info
            requested_date = fields.Date.to_string(requested_date)
            (
                payment_info,
                nb_of_transactions_b,
                control_sum_b,
            ) = self.generate_start_payment_info_block(
                pain_root,
                "self.name + '-' + "
                "sequence_type + '-' + requested_date.replace('-', '')  "
                "+ '-' + priority + '-' + category_purpose",
                priority,
                scheme,
                categ_purpose,
                sequence_type,
                requested_date,
                {
                    "self": self,
                    "sequence_type": sequence_type,
                    "priority": priority,
                    "category_purpose": categ_purpose or "NOcateg",
                    "requested_date": requested_date,
                },
                gen_args,
            )

            # Add pain to payment info tag (CBI required)
            pmt_inf_nodes = pain_root.xpath("//PmtInf")
            for pmt_inf_node in pmt_inf_nodes:
                pmt_inf_node.attrib["xmlns"] = (
                    f"urn:CBI:xsd:CBISDDReqLogMsg{gen_args['version']}"
                )
            tags_to_remove = ["//PmtInf//NbOfTxs", "//PmtInf//CtrlSum"]
            for tag in tags_to_remove:
                elements_to_remove = pain_root.xpath(tag)
                for element in elements_to_remove:
                    parent = element.getparent()
                    if parent is not None:
                        parent.remove(element)

            self.generate_party_block(
                payment_info, "Cdtr", "B", self.company_partner_bank_id, gen_args
            )
            charge_bearer = etree.SubElement(payment_info, "ChrgBr")
            if self.sepa:
                charge_bearer_text = "SLEV"
            else:
                charge_bearer_text = self.charge_bearer
            charge_bearer.text = charge_bearer_text
            creditor_scheme_identification = etree.SubElement(
                payment_info, "CdtrSchmeId"
            )
            self.generate_creditor_scheme_identification(
                creditor_scheme_identification,
                "self.payment_mode_id.sepa_creditor_identifier or "
                "self.company_id.sepa_creditor_identifier",
                "SEPA Creditor Identifier",
                {"self": self},
                "SEPA",
                gen_args,
            )
            transactions_count_b = 0
            amount_control_sum_b = 0.0
            for line in lines:
                transactions_count_b += 1
                # C. Direct Debit Transaction Info
                dd_transaction_info = etree.SubElement(payment_info, "DrctDbtTxInf")
                payment_identification = etree.SubElement(dd_transaction_info, "PmtId")
                instruction_identification = etree.SubElement(
                    payment_identification, "InstrId"
                )
                instruction_identification.text = self._prepare_field(
                    "Instruction Identification",
                    "str(line.move_id.id)",
                    {"line": line},
                    6,
                    gen_args=gen_args,
                )
                end2end_identification = etree.SubElement(
                    payment_identification, "EndToEndId"
                )
                end2end_identification.text = self._prepare_field(
                    "End to End Identification",
                    "str(line.move_id.id)",
                    {"line": line},
                    35,
                    gen_args=gen_args,
                )
                currency_name = self._prepare_field(
                    "Currency Code",
                    "line.currency_id.name",
                    {"line": line},
                    3,
                    gen_args=gen_args,
                )
                instructed_amount = etree.SubElement(
                    dd_transaction_info, "InstdAmt", Ccy=currency_name
                )
                instructed_amount.text = f"{line.amount:.2f}"
                amount_control_sum_a += line.amount
                amount_control_sum_b += line.amount
                dd_transaction = etree.SubElement(dd_transaction_info, "DrctDbtTx")
                mandate_related_info = etree.SubElement(dd_transaction, "MndtRltdInf")
                mandate_identification = etree.SubElement(
                    mandate_related_info, "MndtId"
                )
                mandate = line.payment_line_ids[:1].mandate_id
                mandate_identification.text = self._prepare_field(
                    "Unique Mandate Reference",
                    "mandate.unique_mandate_reference",
                    {"mandate": mandate},
                    35,
                    gen_args=gen_args,
                )
                mandate_signature_date = etree.SubElement(
                    mandate_related_info, "DtOfSgntr"
                )
                mandate_signature_date.text = self._prepare_field(
                    "Mandate Signature Date",
                    "signature_date",
                    {
                        "line": line,
                        "signature_date": fields.Date.to_string(mandate.signature_date),
                    },
                    10,
                    gen_args=gen_args,
                )
                if sequence_type == "FRST" and mandate.last_debit_date:
                    amendment_indicator = etree.SubElement(
                        mandate_related_info, "AmdmntInd"
                    )
                    amendment_indicator.text = "true"
                    amendment_info_details = etree.SubElement(
                        mandate_related_info, "AmdmntInfDtls"
                    )
                    ori_debtor_account = etree.SubElement(
                        amendment_info_details, "OrgnlDbtrAcct"
                    )
                    ori_debtor_account_id = etree.SubElement(ori_debtor_account, "Id")
                    ori_debtor_agent_other = etree.SubElement(
                        ori_debtor_account_id, "Othr"
                    )
                    ori_debtor_agent_other_id = etree.SubElement(
                        ori_debtor_agent_other, "Id"
                    )
                    ori_debtor_agent_other_id.text = "SMNDA"
                    # Until 20/11/2016, SMNDA meant
                    # "Same Mandate New Debtor Agent"
                    # After 20/11/2016, SMNDA means
                    # "Same Mandate New Debtor Account"

                self.generate_party_block(
                    dd_transaction_info,
                    "Dbtr",
                    "C",
                    line.partner_bank_id,
                    gen_args,
                    line,
                )
                line_purpose = line.payment_line_ids[:1].purpose
                if line_purpose:
                    purpose = etree.SubElement(dd_transaction_info, "Purp")
                    etree.SubElement(purpose, "Cd").text = line_purpose

                self.generate_remittance_info_block(dd_transaction_info, line, gen_args)

            nb_of_transactions_b.text = str(transactions_count_b)
            control_sum_b.text = f"{amount_control_sum_b:.2f}"
        nb_of_transactions_a.text = str(transactions_count_a)
        control_sum_a.text = f"{amount_control_sum_a:.2f}"

        return self.finalize_sepa_file_creation(xml_root, gen_args)

    def _grouping_payments(self):
        lines_per_group = {}
        transactions_count_a = 0
        # key = (requested_date, priority, sequence type)
        # value = list of lines as objects
        for line in self.payment_ids:
            transactions_count_a += 1
            payment_line = line.payment_line_ids[:1]
            priority = payment_line.priority
            categ_purpose = payment_line.category_purpose
            scheme = payment_line.mandate_id.scheme
            if payment_line.mandate_id.type == "oneoff":
                seq_type = "OOFF"
            elif payment_line.mandate_id.type == "recurrent":
                seq_type_map = {"recurring": "RCUR", "first": "FRST", "final": "FNAL"}
                seq_type_label = payment_line.mandate_id.recurrent_sequence_type
                assert seq_type_label is not False
                seq_type = seq_type_map[seq_type_label]
            else:
                raise UserError(
                    self.env._(
                        "Invalid mandate type in '%s'. Valid ones are 'Recurrent' "
                        "or 'One-Off'",
                        payment_line.mandate_id.unique_mandate_reference,
                    )
                )
            # The field line.payment_line_date is the requested payment date
            key = (line.payment_line_date, priority, categ_purpose, seq_type, scheme)
            if key in lines_per_group:
                lines_per_group[key].append(line)
            else:
                lines_per_group[key] = [line]
        return lines_per_group, transactions_count_a
