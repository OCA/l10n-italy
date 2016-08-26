# -*- coding: utf-8 -*-
##############################################################################
#    
#    Author: Alessandro Camilli (a.camilli@yahoo.it)
#    Copyright (C) 2014
#    Associazione OpenERP Italia (<http://www.openerp-italia.org>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields,osv
from tools.translate import _
import time 

class wizard_crea_comunicazione(osv.osv_memory):
    
    def default_get(self, cr, uid, fields, context=None):
        
        res = super(wizard_crea_comunicazione, self).default_get(cr, uid, fields, context=context)
        
        res['periodo'] = 'anno'
        res['anno'] = int(time.strftime('%Y')) -1
        res['tipo'] = 'ordinaria'
        res['formato_dati'] = 'aggregati'
        res['quadro_FA'] = True
        res['quadro_SA'] = True
        res['quadro_BL'] = True
        res['quadro_SE'] = True
        res['tipo_fornitore'] = '01'
        
        return res

    _name = "wizard.spesometro.crea.comunicazione"
    
    _columns = {
        'company_id': fields.many2one('res.company', 'Azienda', required=True ),
        'periodo': fields.selection((('anno','Annuale'), ('trimestre','Trimestrale'), ('mese','Mensile')),
                   'Periodo', required=True),
        'anno' : fields.integer('Anno', size=4, required=True),
        'trimestre' : fields.integer('Trimestre', size=1 ),
        'mese' : fields.selection(((1,'Gennaio'), (2,'Febbraio'), (3,'Marzo'), (4,'Aprile'),
                                   (5,'Maggio'), (6,'Giugno'), (7,'Luglio'), (8,'Agosto'),
                                   (9,'Settembre'), (10,'Ottobre'), (11,'Novembre'), (12,'Dicembre'),
                                   ),'Mese'),
        
        'tipo': fields.selection((('ordinaria','Ordinaria'), ('sostitutiva','Sostitutiva'), ('annullamento','Annullamento')),
                   'Tipo comunicazione', required=True),
        'comunicazione_da_sostituire_annullare': fields.integer('Protocollo comunicaz. da sostituire/annullare'),
        'documento_da_sostituire_annullare': fields.integer('Protocollo documento da sostituire/annullare'),
        'formato_dati': fields.selection((('aggregati','Aggregati'),('analitici','Analitici')),'Formato comunicazione', required=True),
        'tipo_fornitore': fields.selection((('01','Soggetti che inviano la propria comunicazione'), ('10','Intermediari')),
                   'Tipo fornitore', required=True),
        'partner_intermediario': fields.many2one('res.partner', 'Intermediario'),
        'quadro_FA': fields.boolean('Quadro FA', help="Operazioni documentate da fattura esposte in forma aggregata"),
        'quadro_SA': fields.boolean('Quadro SA', help="Operazioni senza fattura esposte in forma aggregata"),
        'quadro_BL': fields.boolean('Quadro BL', help="- Operazioni con paesi con fiscalità privilegiata - Operazioni con soggetti non residenti - Acquisti di servizi da soggetti non residenti "),
        
        'quadro_FE': fields.boolean('Quadro FE', help="Fatture emesse e Documenti riepilogativi (Operazioni attive)"),
        'quadro_FR': fields.boolean('Quadro FR', help="Fatture ricevute e Documenti riepilogativi (Operazioni passive)"),
        'quadro_NE': fields.boolean('Quadro NE', help="Note di variazione emesse"),
        'quadro_NR': fields.boolean('Quadro NR', help="Note di variazioni ricevute"),
        'quadro_DF': fields.boolean('Quadro DF', help="Operazioni senza fattura"),
        'quadro_FN': fields.boolean('Quadro FN', help="Operazioni con soggetti non residenti (Operazioni attive)"),
        'quadro_SE': fields.boolean('Quadro SE', help="Acquisti di servizi da non residenti e Acquisti da operatori di San Marino"),
        'quadro_TU': fields.boolean('Quadro TU', help="Operazioni legate al turismo - Art. 3 comma 1 D.L. 16/2012"),
    }
    
    def genera_comunicazione(self, cr, uid, ids, context=None):
        
        comunicazione_obj = self.pool.get('spesometro.comunicazione')
        wizard = self.read(cr, uid, ids)[0]
        
        # Quadri richiesti:
        quadri_richiesti = []
        if wizard['quadro_FA']:
            quadri_richiesti.append('FA')
        if wizard['quadro_SA']:
            quadri_richiesti.append('SA')
        if wizard['quadro_BL']:
            quadri_richiesti.append('BL')
        if wizard['quadro_FE']:
            quadri_richiesti.append('FE')
        if wizard['quadro_FR']:
            quadri_richiesti.append('FR')
        if wizard['quadro_NE']:
            quadri_richiesti.append('NE')
        if wizard['quadro_NR']:
            quadri_richiesti.append('NR')
        if wizard['quadro_DF']:
            quadri_richiesti.append('DF')
        if wizard['quadro_FN']:
            quadri_richiesti.append('FN')
        if wizard['quadro_SE']:
            quadri_richiesti.append('SE')
        if wizard['quadro_TU']:
            quadri_richiesti.append('TU')
                
        params ={
               'company_id': wizard['company_id'][0],
               'periodo': wizard['periodo'], 
               'anno': wizard['anno'], 
               'trimestre': wizard['trimestre'], 
               'mese': wizard['mese'], 
               'tipo': wizard['tipo'], 
               'comunicazione_da_sostituire_annullare': wizard['comunicazione_da_sostituire_annullare'], 
               'documento_da_sostituire_annullare': wizard['documento_da_sostituire_annullare'], 
               'formato_dati': wizard['formato_dati'], 
               'tipo_fornitore': wizard['tipo_fornitore'], 
               'partner_intermediario': wizard['partner_intermediario'], 
               'quadri_richiesti': quadri_richiesti, 
               }
        comunicazione_obj.genera_comunicazione(cr, uid, params, context=None)
        
        return {
            'type': 'ir.actions.act_window_close',
        }
