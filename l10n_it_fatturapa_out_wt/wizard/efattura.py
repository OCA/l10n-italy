# Copyright 2020 Giuseppe Borruso
# Copyright 2020 Marco Colombo
# Copyright 2021 Ciro Urselli <https://github.com/CiroBoxHub>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import EFatturaOut


WT_TAX_CODE = {
    "inps": "RT03", 
    "enasarco": "RT04", 
    "enpam": "RT05", 
    "other": "RT06"}


class EFatturaOut(EFatturaOut):

    def getTipoRitenuta(wt_types, partner):
        if wt_types == "ritenuta":
            if partner.is_company:
                tipoRitenuta = "RT02"
            else:
                tipoRitenuta = "RT01"
        else:
            tipoRitenuta = WT_TAX_CODE[wt_types]
        return tipoRitenuta
