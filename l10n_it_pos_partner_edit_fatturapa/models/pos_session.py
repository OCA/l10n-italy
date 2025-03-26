from odoo import models

class POSSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_partner(self):
        res = super()._loader_params_res_partner()
        res["search_params"]["fields"].extend(
            [
                "electronic_invoice_subjected",
                "electronic_invoice_obliged_subject",
                "codice_destinatario",
                "pec_destinatario",
            ]
        )
        return res