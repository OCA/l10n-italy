# Copyright 2013-2015 Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2016 Alessandro Camilli <alessandro.camilli@openforce.it>
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    pain_version = fields.Selection(
        selection_add=[
            ("CBIBdyPaymentRequest.00.04.01", "CBIBdyPaymentRequest.00.04.01"),
            (
                "CBIBdyCrossBorderPaymentRequest.00.01.01",
                "CBIBdyCrossBorderPaymentRequest.00.01.01",
            ),
        ],
        ondelete={
            "CBIBdyPaymentRequest.00.04.01": "set null",
            "CBIBdyCrossBorderPaymentRequest.00.01.01": "set null",
        },
    )

    def get_xsd_file_path(self):
        self.ensure_one()
        if self.pain_version in [
            "CBIBdyPaymentRequest.00.04.01",
            "CBIBdyCrossBorderPaymentRequest.00.01.01",
        ]:
            path = f"l10n_it_sct_cbi/data/standards/{self.pain_version}.xsd"
        else:
            path = super().get_xsd_file_path()
        return path

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res["sepa_cbi_credit_transfer"] = {
            "mode": "multi",
            "domain": [("type", "=", "bank")],
        }
        return res
