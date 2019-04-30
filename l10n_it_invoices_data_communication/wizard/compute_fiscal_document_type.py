# -*- coding: utf-8 -*-

from openerp import api, models
from openerp.osv import expression
from ..models.communication import _get_invoice_date_domain


class ComunicazioneDatiIvaRicalcoloTipoDocumentoFiscale(models.TransientModel):
    _name = "comunicazione.dati.iva.ricalcolo.tipo.document.fiscale"
    _description = "Recompute invoices document type"

    @api.multi
    def compute(self):
        comunicazione_ids = self._context.get('active_ids')
        for wizard in self:
            for comunicazione in self.env['comunicazione.dati.iva'].\
                    browse(comunicazione_ids):
                domain = [('comunicazione_dati_iva_escludi', '=', True)]
                no_journal_ids = self.env['account.journal'].search(domain).ids
                domain = [
                    ('move_id', '!=', False),
                    ('comunicazione_dati_iva_escludi', '!=', True),
                    ('move_id.journal_id', 'not in', no_journal_ids),
                    ('company_id', '>=', comunicazione.company_id.id),
                ]
                date_domain = _get_invoice_date_domain(
                    comunicazione.date_start,
                    comunicazione.date_end)
                domain = expression.AND([domain, date_domain])
                fatture = self.env['account.invoice'].search(domain)
                for fattura in fatture:
                    fattura.fiscal_document_type_id =\
                        fattura._get_document_fiscal_type(
                            type=fattura.type, partner=fattura.partner_id,
                            fiscal_position=fattura.fiscal_position,
                            journal=fattura.journal_id)[0] or False
            return {}
