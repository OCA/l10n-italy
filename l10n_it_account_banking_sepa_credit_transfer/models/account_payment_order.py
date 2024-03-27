import logging

from odoo import _, models
from odoo.exceptions import RedirectWarning, ValidationError

_logger = logging.getLogger(__name__)
try:
    import fintech

    fintech.register()
    from fintech.sepa import Account, SEPACreditTransfer

except ImportError:
    _logger.debug("Cannot `import fintech`, use `pip install fintech`")


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def generate_payment_file(self):

        self.ensure_one()
        if self.payment_method_id.pain_version != "pain.00.04.00":
            return super().generate_payment_file()

        # Create the debtor account from a tuple (ACCOUNT, BANKCODE)
        iban = self.company_partner_bank_id.acc_number.replace(" ", "")
        bic = self.company_partner_bank_id.bank_id.bic
        cuc = self.company_partner_bank_id.cuc
        acc_holder_name = (
            self.company_partner_bank_id.acc_holder_name
            or self.company_partner_bank_id.partner_id.name
        )

        if not cuc:
            action = self.env.ref("base.action_res_partner_bank_account_form")
            action_dict = action.read()[0]
            action_dict.update(
                {
                    "res_id": self.company_partner_bank_id.id,
                    "domain": [("id", "=", self.company_partner_bank_id.id)],
                }
            )
            raise RedirectWarning(
                message=_(
                    f"Incorrect CUC for '{self.company_partner_bank_id.display_name}'\n"
                ),
                action=action_dict,
                button_text=_("Bank Settings"),
            )

        if not bic:
            action = self.env.ref("base.action_res_bank_form")
            action_dict = action.read()[0]
            action_dict.update(
                {
                    "res_id": self.company_partner_bank_id.bank_id.id,
                    "domain": [("id", "=", self.company_partner_bank_id.bank_id.id)],
                }
            )
            raise RedirectWarning(
                message=_(
                    f"Incorrect BIC for '{self.company_partner_bank_id.bank_id.display_name}'\n"
                ),
                action=action_dict,
                button_text=_("Bank Settings"),
            )

        debtor = Account(iban=(iban, bic), name=acc_holder_name)
        try:
            debtor.set_originator_id(cuc=cuc)
        except Exception as e:
            raise ValidationError(_("Error while setting originator id: {}".format(e)))

        # Create a SEPACreditTransfer instance
        sct = SEPACreditTransfer(debtor, cat_purpose="SUPP")

        for line in self.payment_line_ids:
            sequence = line.line_sequence
            if line.partner_bank_id.acc_type != "iban":
                action = self.env.ref("base.action_res_partner_bank_account_form")
                action_dict = action.read()[0]
                action_dict.update(
                    {
                        "res_id": line.partner_bank_id.id,
                    }
                )
                raise RedirectWarning(
                    message=_(
                        f"Incorrect IBAN for '{line.partner_id.display_name}' line {sequence}"
                    ),
                    action=action_dict,
                    button_text=_("Bank Settings"),
                )

            creditor_iban = line.partner_bank_id.acc_number.replace(" ", "")
            creditor_name = line.partner_id.name
            # Create the creditor account
            creditor = Account(creditor_iban, creditor_name)
            # Add the transaction
            sct.add_transaction(
                creditor,
                amount=line.amount_currency,
                purpose=line.communication,
                eref=f"{sequence}",
                due_date=line.date,
            )

        # Render the SEPA document
        xml_string = sct.render()
        filename = f"{self.name}.xml"
        return xml_string, filename
