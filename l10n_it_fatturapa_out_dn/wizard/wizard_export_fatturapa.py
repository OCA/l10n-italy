
from odoo import models, fields, api
from odoo.addons.l10n_it_fatturapa.bindings.fatturapa import (
    DatiDDTType,
)


class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    @api.model
    def default_get(self, fields):
        res = super(WizardExportFatturapa, self).default_get(fields)
        invoice_ids = self.env.context.get('active_ids', False)
        invoices = self.env['account.invoice'].browse(invoice_ids)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if line.delivery_note_id:
                    res['include_dn_data'] = 'dati_ddt'
                    return res
        return res

    include_dn_data = fields.Selection([
        ('dati_ddt', 'Include DN Data'),
        ],
        string="DN Data",
        help="Include DN data: The field must be entered when a transport "
             "document associated with a deferred invoice is present\n"
    )

    def setDatiDDT(self, invoice, body):
        res = super(WizardExportFatturapa, self).setDatiDDT(
            invoice, body)
        if self.include_dn_data == 'dati_ddt':
            for dn in invoice.delivery_note_ids:
                DatiDDT = DatiDDTType(
                    NumeroDDT=dn.name[-20:],
                    DataDDT=dn.date
                )
                for n, line in enumerate(invoice.invoice_line_ids, start=1):
                    if line.display_type not in ('line_section', 'line_note') \
                            and line.delivery_note_id == dn:
                        DatiDDT.RiferimentoNumeroLinea.append(n)
                body.DatiGenerali.DatiDDT.append(DatiDDT)
        return res
