# Copyright 2022 Dinamiche Aziendali srl
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_pos_payment_method(self):
        result = super()._loader_params_pos_payment_method()
        result["search_params"]["fields"].append("fiscalprinter_payment_type")
        result["search_params"]["fields"].append("fiscalprinter_payment_index")
        return result

    def _loader_params_account_tax(self):
        result = super()._loader_params_account_tax()
        result["search_params"]["fields"].append("fpdeptax")
        return result
