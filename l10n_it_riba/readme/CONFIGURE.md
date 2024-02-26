**Italiano**

Nella configurazione delle RiBa è possibile specificare se si tratti di
'Salvo buon fine' o 'Al dopo incasso', che hanno un flusso completamente
diverso.

- Al dopo incasso: nessuna registrazione verrà effettuata
  automaticamente e le fatture risulteranno pagate solo al momento
  dell'effettivo incasso.
- Salvo buon fine: le registrazioni generate seguiranno la struttura
  descritta nel documento <http://goo.gl/jpRhJp>

È possibile specificare diverse configurazioni (dal menù *Configurazione
→ Pagamenti → Configurazione RiBa*). Per ognuna, in caso di 'Salvo buon
fine', è necessario specificare almeno il registro e il conto da
utilizzare al momento dell'accettazione della distinta da parte della
banca. Tale conto deve essere di tipo 'Crediti' (ad esempio "RiBa
all'incasso", eventualmente da creare).

La configurazione relativa alla fase di accredito, verrà usata nel
momento in cui la banca accredita l'importo della distinta. È possibile
utilizzare un registro creato appositamente, ad esempio "Accredito
RiBa", e un conto chiamato ad esempio "Banche c/RiBa all'incasso", che
non deve essere di tipo 'Banca e cassa'.

La configurazione relativa all'insoluto verrà utilizzata in caso di
mancato pagamento da parte del cliente. Il conto può chiamarsi ad
esempio "Crediti insoluti".

Nel caso si vogliano gestire anche le spese per ogni scadenza con
ricevuta bancaria, si deve configurare un prodotto di tipo servizio e
collegarlo in *Configurazione → Impostazioni → Contabilità → Imposte →
Spese di incasso RiBa*.
