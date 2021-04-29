# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
from openerp.tools.float_utils import float_round
from openerp.addons.l10n_it_account.tools.account_tools import encode_for_export
from openerp.addons.l10n_it_fatturapa.bindings.fatturapa import (
    AltriDatiGestionaliType,
)
from datetime import datetime

class WizardExportFatturapa(models.TransientModel):
    _inherit = "wizard.export.fatturapa"

    def setDettaglioLinea(
        self, line_no, line, body, price_precision, uom_precision):

        DettaglioLinea = super(WizardExportFatturapa, self).setDettaglioLinea(
                    line_no, line, body, price_precision, uom_precision)
        custom_lines = self.env['out_custom_fields'].search([])

        for custom_line in custom_lines:
            dati_gestionali = AltriDatiGestionaliType()
            dati_gestionali.TipoDato = encode_for_export(custom_line.name, 10)
            if custom_line.field_ref:
                list_fields = custom_line.field_ref.split(".")
            else:
                raise UserError(_("Error! The '%s' "
                                  "field on 'AltriDatiGestionali' "
                                  "must contain a valid value.")
                                % custom_line.name)
            temp_line = line
            for item in list_fields:
                field_type = getattr(temp_line, '_fields', {}).get(item).type
                if field_type in ['char', 'text', 'float',
                                  'integer', 'date', 'datetime']:
                    value_var = temp_line.__getattribute__(item)
                else:
                    temp_line = temp_line.__getattribute__(item)

            if value_var and custom_line.active:
                if field_type in ['char', 'text']:
                    dati_gestionali.RiferimentoTesto = \
                        encode_for_export(value_var, 60)
                if field_type in ['float', 'integer']:
                    if not custom_line.force_text:
                        dati_gestionali.RiferimentoNumero = '%.8f' % value_var
                    else:
                        dati_gestionali.RiferimentoTesto = '%.8f' % value_var
                if field_type in ['date', 'datetime']:
                    if not custom_line.force_text:
                        dati_gestionali.RiferimentoData = datetime.strptime(
                            value_var, '%Y-%m-%d %H:%M:%S').date()
                    else:
                        d_date = datetime.strptime(
                            value_var, '%Y-%m-%d %H:%M:%S')
                        dati_gestionali.RiferimentoTesto = \
                            d_date.strftime('%Y-%m-%d')

                DettaglioLinea.AltriDatiGestionali.append(dati_gestionali)
        return DettaglioLinea