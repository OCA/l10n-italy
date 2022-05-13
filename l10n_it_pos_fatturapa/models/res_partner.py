from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if 'pec_destinatario' in vals and vals['pec_destinatario']:
            vals['electronic_invoice_subjected'] = True
            vals['electronic_invoice_obliged_subject'] = True

        if 'codice_destinatario' in vals and vals['codice_destinatario'] and vals['codice_destinatario'] != '0000000':
            vals['electronic_invoice_subjected'] = True
            vals['electronic_invoice_obliged_subject'] = True

        result = super(ResPartner, self).create(vals)
        return result

    def write(self, vals):
        if 'pec_destinatario' in vals or ('codice_destinatario' in vals and vals['codice_destinatario'] and vals['codice_destinatario'] != '0000000'):
            if 'electronic_invoice_subjected' in vals:
                vals['electronic_invoice_subjected'] = True
            else:
                vals.update({
                    'electronic_invoice_subjected': True
                })
            if 'electronic_invoice_obliged_subject' in vals:
                vals['electronic_invoice_obliged_subject'] = True
            else:
                vals.update({
                    'electronic_invoice_obliged_subject': True
                })

        result = super(ResPartner, self).write(vals)
        return result

