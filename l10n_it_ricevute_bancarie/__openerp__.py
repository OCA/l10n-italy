# -*- coding: utf-8 -*-
<<<<<<< HEAD
<<<<<<< HEAD
##############################################################################
#    
=======
#
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba
#
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
#    Copyright (C) 2012 Andrea Cometa.
#    Email: info@andreacometa.it
#    Web site: http://www.andreacometa.it
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
<<<<<<< HEAD
<<<<<<< HEAD
##############################################################################
=======
#
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
=======
##############################################################################
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba

{
    "name": "Ricevute Bancarie",
    "version": "1.3",
    "author": "Odoo Italian Community",
    "category": "Accounting & Finance",
<<<<<<< HEAD
    "website": "http://www.openerp-italia.org",
<<<<<<< HEAD
    "license": "AGPL-3",
    "description": """
Gestione delle Ricevute Bancarie
--------------------------------
Nella configurazione delle Ri.Ba. è possibile specificare se si tratti di 'salvo buon fine' o 'al dopo incasso'. I due tipi di Ri.Ba. hanno un flusso completamente diverso. In caso di 'al dopo incasso', nessuna registrazione verrà effettuata automaticamente e le fatture risulteranno pagate solo al momento dell'effettivo incasso.

E' possibile specificare diverse configurazioni (dal menù configurazioni -> varie -> Ri.Ba.). Per ognuna, in caso di 'salvo buon fine', è necessario specificare almeno il sezionale ed il conto da utilizzare al momento dell'accettazione della distinta da parte della banca.
La configurazione relativa alla fase di accredito, verrà usata nel momento in cui la banca accredita l'importo della distinta. Mentre quella relativa all'insoluto verrà utilizzato in caso di mancato pagamento da parte del cliente.

Per utilizzare il meccanismo delle Ri.Ba. è necessario configurare un termine di pagamento di tipo 'Ri.Ba.'.

Per emettere una distinta bisogna andare su Ri.Ba. -> emetti Ri.Ba. e selezionare i pagamenti per i quali emettere la distinta.
Se per il cliente è stato abilitato il raggruppo, i pagamenti dello stesso cliente e con la stessa data di scadenza andranno a costituire un solo elemento della distinta.

I possibili stati della distinta sono: bozza, accettata, accreditata, pagata, insoluta, annullata.
Ad ogni passaggio di stato sarà possibile generare le relative registrazioni contabili, le quali verranno riepilogate nel tab 'contabilità'. Questo tab è presente sia sulla distinta che sulle sue righe.

Qui https://docs.google.com/document/d/1xCqeTcY6CF-Dgk_Avthhy7iwg_aG86WzNv3E_HHQkt4/edit# abbiamo un esempio delle tipiche registrazioni generate da un flusso 'salvo buon fine'.
    """,
    'images': [],
    'depends': ['account','account_voucher', 'l10n_it_fiscalcode', 'account_due_list'],
=======
=======
    "website": "http://www.odoo-italia.org",
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba
    "description": """
Gestione delle Ricevute Bancarie
--------------------------------
Nella configurazione delle Ri.Ba. è possibile specificare se si tratti di
'salvo buon fine' o 'al dopo incasso'. I due tipi di Ri.Ba. hanno un flusso
completamente diverso. In caso di 'al dopo incasso', nessuna registrazione
verrà effettuata automaticamente e le fatture risulteranno pagate solo al
momento dell'effettivo incasso.

E' possibile specificare diverse configurazioni (dal menù
configurazioni -> varie -> Ri.Ba.). Per ognuna, in caso di 'salvo buon fine',
è necessario specificare almeno il sezionale ed il conto da
utilizzare al momento dell'accettazione della distinta da parte della banca.
La configurazione relativa alla fase di accredito, verrà usata nel momento in
cui la banca accredita l'importo della distinta. Mentre quella relativa
all'insoluto verrà utilizzato in caso di
mancato pagamento da parte del cliente.

Per utilizzare il meccanismo delle Ri.Ba. è necessario configurare un termine
di pagamento di tipo 'Ri.Ba.'.

Per emettere una distinta bisogna andare su Ri.Ba. -> emetti Ri.Ba. e
selezionare i pagamenti per i quali emettere la distinta.
Se per il cliente è stato abilitato il raggruppo, i pagamenti dello stesso
cliente e con la stessa data di scadenza andranno a costituire un solo elemento
della distinta.

I possibili stati della distinta sono: bozza, accettata, accreditata, pagata,
insoluta, annullata.
Ad ogni passaggio di stato sarà possibile generare le relative registrazioni
contabili, le quali verranno riepilogate nel tab 'contabilità'.
Questo tab è presente sia sulla distinta che sulle sue righe.

Qui
http://goo.gl/jpRhJp abbiamo un esempio delle tipiche registrazioni generate
da un flusso 'salvo buon fine'.
    """,
    'images': [],
    'depends': [
        'account',
        'account_voucher',
        'l10n_it_fiscalcode',
<<<<<<< HEAD
<<<<<<< HEAD
        'account_due_list',
        'base_iban',
    ],
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    'init_xml': [],
=======
        'account_due_list'],
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba
=======
        'account_due_list',
        'base_iban'],
>>>>>>> 154323a... fixed errors in tests and added dep needed
    'data': [
        "views/partner_view.xml",
        "views/configuration_view.xml",
        "riba_sequence.xml",
        "views/wizard_accreditation.xml",
        "views/wizard_unsolved.xml",
        "views/riba_view.xml",
        "views/account_view.xml",
        "views/wizard_riba_issue.xml",
        "views/wizard_riba_file_export.xml",
        "views/account_config_view.xml",
        "riba_workflow.xml",
        # "security/ir.model.access.csv",
    ],
<<<<<<< HEAD
<<<<<<< HEAD
    'demo_xml': [],
    'test': [],
    'installable': False,
=======
    'demo_xml': [
        'demo/riba_demo.xml',
        ],
=======
    'demo': ["demo/riba_demo.xml"],
<<<<<<< HEAD
>>>>>>> 8fe6aa6... added l10n_it_ricevute_bancarie from 8.0-riba
    'test': [
        'test/riba_invoice.yml',
        'test/issue_riba.yml',
        'test/unsolved_riba.yml',
        ],
=======
    # 'test': [
    #     'test/riba_invoice.yml',
    #     'test/issue_riba.yml',
    #     'test/unsolved_riba.yml',
    #     ],
>>>>>>> 67ced3e... [IMP] Management of due cost for Ri.Ba.
    'installable': True,
>>>>>>> 20676d5... added l10n_it_ricevute_bancarie from 7.0
    'active': False,
}
