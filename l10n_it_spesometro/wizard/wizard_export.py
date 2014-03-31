# -*- coding: utf-8 -*-
#################################################################################
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import pdb
from osv import fields,osv
from tools.translate import _
from datetime import datetime
from StringIO import StringIO
import base64
from decimal import *

class wizard_spesometro_export(osv.osv_memory):
    
    _name = "wizard.spesometro.export"
    _description = 'Use this wizard to export fiscal file'
    _columns={
        'file_spesometro': fields.binary('File spesometro', readonly=True),
    }
    
    def _split_string_positional_field(self, string):
        '''
        Da manuale:
        Con riferimento ai campi non posizionali, nel caso in cui la lunghezza del dato da inserire 
        ecceda i 16 caratteri disponibili, dovraÃŒâ‚¬ essere inserito un ulteriore elemento con un identico 
        campo-codice e con un campo-valore il cui primo carattere dovraÃŒâ‚¬ essere impostato con il simbolo Ã¢â‚¬Å“+Ã¢â‚¬ï¿½, 
        mentre i successivi quindici potranno essere utilizzati per la continuazione del dato da inserire. 
        Tale situazione puoÃŒâ‚¬ verificarsi solo per alcuni campi con formato AN.
        '''
        # Prima parte:
        res = []
        res.append(string[:16])
        length = 15
        # Parte in eccesso:
        str_eccesso = string[16:]
        str_split = [str_eccesso[i:i+length] for i in range(0, len(str_eccesso), length)]
        for s in str_split:
            new_string = '+' + s
            res.append(new_string)
        return res
    
    def _add_field(self, cr, uid, format_id, pic, prog_sezione, val_id, val, partner_id=False):
        rcd = ''
        # Text -> if is longer than 16 chars, will be splitted in 2 o more fields.
        if format_id == 'AN' and len(val) > 16:
            str_split = self._split_string_positional_field(val)
            for s in str_split:
                rcd += '{0:2s}'.format(pic)
                rcd += '{0:3s}'.format(prog_sezione)
                rcd += '{0:3d}'.format(val_id)
                rcd += '{0:16s}'.format(s)
        else:             
            rcd += '{0:2s}'.format(pic)
            rcd += '{0:3s}'.format(prog_sezione)
            rcd += '{0:03d}'.format(val_id)
            # Text -> shorter than 16 chars.
            if format_id == 'AN':
                rcd += '{0:16s}'.format(val)
            # Combobox -> if false do nothing, if true set value '      1'    
            elif format_id == 'CB':
                if val_id:
                    rcd += '{0:16d}'.format('1')
            # Positive number -> right align, space filled        
            elif format_id == 'NP':
                if val > 0 :
                    rcd += '{0:>16.0f}'.format(val)
            # Fiscal code -> May of vat number too, left align
            elif format_id == 'CF':
                rcd += '{0:16s}'.format(val)
            # Birthday, (extracted by parter_id) -> day, month, year, left align    
            elif format_id == 'DT':
                rcd += '{0:>16s}'.format(datetime.strptime(val, "%Y-%m-%d").strftime("%d%m%Y"))
            # Born district, (extracted by parter_id) -> 2 chars, left align
            elif format_id == 'PN':
                rcd += '{0:16s}'.format(val)
            # Name, extracted by parter_id -> 2 chars, left align
            elif format_id == 'r1':
                rcd += '{0:16s}'.format(val)
            # Born in city, extracted by parter_id -> 2 chars, left align
            elif format_id == 'r3':
                rcd += '{0:16s}'.format(val)
            # Live in city, extracted by parter_id -> 2 chars, left align
            elif format_id == 'r4':
                rcd += '{0:16s}'.format(val) 
            # Live in country, extracted by parter_id -> 2 chars, left align
            # Warning: code extracted by res.country of l10n_it_base v7.0.02 (2014)
            # Warning: it is a numeric code, right align space filled but  Ã¢â‚¬Â¦
            #  must be 3 digit len -> '    011'
            elif format_id == 'r5':
                rcd += '{0:16s}'.format(val)
            # Live in addresss, extracted by parter_id -> 2 chars, left align
            elif format_id == 'r6':
                rcd += '{0:16s}'.format(val)
            # recording date
            elif format_id == 'dr':
                rcd += '{0:16s}'.format(val)
            # document date
            elif format_id == 'dd':
                rcd += '{0:16s}'.format(val)
            # document number
            elif format_id == 'dn':
                rcd += '{0:16s}'.format(val)
            
            return rcd
    
    def _record_A(self, cr, uid, comunicazione, context=None):
        
        if not comunicazione.soggetto_trasmissione_codice_fiscale:
            raise osv.except_osv(_('Errore comunicazione!'),_("Manca il codice fiscale dell'incaricato alla trasmissione"))
        
        rcd = "A"
        rcd += '{0:14s}'.format("") # Filler 
        rcd += "NSP00" # codice fornitura 
        rcd += comunicazione.tipo_fornitore # 01 - Soggetti che inviano la propria comunicazione 10 -Intermediari
        rcd += '{0:16s}'.format(comunicazione.soggetto_trasmissione_codice_fiscale) # cd fiscale  (se intermediaro va messo quello dell'intermediario)
        rcd += '{0:483s}'.format("")# Filler 
        #rcd += '{0:4s}'.format(str(comunicazione.progressivo_telematico).zfill(4)) # dich.su piÃƒÂ¹ invii: Progressivo dell'invio telematico 
        rcd += '{0:4s}'.format("0".zfill(4)) # dich.su piÃƒÂ¹ invii: Progressivo dell'invio telematico 
        rcd += '{0:4s}'.format("0".zfill(4)) # dich.su piÃƒÂ¹ invii: Numero totale degli invii telematici
        rcd += '{0:100s}'.format("") # Filler 
        rcd += '{0:1068s}'.format("") # Filler
        rcd += '{0:200s}'.format("") # Filler 
        rcd += "A" # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd

    def _record_B(self, cr, uid, comunicazione, context=None):
        rcd = "B"
        rcd += '{0:16s}'.format(comunicazione.soggetto_codice_fiscale)    
        rcd += '{0:8s}'.format("1".zfill(8)) # Progressivo modulo - vale 1    
        rcd += '{0:3s}'.format("") #  Spazio a disposizione dell'utente
        rcd += '{0:25s}'.format("")  # Filler 
        rcd += '{0:20s}'.format("")  #  Spazio a disposizione dell'utente
        rcd += '{0:16s}'.format("")  #  Identificativo del produttore del software (codice fiscale)
        # tipo comunicazione ( alterntative: ordinaria,sostitutiva o  di annullamento )
        if comunicazione.tipo == 'ordinaria':
            rcd += "1" 
        else:
            rcd += "0"
        if comunicazione.tipo == 'sostitutiva':
            rcd += "1" 
        else:
            rcd += "0"
        if comunicazione.tipo == 'annullamento':
            rcd += "1" 
        else:
            rcd += "0"
        # campi x annullamento e sostituzione
        if comunicazione.comunicazione_da_sostituire_annullare == 0:
            rcd += '{0:17s}'.format("".zfill(17))
        else: 
            rcd += '{0:17s}'.format(str(comunicazione_da_sostituire_annullare).zfill(17))
        if comunicazione.documento_da_sostituire_annullare == 0:
            rcd += '{0:6s}'.format("".zfill(6))
        else:
            rcd += '{0:6s}'.format(str(comunicazione.documento_da_sostituire_annullare).zfill(6))
        # formato dati: aggregata o analitica (caselle alternative)
        if comunicazione.formato_dati == 'aggregati':
            rcd += "10" 
        else:
            rcd += "01" 
        # Quadri compilati
        if comunicazione.line_FA_ids :
            rcd += "1" 
        else:
            rcd += "0"
        if comunicazione.line_SA_ids :
            rcd += "1" 
        else:
            rcd += "0"
        if comunicazione.line_BL_ids :
            rcd += "1" 
        else:
            rcd += "0"
        #if comunicazione.quadro_FE :
        #    rcd += "1" 
        #else:
        rcd += "0"  
        #if comunicazione.quadro_FR :
        #    rcd += "1" 
        #else:
        rcd += "0"
        #if comunicazione.quadro_NE :
        #    rcd += "1" 
        #else:
        rcd += "0"  
        #if comunicazione.quadro_NR :
        #    rcd += "1" 
        #else:
        rcd += "0"
        #if comunicazione.quadro_DF :
        #    rcd += "1" 
        #else:
        rcd += "0"
        #if comunicazione.quadro_FN :
        #    rcd += "1" 
        #else:
        rcd += "0"  
        if comunicazione.line_SE_ids :
            rcd += "1" 
        else:
            rcd += "0"
        #if comunicazione.quadro_TU :
        #    rcd += "1" 
        #else:
        rcd += "0"  
        
        rcd += "1" #  Quadro TA  - RIEPILOGO
        #Partita IVA , Codice AttivitÃƒÂ  e riferimenti del Soggetto cui si riferisce la comunicazione
        rcd += '{0:11s}'.format(comunicazione.soggetto_partitaIVA) # PARTITA IVA
        if not comunicazione.soggetto_codice_attivita:
                raise osv.except_osv(_('Errore comunicazione!'),_("Manca il codice attivitÃƒÂ "))
        rcd += '{0:6s}'.format(comunicazione.soggetto_codice_attivita) # CODICE attivitÃƒÂ   (6 caratteri) --> obbligatorio
        tel = comunicazione.soggetto_telefono
        rcd += '{0:12s}'.format(tel.replace(' ','') or '') # telefono
        fax = comunicazione.soggetto_fax
        rcd += '{0:12s}'.format(fax.replace(' ','') or '') # fax
        rcd += '{0:50s}'.format(comunicazione.soggetto_email or '') # ind posta elettronica
        # Dati Anagrafici del Soggetto cui si riferisce la comunicazione - Persona Fisica
        if comunicazione.soggetto_forma_giuridica == 'persona_fisica':
            if not comunicazione.soggetto_pf_cognome or not comunicazione.soggetto_pf_nome or not comunicazione.soggetto_pf_sesso \
                or not comunicazione.soggetto_pf_data_nascita or not comunicazione.soggetto_pf_comune_nascita or not comunicazione.soggetto_pf_provincia_nascita:
                raise osv.except_osv(_('Errore comunicazione!'),_("Soggetto obbligato: Inserire tutti i dati della persona fisica"))
            rcd += '{0:24s}'.format(comunicazione.soggetto_pf_cognome)  # cognome
            rcd += '{0:20s}'.format(comunicazione.soggetto_pf_nome)  # nome
            rcd += '{0:1s}'.format(comunicazione.soggetto_pf_sesso) # sesso
            rcd += '{0:8s}'.format(datetime.strptime(comunicazione.soggetto_pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y")) # data nascita
            rcd += '{0:40s}'.format(comunicazione.soggetto_pf_comune_nascita)  # comune di nascita
            rcd += '{0:2s}'.format(comunicazione.soggetto_pf_provincia_nascita) # provincia comune di nascita
            rcd += '{0:60s}'.format("") # persona giuridica
        else:
            if not comunicazione.soggetto_pg_denominazione:
                raise osv.except_osv(_('Errore comunicazione!'),_("Soggetto obbligato: Inserire tutti i dati della persona giuridica"))
            rcd += '{0:24s}'.format("")  # cognome
            rcd += '{0:20s}'.format("")  # nome
            rcd += '{0:1s}'.format("") # sesso
            rcd += '{0:8s}'.format("".zfill(8)) # data nascita
            rcd += '{0:40s}'.format("")  # comune di nascita
            rcd += '{0:2s}'.format("") # provincia comune di nascita
            rcd += '{0:60s}'.format(comunicazione.soggetto_pg_denominazione) # persona giuridica
        
        rcd += '{0:4d}'.format(comunicazione.anno) #Ã‚Â anno riferimento
        #Ã‚Â Mese di riferimento : Da valorizzare obbligatoriamente solo se presenti Acquisti da Operatori di San Marino. In tutti gli altri casi non deve essere compilato
        if comunicazione.periodo == 'trimestre' and comunicazione.trimestre:
            rcd += '{0:2s}'.format( str(comunicazione.trimestre) + "T")
        elif comunicazione.periodo == 'mese' and comunicazione.mese:
            rcd += '{0:2s}'.format( str(comunicazione.mese).zfill(2))
        else:
            rcd += '{0:2s}'.format("")  
        # Dati del Soggetto tenuto alla comunicazione (soggetto che effettua la comunicazione, se diverso dal soggetto cui si riferisce la comunicazione)
        rcd += '{0:16s}'.format(comunicazione.soggetto_cm_codice_fiscale or "") 
        rcd += '{0:2s}'.format(comunicazione.tipo_fornitore or "01") # codice carica 
        rcd += '{0:8s}'.format("".zfill(8)) # data inizio procedura 
        rcd += '{0:8s}'.format("".zfill(8)) #Ã‚Â data fine procedura
        # Dati anagrafici del soggetto tenuto alla comunicazione - Persona fisica
        # (Obbligatorio e da compilare solo se si tratta di Persona Fisica. )
        if comunicazione.soggetto_cm_forma_giuridica == 'persona_fisica':
            if not comunicazione.soggetto_cm_pf_cognome or not comunicazione.soggetto_cm_pf_nome or not comunicazione.soggetto_cm_pf_sesso \
                or not comunicazione.soggetto_cm_pf_data_nascita or not comunicazione.soggetto_cm_pf_comune_nascita or not comunicazione.soggetto_cm_pf_provincia_nascita:
                raise osv.except_osv(_('Errore comunicazione!'),_("Soggetto tenuto alla comunicazione: Inserire tutti i dati della persona fisica"))
            rcd += '{0:24s}'.format(comunicazione.soggetto_cm_pf_cognome) # cognome
            rcd += '{0:20s}'.format(comunicazione.soggetto_cm_pf_nome) # nome
            rcd += '{0:1s}'.format(comunicazione.soggetto_cm_pf_sesso)  # sesso
            rcd += '{0:8s}'.format(datetime.strptime(comunicazione.soggetto_cm_pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y")) # data nascita
            rcd += '{0:40s}'.format(comunicazione.soggetto_cm_pf_comune_nascita) # comune di nascita
            rcd += '{0:2s}'.format(comunicazione.soggetto_cm_pf_provincia_nascita) # provincia comune di nascita
            rcd += '{0:60s}'.format("") #Ã‚Â persona giuridica
        else:
            if not comunicazione.soggetto_cm_pg_denominazione:
                raise osv.except_osv(_('Errore comunicazione!'),_("Soggetto tenuto alla comunicazione: Inserire tutti i dati della persona giuridica"))
            rcd += '{0:24s}'.format("") # cognome
            rcd += '{0:20s}'.format("") # nome
            rcd += '{0:1s}'.format("")  # sesso
            rcd += '{0:8s}'.format("".zfill(8)) # data nascita
            rcd += '{0:40s}'.format("") # comune di nascita
            rcd += '{0:2s}'.format("") # provincia comune di nascita
            rcd += '{0:60s}'.format(comunicazione.soggetto_cm_pg_denominazione) #Ã‚Â persona giuridica
            
        # Impegno alla trasmissione telematica
        if comunicazione.tipo_fornitore == '10' and not comunicazione.soggetto_trasmissione_codice_fiscale:
            raise osv.except_osv(_('Errore comunicazione!'),_("Manca il codice fiscale dell'intermediario incaricato alla trasmissione telematica"))
        rcd += '{0:16s}'.format(comunicazione.soggetto_trasmissione_codice_fiscale or '') # Codice fiscale dell'intermediario 
        rcd += '{0:5s}'.format(str(comunicazione.soggetto_trasmissione_numero_CAF).zfill(5)) # Numero di iscrizione all'albo del C.A.F.
        rcd += '{0:1s}'.format(comunicazione.soggetto_trasmissione_impegno)# Impegno a trasmettere in via telematica la comunicazione 
                    # Dato obbligatorio Vale 1 se la comunicazione ÃƒÂ¨ stata predisposta dal soggetto obbligato
                    # Vale 2 se ÃƒÂ¨ stata predisposta dall'intermediario. 
        rcd += '{0:1s}'.format("") # Filler
        if not comunicazione.soggetto_trasmissione_data_impegno:
            raise osv.except_osv(_('Errore comunicazione!'),_("Manca la data dell'impegno alla trasmissione"))
        rcd += '{0:8s}'.format(datetime.strptime(comunicazione.soggetto_trasmissione_data_impegno, "%Y-%m-%d").strftime("%d%m%Y")) # Data dell'impegno
        # Spazio riservato al Servizio telematico
        rcd += '{0:1258s}'.format("") # Filler
        rcd += '{0:20s}'.format("") # Spazio riservato al Servizio Telematico 
        rcd += '{0:18s}'.format("") # Filler
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
        
    def _record_C_FA(self, cr, uid, line, prog_modulo, prog_sezione, context=None):
        prog_sezione = str(prog_sezione).zfill(3)
        
        rcd = "C"
        rcd += '{0:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale) # codice fiscale soggetto obbligato
        rcd += '{0:8s}'.format(str(prog_modulo).zfill(8)) # Progressivo modulo 
        rcd += '{0:3s}'.format("") # Filler 
        rcd += '{0:25s}'.format("") # Filler 
        rcd += '{0:20s}'.format("") # Spazio utente 
        rcd += '{0:16s}'.format("") # Filler 
        
        # QUADRO FA
        # Partita iva o codice fiscale presenti se non si tratta di documento riepilogativo(ES: scheda carburante)
        if not line.partita_iva and not line.codice_fiscale and not line.documento_riepilogativo:
            raise osv.except_osv(_('Errore comunicazione!'),_("Inserire Codice Fiscale o partita IVA su partner %s") % (line.partner_id.name,))
        # Doc. riepilogativo : non ammessi codice fiscale o partita iva
        if line.documento_riepilogativo and (line.partita_iva or line.codice_fiscale) :
            raise osv.except_osv(_('Errore comunicazione!'),_("Documento riepilogativo per partner %s, togliere Codice Fiscale E partita IVA") % (line.partner_id.name,))
        
        #pdb.set_trace()
        
        if line.partita_iva:
            rcd += self._add_field(cr, uid, 'AN', "FA", prog_sezione, 1, line.partita_iva)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "001" )
            #rcd += '{0:16s}'.format(line.partita_iva) 
        elif line.codice_fiscale:
            rcd += self._add_field(cr, uid, 'AN', "FA", prog_sezione, 2, line.codice_fiscale)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "002" )
            #rcd += '{0:16s}'.format(line.codice_fiscale)
        if line.documento_riepilogativo:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 3, 1)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "003" ) + '{0:>16s}'.format('1')
        # Numero operazioni attive aggregate 
        if line.numero_operazioni_attive_aggregate > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 4, line.numero_operazioni_attive_aggregate)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "004" ) + '{0:16d}'.format(line.numero_operazioni_attive_aggregate)
        # Numero operazioni passive aggregate 
        if line.numero_operazioni_passive_aggregate > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 5, line.numero_operazioni_passive_aggregate)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "005" ) + '{0:16d}'.format(line.numero_operazioni_passive_aggregate)
        # Noleggio / Leasing
        if line.noleggio:
            rcd += self._add_field(cr, uid, 'AN', "FA", prog_sezione, 6, line.noleggio)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "006" ) + '{0:16s}'.format(line.noleggio)
            
        # OPERAZIONI ATTIVE
        if line.attive_imponibile_non_esente > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 7, line.attive_imponibile_non_esente)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "007" ) + '{0:16.0f}'.format(line.attive_imponibile_non_esente)
        # Totale imposta
        if line.attive_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 8, line.attive_imposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "008" ) + '{0:16.0f}'.format(line.attive_imposta)
        # Totale operazioni con IVA non esposta
        if line.attive_operazioni_iva_non_esposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 9, line.attive_operazioni_iva_non_esposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "009" ) + '{0:16.0f}'.format(line.attive_operazioni_iva_non_esposta)
        # Totale note di variazione a debito per la controparte
        if line.attive_note_variazione > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 10, line.attive_note_variazione)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "010" ) + '{0:16.0f}'.format(line.attive_note_variazione)
        if line.attive_note_variazione_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 11, line.attive_note_variazione_imposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "011" ) + '{0:16.0f}'.format(line.attive_note_variazione_imposta)
        
        # OPERAZIONI PASSIVE
        # Totale operazioni imponibili, non imponibili ed esenti
        if line.passive_imponibile_non_esente > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 12, line.passive_imponibile_non_esente)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "012" ) + '{0:16.0f}'.format(line.passive_imponibile_non_esente)
        if line.passive_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 13, line.passive_imposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "013" ) + '{0:16.0f}'.format(line.passive_imposta)
        if line.passive_operazioni_iva_non_esposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 14, line.passive_operazioni_iva_non_esposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "014" ) + '{0:16.0f}'.format(line.passive_operazioni_iva_non_esposta)
        if line.passive_note_variazione > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 15, line.passive_note_variazione)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "015" ) + '{0:16.0f}'.format(line.passive_note_variazione)
        if line.passive_note_variazione_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "FA", prog_sezione, 16, line.passive_note_variazione_imposta)
            #rcd += '{0:8s}'.format("FA" + prog_sezione + "016" ) + '{0:16.0f}'.format(line.passive_note_variazione_imposta)

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 -len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    
    def _record_C_SA(self, cr, uid, line, prog_modulo, prog_sezione, context=None):
        prog_sezione = str(prog_sezione).zfill(3)
        
        if not line.codice_fiscale:
            raise osv.except_osv(_('Errore comunicazione!'),_("Manca codice fiscale su partner %s") % (line.partner_id.name,))
        rcd = "C"
        rcd += '{0:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale) # codice fiscale soggetto obbligato
        rcd += '{0:8s}'.format(str(prog_modulo).zfill(8)) # Progressivo modulo 
        rcd += '{0:3s}'.format("") # Filler 
        rcd += '{0:25s}'.format("") # Filler 
        rcd += '{0:20s}'.format("") # Spazio utente 
        rcd += '{0:16s}'.format("") # Filler 
        
        rcd += self._add_field(cr, uid, 'AN', "SA", prog_sezione, 1, line.codice_fiscale)
        #rcd += '{0:8s}'.format("SA" + prog_sezione + "001" ) + '{0:16s}'.format(line.codice_fiscale)
        if line.numero_operazioni:
            rcd += self._add_field(cr, uid, 'NP', "SA", prog_sezione, 2, line.numero_operazioni)
            #rcd += '{0:8s}'.format("SA" + prog_sezione + "002" ) + '{0:16d}'.format(line.numero_operazioni)
        if line.importo_complessivo:
            rcd += self._add_field(cr, uid, 'NP', "SA", prog_sezione, 3, line.importo_complessivo)
            #rcd += '{0:8s}'.format("SA" + prog_sezione + "003" ) + '{0:16.0f}'.format(line.importo_complessivo) 
        if line.noleggio:
            rcd += self._add_field(cr, uid, 'AN', "SA", prog_sezione, 4, line.noleggio)
            #rcd += '{0:8s}'.format("SA" + prog_sezione + "004" ) + '{0:16s}'.format(line.noleggio) 

        # riempio fino a 1900 caratteri
        rcd += " " * (1897 -len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    
    def _record_C_BL(self, cr, uid, line, prog_modulo, prog_sezione, context=None):
        
        prog_sezione = str(prog_sezione).zfill(3)
        
        # Controlli
        # ...Operazioni con paesi con fiscalitÃƒÂ  privilegiata (ÃƒÂ¨ obbligatorio compilare le sezioni BL001, BL002 e almeno un campo delle sezioni BL003, BL004, BL005, BL006, BL007, BL008)
        if line.operazione_fiscalita_privilegiata:
            if (not line.pf_cognome or not line.pf_nome) and not line.pg_denominazione:
                raise osv.except_osv(_("Errore quadro BL"), _(" - Partner %s! Cognome e nome obbligatori oppure ragione sociale per soggetto giuridico") % (line.partner_id.name ,) )
        # ...Operazioni con soggetti non residenti (ÃƒÂ¨ obbligatorio compilare le sezioni BL001, BL002 e almeno un campo delle sezioni BL003 e BL006)
        if line.operazione_con_soggetti_non_residenti:
            if (not line.pf_cognome or not line.pf_nome) and not line.pg_denominazione:
                raise osv.except_osv(_("Errore quadro BL"), _(" - Partner %s! Cognome e nome obbligatori oppure ragione sociale per soggetto giuridico") % (line.partner_id.name ,) )
            if line.pf_cognome and not line.pf_data_nascita and not line.pf_codice_stato_estero:
                raise osv.except_osv(_("Errore quadro BL - Partner %s! Inserire alemno uno dei seguenti valori: \
                    Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato") % (line.partner_id.name ,) )
        # ...Acquisti di servizi da soggetti non residenti (ÃƒÂ¨ obbligatorio compilare le sezioni BL001, BL002 e almeno un campo della sezione BL006) 
        if line.Acquisto_servizi_da_soggetti_non_residenti:
            if (not line.pf_cognome or not line.pf_nome) and not line.pg_denominazione:
                raise osv.except_osv(_("Errore quadro BL"), _(" - Partner %s! Cognome e nome obbligatori oppure ragione sociale per soggetto giuridico") % (line.partner_id.name ,) )
            if line.pf_cognome and not line.pf_data_nascita and not line.pf_codice_stato_estero:
                raise osv.except_osv(_("Errore quadro BL"), _(" - Partner %s! Inserire alemno uno dei seguenti valori: \
                    Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato") % (line.partner_id.name ,) )
        
        rcd = "C"
        rcd += '{0:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale) # codice fiscale soggetto obbligato
        rcd += '{0:8s}'.format(str(prog_modulo).zfill(8)) # Progressivo modulo 
        rcd += '{0:3s}'.format("") # Filler 
        rcd += '{0:25s}'.format("") # Filler 
        rcd += '{0:20s}'.format("") # Spazio utente 
        rcd += '{0:16s}'.format("") # Filler 
        
        # Dati anagrafici
        # .. persona fisica
        if line.pf_cognome:
            if not line.pf_nome or not line.pf_data_nascita or not line.pf_comune_stato_nascita or not line.pf_provincia_nascita \
                or not line.pf_codice_stato_estero:
                raise osv.except_osv('Error', _('Completare dati persona fisica nel quadro BL del partner: %s') %(line.partner_id.name,))
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 1, line.pf_cognome)
            #str_split = self._split_string_positional_field(line.pf_cognome)
            #for s in str_split:   
                #rcd += '{0:8s}'.format("BL" + "001" + "001" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 2, line.pf_nome)
            #str_split = self._split_string_positional_field(line.pf_nome)
            #for s in str_split:   
                #rcd += '{0:8s}'.format("BL" + "001" + "002" )  + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'DT', "BL", "001", 3, line.pf_data_nascita)
            #rcd += '{0:8s}'.format("BL" + "001" + "003" ) + '{0:16s}'.format(datetime.strptime(line.pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y")) # Data di nascita
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 4, line.pf_comune_stato_nascita)
            #str_split = self._split_string_positional_field(line.pf_comune_stato_nascita)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("BL" + "001" + "004" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 5, line.pf_provincia_nascita)
            #rcd += '{0:8s}'.format("BL" + "001" + "005" ) + '{0:16s}'.format(line.pf_provincia_nascita)
            rcd += self._add_field(cr, uid, 'NP', "BL", "001", 6, line.pf_codice_stato_estero)
            #rcd += '{0:8s}'.format("BL" + "001" + "006" ) + '{0:>16s}'.format(line.pf_codice_stato_estero)
        # .. persona giuridica
        if line.pg_denominazione:
            if not line.pg_citta_estera_sede_legale or not line.pg_codice_stato_estero or not line.pg_indirizzo_sede_legale:
                raise osv.except_osv('Error', _('Completare dati persona giuridica nel quadro BL del partner: %s : Citta estera - Codice Stato estero - Indirizzo') %(line.partner_id.name,))
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 7, line.pg_denominazione)
            #str_split = self._split_string_positional_field(line.pg_denominazione)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("BL" + "001" + "007" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 8, line.pg_citta_estera_sede_legale)
            #str_split = self._split_string_positional_field(line.pg_citta_estera_sede_legale)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("BL" + "001" + "008" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'NP', "BL", "001", 9, line.pg_codice_stato_estero)
            #rcd += '{0:8s}'.format("BL" + "001" + "009" ) + '{0:>16s}'.format(line.pg_codice_stato_estero)
            rcd += self._add_field(cr, uid, 'AN', "BL", "001", 10, line.pg_indirizzo_sede_legale)
            #str_split = self._split_string_positional_field(line.pg_indirizzo_sede_legale)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("BL" + "001" + "010" ) + '{0:16s}'.format(s)
        # Codice identificativo IVA
        if line.codice_identificativo_IVA:
            rcd += self._add_field(cr, uid, 'AN', "BL", "002", 1, line.codice_identificativo_IVA)
            #rcd += '{0:8s}'.format("BL" + "002" + "001" ) + '{0:16s}'.format(line.codice_identificativo_IVA or '')
        # Operazioni con paesi con fiscalitÃƒÂ  privilegiata
        #rcd += '{0:8s}'.format("BL" + "002" + "002" )
        if line.operazione_fiscalita_privilegiata:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 2, 1)
            #rcd += '{0:>16s}'.format("1")
        else:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 2, 0)
            #rcd += '{0:>16s}'.format("0")
            
        # Operazioni con soggetti non residenti
        #rcd += '{0:8s}'.format("BL" + "002" + "003" ) 
        if line.operazione_con_soggetti_non_residenti:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 3, 1)
            #rcd += '{0:>16s}'.format("1")
        else:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 3, 0)
            #rcd += '{0:>16s}'.format("0")
        # Acquisti di servizi da soggetti non residenti
        #rcd += '{0:8s}'.format("BL" + "002" + "004" )
        if line.Acquisto_servizi_da_soggetti_non_residenti:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 4, 1)
            #rcd += '{0:>16s}'.format("1")
        else:
            rcd += self._add_field(cr, uid, 'NP', "BL", "002", 4, 0)
            #rcd += '{0:>16s}'.format("0")
            
            
        # OPERAZIONI ATTIVE
        if line.attive_importo_complessivo > 0:
            rcd += self._add_field(cr, uid, 'NP', "BL", "003", 1, line.attive_importo_complessivo)
            #rcd += '{0:8s}'.format("BL" + "003" + "001" ) + '{0:16.0f}'.format(line.attive_importo_complessivo)
        if line.attive_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "BL", "003", 2, line.attive_imposta)
            #rcd += '{0:8s}'.format("BL" + "003" + "002" ) + '{0:16.0f}'.format(line.attive_imposta)
        
        if line.operazione_fiscalita_privilegiata:
            if line.attive_non_sogg_cessione_beni > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "004", 1, line.attive_non_sogg_cessione_beni)
                #rcd += '{0:8s}'.format("BL" + "004" + "001" ) + '{0:16.0f}'.format(line.attive_non_sogg_cessione_beni)
            if line.attive_non_sogg_servizi > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "004", 2, line.attive_non_sogg_servizi)
                #rcd += '{0:8s}'.format("BL" + "004" + "002" ) + '{0:16.0f}'.format(line.attive_non_sogg_servizi)
            if line.attive_note_variazione > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "005", 1, line.attive_note_variazione)
                #rcd += '{0:8s}'.format("BL" + "005" + "001" ) + '{0:16.0f}'.format(line.attive_note_variazione)
            if line.attive_note_variazione_imposta > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "005", 2, line.attive_note_variazione_imposta)
                #rcd += '{0:8s}'.format("BL" + "005" + "002" ) + '{0:16.0f}'.format(line.attive_note_variazione_imposta)
        
        # OPERAZIONI PASSIVE
        if line.passive_importo_complessivo > 0:
            rcd += self._add_field(cr, uid, 'NP', "BL", "006", 1, line.passive_importo_complessivo)
            #rcd += '{0:8s}'.format("BL" + "006" + "001" ) + '{0:16.0f}'.format(line.passive_importo_complessivo)
        if line.passive_imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "BL", "006", 2, line.passive_imposta)
            #rcd += '{0:8s}'.format("BL" + "006" + "002" ) + '{0:16.0f}'.format(line.passive_imposta)
        
        if line.operazione_fiscalita_privilegiata:
            if line.passive_non_sogg_importo_complessivo > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "007", 1, line.passive_non_sogg_importo_complessivo)
                #rcd += '{0:8s}'.format("BL" + "007" + "001" ) + '{0:16.0f}'.format(line.passive_non_sogg_importo_complessivo)
            if line.passive_note_variazione > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "008", 1, line.passive_note_variazione)
                #rcd += '{0:8s}'.format("BL" + "008" + "001" ) + '{0:16.0f}'.format(line.passive_note_variazione)
            if line.passive_note_variazione_imposta > 0:
                rcd += self._add_field(cr, uid, 'NP', "BL", "008", 2, line.passive_note_variazione_imposta)
                #rcd += '{0:8s}'.format("BL" + "008" + "002" ) + '{0:16.0f}'.format(line.passive_note_variazione_imposta)
        
        # riempio fino a 1900 caratteri
        rcd += " " * (1897 -len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    
    def _record_D_SE(self, cr, uid, line, prog_modulo, prog_sezione, context=None):
        
        prog_sezione = str(prog_sezione).zfill(3)
        
        # Controlli
        # ...Cognome o Ragione sociale
        if (not line.pf_cognome or not line.pf_nome) and not line.pg_denominazione:
            raise osv.except_osv(_("Errore quadro SE"), _(" - Partner %s! Cognome e nome obbligatori oppure ragione sociale per soggetto giuridico") % (line.partner_id.name ,) )
        # ...
        if line.pf_cognome and not line.pf_data_nascita and not line.pf_codice_stato_estero:
            raise osv.except_osv(_("Errore quadro SE - Partner %s! Inserire alemno uno dei seguenti valori: \
                Pers.Fisica-Data di nascita, Pers.Fisica-Codice Stato") % (line.partner_id.name ,) )
        
        rcd = "D"
        rcd += '{0:16s}'.format(line.comunicazione_id.soggetto_codice_fiscale) # codice fiscale soggetto obbligato
        rcd += '{0:8s}'.format(str(prog_modulo).zfill(8)) # Progressivo modulo 
        rcd += '{0:3s}'.format("") # Filler 
        rcd += '{0:25s}'.format("") # Filler 
        rcd += '{0:20s}'.format("") # Spazio utente 
        rcd += '{0:16s}'.format("") # Filler 
        
        # Dati anagrafici
        # .. persona fisica
        if line.pf_cognome:
            if not line.pf_nome or not line.pf_data_nascita or not line.pf_comune_stato_nascita or not line.pf_provincia_nascita \
                or not line.pf_codice_stato_estero:
                raise osv.except_osv('Error', _('Completare dati persona fisica nel quadro SE del partner: %s') %(line.partner_id.name,))
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 1, line.pf_cognome)
            #str_split = self._split_string_positional_field(line.pf_cognome)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "001" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 2, line.pf_nome)
            #str_split = self._split_string_positional_field(line.pf_nome)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "002" )  + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'DT', "SE", prog_sezione, 3, line.pf_data_nascita)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "003" ) + '{0:16s}'.format(datetime.strptime(line.pf_data_nascita, "%Y-%m-%d").strftime("%d%m%Y")) # Data di nascita
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 4, line.pf_comune_stato_nascita)
            #str_split = self._split_string_positional_field(line.pf_comune_stato_nascita)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "004" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 5, line.pf_provincia_nascita)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "005" ) + '{0:16s}'.format(line.pf_provincia_nascita)
            rcd += self._add_field(cr, uid, 'NP', "SE", prog_sezione, 6, line.pf_codice_stato_estero_domicilio)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "006" ) + '{0:>16s}'.format(line.pf_codice_stato_estero_domicilio)
        # .. persona giuridica
        if line.pg_denominazione:
            if not line.pg_citta_estera_sede_legale or not line.pg_codice_stato_estero_domicilio or not line.pg_indirizzo_sede_legale:
                raise osv.except_osv('Error', _('Completare dati persona giuridica nel quadro SE del partner: %s : Citta estera - Codice Stato estero - Indirizzo') %(line.partner_id.name,))
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 7, line.pg_denominazione)
            #str_split = self._split_string_positional_field(line.pg_denominazione)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "007" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 8, line.pg_citta_estera_sede_legale)
            #str_split = self._split_string_positional_field(line.pg_citta_estera_sede_legale)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "008" ) + '{0:16s}'.format(s)
            rcd += self._add_field(cr, uid, 'NP', "SE", prog_sezione, 9, line.pg_codice_stato_estero_domicilio)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "009" ) + '{0:>16s}'.format(line.pg_codice_stato_estero_domicilio)
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 10, line.pg_indirizzo_sede_legale)
            #str_split = self._split_string_positional_field(line.pg_indirizzo_sede_legale)
            #for s in str_split:
            #    rcd += '{0:8s}'.format("SE" + prog_sezione + "010" ) + '{0:16s}'.format(s)
        # Codice identificativo IVA
        if line.codice_identificativo_IVA:
            rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 11, line.codice_identificativo_IVA)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "011" ) + '{0:16s}'.format(line.codice_identificativo_IVA)
        # Dati documento
        rcd += self._add_field(cr, uid, 'DT', "SE", prog_sezione, 12, line.data_emissione)
        rcd += self._add_field(cr, uid, 'DT', "SE", prog_sezione, 13, line.data_registrazione)
        rcd += self._add_field(cr, uid, 'AN', "SE", prog_sezione, 14, line.numero_fattura)
        #rcd += '{0:8s}'.format("SE" + prog_sezione + "012" ) + '{0:>16s}'.format(datetime.strptime(line.data_emissione, "%Y-%m-%d").strftime("%d%m%Y")) 
        #rcd += '{0:8s}'.format("SE" + prog_sezione + "013" ) + '{0:>16s}'.format(datetime.strptime(line.data_registrazione, "%Y-%m-%d").strftime("%d%m%Y")) 
        #rcd += '{0:8s}'.format("SE" + prog_sezione + "014" ) + '{0:16s}'.format(line.numero_fattura) 
        
        if line.importo > 0:
            rcd += self._add_field(cr, uid, 'NP', "SE", prog_sezione, 15, line.importo)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "015" ) + '{0:16.0f}'.format(line.importo)
        if line.imposta > 0:
            rcd += self._add_field(cr, uid, 'NP', "SE", prog_sezione, 15, line.imposta)
            #rcd += '{0:8s}'.format("SE" + prog_sezione + "016" ) + '{0:16.0f}'.format(line.imposta)
        
        # riempio fino a 1900 caratteri
        rcd += " " * (1897 -len(rcd))
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        
        return rcd
    
   
    def _record_E(self, cr, uid, comunicazione, prog_modulo, context=None):
        rcd = "E"
        rcd += '{0:16s}'.format(comunicazione.soggetto_codice_fiscale)  
        #rcd += '{0:8d}'.format(prog_modulo) # Progressivo modulo 
        rcd += '{0:8s}'.format(str(prog_modulo).zfill(8)) # Progressivo modulo 
        rcd += '{0:3s}'.format("") # Filler 
        rcd += '{0:25s}'.format("") # Filler 
        rcd += '{0:20s}'.format("") # Filler 
        rcd += '{0:16s}'.format("") # Filler 
        # Aggregate
        if comunicazione.totale_FA:
            rcd += '{0:8s}'.format("TA001001") + '{0:16d}'.format(comunicazione.totale_FA)
        if comunicazione.totale_SA:
            rcd += '{0:8s}'.format("TA002001") + '{0:16d}'.format(comunicazione.totale_SA)
        if comunicazione.totale_BL1:
            rcd += '{0:8s}'.format("TA003001") + '{0:16d}'.format(comunicazione.totale_BL1)
        if comunicazione.totale_BL2:
            rcd += '{0:8s}'.format("TA003002") + '{0:16d}'.format(comunicazione.totale_BL2)
        if comunicazione.totale_BL3:
            rcd += '{0:8s}'.format("TA003003") + '{0:16d}'.format(comunicazione.totale_BL3)
        # Analitiche
        if comunicazione.totale_FE:
            rcd += '{0:8s}'.format("TA004001") + '{0:16d}'.format(comunicazione.totale_FE)
        if comunicazione.totale_FE_R:
            rcd += '{0:8s}'.format("TA004002") + '{0:16d}'.format(comunicazione.totale_FE_R)
        if comunicazione.totale_FR:
            rcd += '{0:8s}'.format("TA005001") + '{0:16d}'.format(comunicazione.totale_FR)
        if comunicazione.totale_FR_R:
            rcd += '{0:8s}'.format("TA005002") + '{0:16d}'.format(comunicazione.totale_FR_R)
        if comunicazione.totale_NE:
            rcd += '{0:8s}'.format("TA006001") + '{0:16d}'.format(comunicazione.totale_NE)
        if comunicazione.totale_NR:
            rcd += '{0:8s}'.format("TA007001") + '{0:16d}'.format(comunicazione.totale_NR)
        if comunicazione.totale_DF:
            rcd += '{0:8s}'.format("TA008001") + '{0:16d}'.format(comunicazione.totale_DF)
        if comunicazione.totale_FN:
            rcd += '{0:8s}'.format("TA009001") + '{0:16d}'.format(comunicazione.totale_FN)
        if comunicazione.totale_SE:
            rcd += '{0:8s}'.format("TA010001") + '{0:16d}'.format(comunicazione.totale_SE)
        if comunicazione.totale_TU:
            rcd += '{0:8s}'.format("TA011001") + '{0:16d}'.format(comunicazione.totale_TU)
        
        rcd += " " * (1897 -len(rcd))
        
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        return rcd 
            
    def _record_Z(self, cr, uid, args, context=None):
        rcd = "Z"
        rcd += '{0:14s}'.format("") #Ã‚Â filler
        rcd += '{0:9s}'.format(str(args.get('numero_record_B')).zfill(9))
        rcd += '{0:9s}'.format(str(args.get('numero_record_C')).zfill(9))
        rcd += '{0:9s}'.format(str(args.get('numero_record_D')).zfill(9))
        rcd += '{0:9s}'.format(str(args.get('numero_record_E')).zfill(9))
        rcd += " " * 1846
        # Ultimi caratteri di controllo
        rcd += "A"  # Impostare al valore "A"
        rcd += "\r" # 
        rcd += "\n" # 
        return rcd
            
    def execute_export(self, cr, uid, ids, context=None):
        if len(ids) > 1:
            raise osv.except_osv('Error', _('Only one comunication'))
        
        numero_record_B = 0
        numero_record_C = 0
        numero_record_D = 0
        numero_record_E = 0
        
        comunicazione_id = context.get('active_id', False)
        comunicazione = self.pool.get('spesometro.comunicazione').browse(cr, uid, comunicazione_id)
        
        # Testata
        content = self._record_A(cr, uid, comunicazione, context=context)
        numero_record_B += 1
        content += self._record_B(cr, uid, comunicazione, context=context)
        
        # Dettaglio
        progressivo_modulo = 0
        progressivo_sezione = 0
        sezione_max = 3
        # .. quadro FA
        for line in comunicazione.line_FA_ids:
            progressivo_modulo +=1
            progressivo_sezione +=1
            if progressivo_sezione > sezione_max :
                progressivo_sezione = 1
            content += self._record_C_FA(cr, uid, line, progressivo_modulo, progressivo_sezione, context=context)
            numero_record_C += 1
        # .. quadro SA
        progressivo_sezione = 0
        sezione_max = 10
        for line in comunicazione.line_SA_ids:
            progressivo_modulo +=1
            progressivo_sezione +=1
            if progressivo_sezione > sezione_max :
                progressivo_sezione = 1
            content += self._record_C_SA(cr, uid, line, progressivo_modulo, progressivo_sezione, context=context)
            numero_record_C += 1
        
        # .. quadro BL
        progressivo_sezione = 0
        sezione_max = 1
        for line in comunicazione.line_BL_ids:
            progressivo_modulo +=1
            progressivo_sezione +=1
            if progressivo_sezione > sezione_max :
                progressivo_sezione = 1
            content += self._record_C_BL(cr, uid, line, progressivo_modulo, progressivo_sezione, context=context)
            numero_record_C += 1
        
        # .. quadro SE
        progressivo_sezione = 0
        sezione_max = 3
        for line in comunicazione.line_SE_ids:
            progressivo_modulo +=1
            progressivo_sezione +=1
            if progressivo_sezione > sezione_max :
                progressivo_sezione = 1
            content += self._record_D_SE(cr, uid, line, progressivo_modulo, progressivo_sezione, context=context)
            numero_record_D += 1
        
        # Riepilogo
        progressivo_modulo = 1
        content += self._record_E(cr, uid, comunicazione, progressivo_modulo, context=context)
        numero_record_E += 1
        
        # Coda
        args = {
                'numero_record_B' : numero_record_B,
                'numero_record_C' : numero_record_C,
                'numero_record_D' : numero_record_D,
                'numero_record_E' : numero_record_E,
                }
        content += self._record_Z(cr, uid, args, context=None)
        

        
        out=base64.encodestring(content.encode("utf8"))
        #return self.write(cr, uid, ids, {'file_spesometro':out}, context=context)
        
        self.write(cr, uid, ids, {'file_spesometro':out}, context=context)

        return {
           'view_type': 'form',
           'view_id' : [view_id],
           'view_mode': 'form',
           'res_model': 'wizard.spesometro.export',
           'res_id': ids[0],
           'type': 'ir.actions.act_window',
           'target': 'new',
           'context': context,
        }
       
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: