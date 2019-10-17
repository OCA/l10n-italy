# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class NutsImport(models.TransientModel):
    _inherit = 'nuts.import'
    _it_state_map = {
        'ITG14': 'base.state_it_ag',  # Agrigento
        'ITC18': 'base.state_it_al',  # Alessandria
        'ITI32': 'base.state_it_an',  # Ancona
        'ITI18': 'base.state_it_ar',  # Arezzo
        'ITI34': 'base.state_it_ap',  # Ascoli Piceno
        'ITC17': 'base.state_it_at',  # Asti
        'ITF34': 'base.state_it_av',  # Avellino
        'ITF47': 'base.state_it_ba',  # Bari
        'ITF48': 'base.state_it_bt',  # Barletta-Andria-Trani
        'ITH33': 'base.state_it_bl',  # Belluno
        'ITF32': 'base.state_it_bn',  # Benevento
        'ITC46': 'base.state_it_bg',  # Bergamo
        'ITC13': 'base.state_it_bi',  # Biella
        'ITH55': 'base.state_it_bo',  # Bologna
        'ITH10': 'base.state_it_bz',  # Bolzano
        'ITC47': 'base.state_it_bs',  # Brescia
        'ITF44': 'base.state_it_br',  # Brindisi
        'ITG27': 'base.state_it_ca',  # Cagliari
        'ITG15': 'base.state_it_cl',  # Caltanissetta
        'ITF22': 'base.state_it_cb',  # Campobasso
        'ITG2C': 'base.state_it_ci',  # Carbonia-Iglesias
        'ITF31': 'base.state_it_ce',  # Caserta
        'ITG17': 'base.state_it_ct',  # Catania
        'ITF63': 'base.state_it_cz',  # Catanzaro
        'ITF14': 'base.state_it_ch',  # Chieti
        'ITC42': 'base.state_it_co',  # Como
        'ITF61': 'base.state_it_cs',  # Cosenza
        'ITC4A': 'base.state_it_cr',  # Cremona
        'ITF62': 'base.state_it_kr',  # Crotone
        'ITC16': 'base.state_it_cn',  # Cuneo
        'ITG16': 'base.state_it_en',  # Enna
        'ITI35': 'base.state_it_fm',  # Fermo
        'ITH56': 'base.state_it_fe',  # Ferrara
        'ITI14': 'base.state_it_fi',  # Firenze
        'ITF46': 'base.state_it_fg',  # Foggia
        'ITH58': 'base.state_it_fc',  # Forlì-Cesena
        'ITI45': 'base.state_it_fr',  # Frosinone
        'ITC33': 'base.state_it_ge',  # Genova
        'ITH43': 'base.state_it_go',  # Gorizia
        'ITI1A': 'base.state_it_gr',  # Grosseto
        'ITC31': 'base.state_it_im',  # Imperia
        'ITF21': 'base.state_it_is',  # Isernia
        'ITF11': 'base.state_it_aq',  # L'Aquila
        'ITC34': 'base.state_it_sp',  # La Spezia
        'ITI44': 'base.state_it_lt',  # Latina
        'ITF45': 'base.state_it_le',  # Lecce
        'ITC43': 'base.state_it_lc',  # Lecco
        'ITI16': 'base.state_it_li',  # Livorno
        'ITC49': 'base.state_it_lo',  # Lodi
        'ITI12': 'base.state_it_lu',  # Lucca
        'ITI33': 'base.state_it_mc',  # Macerata
        'ITC4B': 'base.state_it_mn',  # Mantova
        'ITI11': 'base.state_it_ms',  # Massa-Carrara
        'ITF52': 'base.state_it_mt',  # Matera
        'ITG2B': 'base.state_it_vs',  # Medio Campidano
        'ITG13': 'base.state_it_me',  # Messina
        'ITC4C': 'base.state_it_mi',  # Milano
        'ITH54': 'base.state_it_mo',  # Modena
        'ITC4D': 'base.state_it_mb',  # Monza e Brianza
        'ITF33': 'base.state_it_na',  # Napoli
        'ITC15': 'base.state_it_no',  # Novara
        'ITG26': 'base.state_it_nu',  # Nuoro
        'ITG2A': 'base.state_it_og',  # Ogliastra
        'ITG29': 'base.state_it_ot',  # Olbia-Tempio
        'ITG28': 'base.state_it_or',  # Oristano
        'ITH36': 'base.state_it_pd',  # Padova
        'ITG12': 'base.state_it_pa',  # Palermo
        'ITH52': 'base.state_it_pr',  # Parma
        'ITC48': 'base.state_it_pv',  # Pavia
        'ITI21': 'base.state_it_pg',  # Perugia
        'ITI31': 'base.state_it_pu',  # Pesaro e Urbino
        'ITF13': 'base.state_it_pe',  # Pescara
        'ITH51': 'base.state_it_pc',  # Piacenza
        'ITI17': 'base.state_it_pi',  # Pisa
        'ITI13': 'base.state_it_pt',  # Pistoia
        'ITH41': 'base.state_it_pn',  # Pordenone
        'ITF51': 'base.state_it_pz',  # Potenza
        'ITI15': 'base.state_it_po',  # Prato
        'ITG18': 'base.state_it_rg',  # Ragusa
        'ITH57': 'base.state_it_ra',  # Ravenna
        'ITF65': 'base.state_it_rc',  # Reggio Calabria
        'ITH53': 'base.state_it_re',  # Reggio Emilia
        'ITI42': 'base.state_it_ri',  # Rieti
        'ITH59': 'base.state_it_rn',  # Rimini
        'ITI43': 'base.state_it_rm',  # Roma
        'ITH37': 'base.state_it_ro',  # Rovigo
        'ITF35': 'base.state_it_sa',  # Salerno
        'ITG25': 'base.state_it_ss',  # Sassari
        'ITC32': 'base.state_it_sv',  # Savona
        'ITI19': 'base.state_it_si',  # Siena
        'ITG19': 'base.state_it_sr',  # Siracusa
        'ITC44': 'base.state_it_so',  # Sondrio
        'ITG2H': 'base.state_it_su',  # Sud Sardegna
        'ITF43': 'base.state_it_ta',  # Taranto
        'ITF12': 'base.state_it_te',  # Teramo
        'ITI22': 'base.state_it_tr',  # Terni
        'ITC11': 'base.state_it_to',  # Torino
        'ITG11': 'base.state_it_tp',  # Trapani
        'ITH20': 'base.state_it_tn',  # Trento
        'ITH34': 'base.state_it_tv',  # Treviso
        'ITH44': 'base.state_it_ts',  # Trieste
        'ITH42': 'base.state_it_ud',  # Udine
        'ITC41': 'base.state_it_va',  # Varese
        'ITH35': 'base.state_it_ve',  # Venezia
        'ITC14': 'base.state_it_vb',  # Verbano-Cusio-Ossola
        'ITC12': 'base.state_it_vc',  # Vercelli
        'ITH31': 'base.state_it_vr',  # Verona
        'ITF64': 'base.state_it_vv',  # Vibo Valentia
        'ITH32': 'base.state_it_vi',  # Vicenza
        'ITI41': 'base.state_it_vt'  # Viterbo
    }

    @api.model
    def state_mapping(self, data, node):
        mapping = super(NutsImport, self).state_mapping(data, node)
        level = data.get('level', 0)
        code = data.get('code', '')
        if self._current_country.code == 'IT' and level == 4:
            external_ref = self._it_state_map.get(code, False)
            if external_ref:
                state = self.env.ref(external_ref)
                if state:
                    mapping['state_id'] = state.id
        return mapping
