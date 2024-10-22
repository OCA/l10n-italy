# Copyright 2013-2015 Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016 Alessandro Camilli <alessandro.camilli@openforce.it>
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import first


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    @api.model
    def generate_party_acc_number(
        self,
        parent_node,
        party_type,
        order,
        partner_bank,
        gen_args,
        bank_line=None,
    ):
        res = super().generate_party_acc_number(
            parent_node,
            party_type,
            order,
            partner_bank,
            gen_args,
            bank_line=bank_line,
        )
        pain_flavor = gen_args.get("pain_flavor")
        if pain_flavor == "CBIBdyPaymentRequest.00.04.01":
            iban_node = parent_node.find(f".//{'%sAcct' % party_type}/Id/IBAN")
            if iban_node is None:
                raise UserError(
                    _(
                        "Bank account '%(partner_bank)s' must have a valid IBAN",
                        partner_bank=partner_bank.display_name,
                    )
                )
        return res

    @api.model
    def generate_party_agent(
        self,
        parent_node,
        party_type,
        order,
        partner_bank,
        gen_args,
        bank_line=None,
    ):
        res = super().generate_party_agent(
            parent_node,
            party_type,
            order,
            partner_bank,
            gen_args,
            bank_line=bank_line,
        )
        pain_flavor = gen_args.get("pain_flavor")
        if pain_flavor == "CBIBdyPaymentRequest.00.04.01":
            full_debtor_data = False
        elif pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            full_debtor_data = True
            if not partner_bank.bank_bic:
                raise UserError(
                    _(
                        "BIC is mandatory for Payment Type Code '%(pain_flavor)s', "
                        "but the bank %(bank)s of %(partner_bank)s has no BIC.\n",
                        bank=partner_bank.bank_id.display_name,
                        partner_bank=partner_bank.display_name,
                        pain_flavor=pain_flavor,
                    )
                )
        else:
            return res

        if party_type == "Dbtr":
            party_agent_tag = "%sAgt" % party_type
            party_agent_node = parent_node.xpath(f"//{party_agent_tag}")[-1]

            party_agent_institution_tag = "FinInstnId"
            party_agent_institution_node = party_agent_node.xpath(
                f"{party_agent_institution_tag}"
            )[-1]

            othr = party_agent_institution_node.find(".//Othr")
            if othr is not None:
                party_agent_institution_node.remove(othr)

            iban = (
                partner_bank.sanitized_acc_number
                if partner_bank.acc_type == "iban"
                else ""
            )

            # ABI
            abi_code = False
            if "bank_abi" in partner_bank._fields:
                abi_code = partner_bank.bank_abi
            # ... try from iban
            if not abi_code and iban:
                abi_code = iban[5:10]
            if not abi_code:
                raise UserError(
                    _(
                        "ABI is mandatory for Payment Type Code '%(pain_flavor)s', "
                        "but the bank %(bank)s of %(partner_bank)s has no ABI.\n",
                        bank=partner_bank.bank_id.display_name,
                        partner_bank=partner_bank.display_name,
                        pain_flavor=pain_flavor,
                    )
                )
            party_agent_institution_sys = etree.SubElement(
                party_agent_institution_node, "ClrSysMmbId"
            )
            party_agent_institution_sys_abi = etree.SubElement(
                party_agent_institution_sys, "MmbId"
            )
            party_agent_institution_sys_abi.text = abi_code

            if full_debtor_data:
                # Complete Debtor data
                debtor_node = parent_node.xpath("//Dbtr")[0]
                debtor_address_node = etree.SubElement(debtor_node, "PstlAdr")
                debtor_country_node = etree.SubElement(debtor_address_node, "Ctry")
                debtor_country_node.text = iban[:2]

                debtor_partner = partner_bank.partner_id
                if debtor_partner:
                    debtor_address_line_node = etree.SubElement(
                        debtor_address_node, "AdrLine"
                    )
                    debtor_address_line_node.text = "{} {} {}".format(
                        debtor_partner.street or "",
                        debtor_partner.city or "",
                        debtor_partner.country_id
                        and debtor_partner.country_id.name
                        or "",
                    )

        return res

    @api.model
    def _must_have_initiating_party(self, gen_args):
        pain_flavor = gen_args.get("pain_flavor")
        is_sct_cbi_flavor = pain_flavor in [
            "CBIBdyPaymentRequest.00.04.01",
            "CBIBdyCrossBorderPaymentRequest.00.01.01",
        ]
        return is_sct_cbi_flavor or super()._must_have_initiating_party(gen_args)

    def generate_pain_nsmap(self):
        self.ensure_one()
        payment_method = self.payment_method_id
        if payment_method.code != "sepa_cbi_credit_transfer":
            nsmap = super().generate_pain_nsmap()
        else:
            pain_flavor = self.payment_method_id.pain_version
            if pain_flavor == "CBIBdyPaymentRequest.00.04.01":
                pain_xml_xsd = "CBIPaymentRequest.00.04.01"
            elif pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
                pain_xml_xsd = "CBICrossBorderPaymentRequestLogMsg"
            else:
                raise self._l10n_it_sct_cbi_unsupported_pain_exception(pain_flavor)
            nsmap = {
                None: f"urn:CBI:xsd:{payment_method.pain_version}",
                "PMRQ": f"urn:CBI:xsd:{pain_xml_xsd}",
            }
        return nsmap

    @api.model
    def generate_start_payment_info_block(
        self,
        parent_node,
        payment_info_ident,
        priority,
        local_instrument,
        category_purpose,
        sequence_type,
        requested_date,
        eval_ctx,
        gen_args,
    ):
        pain_flavor = gen_args.get("pain_flavor")
        if pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            priority = local_instrument = False

        (
            payment_info_node,
            nb_of_payment_transactions_node,
            control_payment_sum_node,
        ) = super().generate_start_payment_info_block(
            parent_node,
            payment_info_ident,
            priority,
            local_instrument,
            category_purpose,
            sequence_type,
            requested_date,
            eval_ctx,
            gen_args,
        )

        if pain_flavor in [
            "CBIBdyPaymentRequest.00.04.01",
            "CBIBdyCrossBorderPaymentRequest.00.01.01",
        ]:
            # Remove duplicate nodes
            duplicate_node_xpath_list = [
                "//PmtInf//NbOfTxs",
                "//PmtInf//CtrlSum",
            ]
            for duplicate_node_xpath in duplicate_node_xpath_list:
                duplicate_node = payment_info_node.xpath(duplicate_node_xpath)[0]
                if duplicate_node is not None:
                    duplicate_node.getparent().remove(duplicate_node)

            # Refactor ReqdExctnDt to ReqdExctnDt/Dt and move its text
            requested_execution_date_node = payment_info_node.find(".//ReqdExctnDt")
            requested_execution_date_child_node = etree.SubElement(
                requested_execution_date_node, "Dt"
            )
            requested_execution_date_child_node.text = (
                requested_execution_date_node.text
            )
            requested_execution_date_node.text = None

        return (
            payment_info_node,
            nb_of_payment_transactions_node,
            control_payment_sum_node,
        )

    def _l10n_it_sct_cbi_group_transactions_key(self, line):
        """Key for grouping transactions

        key = (requested_date, priority)
        """
        payment_line = first(line.payment_line_ids)

        requested_date = fields.Date.to_string(line.date)
        priority = payment_line.priority
        return (
            requested_date,
            priority,
        )

    def _l10n_it_sct_cbi_group_transactions(self):
        """Group transactions by key.

        Key is defined by `_l10n_it_sct_cbi_group_transactions_key`.
        """
        lines_per_group = defaultdict(list)
        for line in self.payment_ids:
            key = self._l10n_it_sct_cbi_group_transactions_key(line)
            lines_per_group[key].append(line)
        return lines_per_group

    def _l10n_it_sct_cbi_unsupported_pain_exception(self, pain_flavor):
        return UserError(
            _(
                "Payment Type Code '%(pain_flavor)s' is not supported.\n"
                "The only Payment Type Codes supported for SEPA Credit Transfers "
                "'CBIBdyPaymentRequest.00.04.01' and "
                "'CBIBdyCrossBorderPaymentRequest.00.01.01'.",
                pain_flavor=pain_flavor,
            )
        )

    def _l10n_it_sct_cbi_gen_args(self):
        payment_method = self.payment_method_id
        pain_flavor = payment_method.pain_version
        if pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            bic_xml_tag = "BIC"
        elif pain_flavor == "CBIBdyPaymentRequest.00.04.01":
            bic_xml_tag = "BICFI"
        else:
            raise self._l10n_it_sct_cbi_unsupported_pain_exception(pain_flavor)
        return {
            "bic_xml_tag": bic_xml_tag,
            "name_maxsize": 70,
            "convert_to_ascii": payment_method.convert_to_ascii,
            "payment_method": "TRF",
            "file_prefix": "sct_bci_",
            "pain_flavor": pain_flavor,
            "pain_xsd_file": payment_method.get_xsd_file_path(),
        }

    def _l10n_it_sct_cbi_root_tag(self):
        pain_flavor = self.payment_method_id.pain_version
        if pain_flavor == "CBIBdyPaymentRequest.00.04.01":
            root_xml_tag = "CBIBdyPaymentRequest"
        elif pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            root_xml_tag = "CBIBdyCrossBorderPaymentRequest"
        else:
            raise self._l10n_it_sct_cbi_unsupported_pain_exception(pain_flavor)
        return root_xml_tag

    def _l10n_it_sct_cbi_generate_xml_root(self):
        root_xml_tag = self._l10n_it_sct_cbi_root_tag()

        nsmap = self.generate_pain_nsmap()
        xml_root = etree.Element(root_xml_tag, nsmap=nsmap)
        return xml_root

    def _l10n_it_sct_cbi_payment_tags(self):
        pain_flavor = self.payment_method_id.pain_version
        if pain_flavor == "CBIBdyPaymentRequest.00.04.01":
            envel_xml_tag = "CBIEnvelPaymentRequest"
            pain_xml_tag = "CBIPaymentRequest"
        elif pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            envel_xml_tag = "CBIEnvelCBICrossBorderPaymentRequest"
            pain_xml_tag = "CBICrossBorderPaymentRequestLogMsg"
        else:
            raise self._l10n_it_sct_cbi_unsupported_pain_exception(pain_flavor)
        return envel_xml_tag, pain_xml_tag

    def _l10n_it_sct_cbi_generate_payment_root(self, parent_node):
        envel_xml_tag, pain_xml_tag = self._l10n_it_sct_cbi_payment_tags()

        envel_root = etree.SubElement(parent_node, envel_xml_tag)
        pain_root = etree.SubElement(envel_root, pain_xml_tag)
        return pain_root

    def _l10n_it_sct_cbi_generate_transaction_block(
        self, payment_info_node, line, gen_args
    ):
        # C. Credit Transfer Transaction Info
        credit_transfer_transaction_info_node = etree.SubElement(
            payment_info_node, "CdtTrfTxInf"
        )
        payment_identification = etree.SubElement(
            credit_transfer_transaction_info_node, "PmtId"
        )
        # CBI PmtTpInf (Causale bonifici)
        payment_identification_PmtTpInf = etree.SubElement(
            credit_transfer_transaction_info_node, "PmtTpInf"
        )
        payment_identification_CtgyPurp = etree.SubElement(
            payment_identification_PmtTpInf, "CtgyPurp"
        )
        payment_identification_CtgyPurp_Cd = etree.SubElement(
            payment_identification_CtgyPurp, "Cd"
        )
        payment_identification_CtgyPurp_Cd.text = "SUPP"
        instruction_identification = etree.SubElement(payment_identification, "InstrId")
        instruction_identification.text = self._prepare_field(
            "Instruction Identification",
            "str(line.move_id.id)",
            {"line": line},
            35,
            gen_args=gen_args,
        )
        end2end_identification = etree.SubElement(payment_identification, "EndToEndId")
        end2end_identification.text = self._prepare_field(
            "End to End Identification",
            "str(line.move_id.id)",
            {
                "line": line,
            },
            35,
            gen_args=gen_args,
        )
        currency_name = self._prepare_field(
            "Currency Code",
            "line.currency_id.name",
            {
                "line": line,
            },
            3,
            gen_args=gen_args,
        )
        amount_node = etree.SubElement(credit_transfer_transaction_info_node, "Amt")
        instructed_amount = etree.SubElement(amount_node, "InstdAmt", Ccy=currency_name)
        instructed_amount.text = "%.2f" % line.amount
        if not line.partner_bank_id:
            raise UserError(
                _(
                    "Bank account is missing on the bank payment line "
                    "of partner '%(partner)s' (reference '%(reference)s').",
                    partner=line.partner_id.name,
                    reference=line.name,
                )
            )
        self.generate_party_block(
            credit_transfer_transaction_info_node,
            "Cdtr",
            "C",
            line.partner_bank_id,
            gen_args,
            line,
        )

        pain_flavor = self.payment_method_id.pain_version
        if pain_flavor == "CBIBdyCrossBorderPaymentRequest.00.01.01":
            # Add info for Cross Border payment
            creditor_partner = line.partner_id
            creditor_node = credit_transfer_transaction_info_node.xpath("//Cdtr[-1]")
            creditor_address_node = etree.SubElement(creditor_node, "PstlAdr")

            creditor_address_country_node = etree.SubElement(
                creditor_address_node, "Ctry"
            )
            iso_country = False
            iban = (
                line.bank_id.sanitized_acc_number
                if line.bank_id.acc_type == "iban"
                else ""
            )
            if iban:
                iso_country = iban[:2]
            elif creditor_partner.country_id:
                iso_country = creditor_partner.country_id.code
            if not iso_country:
                raise UserError(
                    _(
                        "Missing Country for Partner '%(partner)s' (payment "
                        "order line reference '%(reference)s')",
                        partner=line.partner_id.name,
                        reference=line.name,
                    )
                )
            creditor_address_country_node.text = iso_country

            creditor_address_line_node = etree.SubElement(
                creditor_address_node, "AdrLine"
            )
            if creditor_partner:
                address = (
                    f"{creditor_partner.street or ''} "
                    f"{creditor_partner.city or ''} "
                    f"{creditor_partner.country_id.name or ''}"
                )
                creditor_address_line_node.text = address[:70]

        self.generate_remittance_info_block(
            credit_transfer_transaction_info_node, line, gen_args
        )
        return credit_transfer_transaction_info_node, line.amount

    def _l10n_it_sct_cbi_generate_payment_block(
        self, pain_root, transactions_key, transactions, gen_args
    ):
        # Payment
        # Unpack key as defined in _l10n_it_sct_cbi_group_transactions_key
        requested_date, priority = transactions_key
        (
            payment_node,
            transactions_number_node,
            transactions_amount_node,
        ) = self.generate_start_payment_info_block(
            pain_root,
            "self.name + '-' " "+ requested_date.replace('-', '')  + '-' + priority",
            priority,
            False,
            False,
            False,
            requested_date,
            {
                "self": self,
                "priority": priority,
                "requested_date": requested_date,
            },
            gen_args,
        )

        self.generate_party_block(
            payment_node, "Dbtr", "B", self.company_partner_bank_id, gen_args
        )

        charge_bearer = etree.SubElement(payment_node, "ChrgBr")
        charge_bearer.text = self.charge_bearer

        transactions_amount = 0.0
        for transaction in transactions:
            (
                transaction_node,
                transaction_amount,
            ) = self._l10n_it_sct_cbi_generate_transaction_block(
                payment_node, transaction, gen_args
            )
            transactions_amount += transaction_amount

        transactions_number = len(transactions)
        transactions_number_node.text = str(transactions_number)
        transactions_amount_node.text = "%.2f" % transactions_amount
        return payment_node, transactions_number, transactions_amount

    def finalize_sepa_file_creation(self, xml_root, gen_args):
        if self.payment_method_id.code == "sepa_cbi_credit_transfer":
            # Children of pain node must be in PMRQ namespace
            pain_namespace = xml_root.nsmap["PMRQ"]
            _envel_xml_tag, pain_xml_tag = self._l10n_it_sct_cbi_payment_tags()
            pain_roots = xml_root.findall(f".//{pain_xml_tag}")
            for pain_root in pain_roots:
                for pain_child in pain_root.iterdescendants():
                    pain_child.tag = etree.QName(pain_namespace, tag=pain_child.tag)
        return super().finalize_sepa_file_creation(xml_root, gen_args)

    def generate_payment_file(self):
        """Creates the SEPA Credit Transfer file. That's the important code!"""
        self.ensure_one()
        if self.payment_method_id.code != "sepa_cbi_credit_transfer":
            return super().generate_payment_file()

        gen_args = self._l10n_it_sct_cbi_gen_args()

        xml_root = self._l10n_it_sct_cbi_generate_xml_root()

        transactions_number = 0
        transactions_amount = 0.0
        grouped_transactions = self._l10n_it_sct_cbi_group_transactions()
        for transactions_key, transactions in grouped_transactions.items():
            pain_root = self._l10n_it_sct_cbi_generate_payment_root(xml_root)

            # Header
            (
                group_header_node,
                transactions_number_node,
                transactions_amount_node,
            ) = self.generate_group_header_block(pain_root, gen_args)

            (
                payment_node,
                payment_transactions_number,
                payment_transactions_amount,
            ) = self._l10n_it_sct_cbi_generate_payment_block(
                pain_root, transactions_key, transactions, gen_args
            )

            transactions_number += payment_transactions_number
            transactions_amount += payment_transactions_amount

            transactions_number_node.text = str(transactions_number)
            transactions_amount_node.text = "%.2f" % transactions_amount

        return self.finalize_sepa_file_creation(xml_root, gen_args)
