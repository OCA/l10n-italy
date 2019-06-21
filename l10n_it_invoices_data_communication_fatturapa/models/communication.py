
from odoo import models, fields


class Communication(models.Model):
    _inherit = 'comunicazione.dati.iva'
    exclude_e_invoices = fields.Boolean("Exclude e-invoices", default=True)

    def _get_fatture_emesse_domain(self):
        domain = super(Communication, self)._get_fatture_emesse_domain()
        if self.exclude_e_invoices:
            domain.append(('fatturapa_attachment_out_id', '=', False))
        return domain

    def _get_fatture_ricevute_domain(self):
        domain = super(Communication, self)._get_fatture_ricevute_domain()
        if self.exclude_e_invoices:
            domain.append(('fatturapa_attachment_in_id', '=', False))
        return domain
